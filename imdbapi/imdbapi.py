import requests
import json
from bs4 import BeautifulSoup
import re
import math
from typing import *
from infotools import timetools
from pathlib import Path
from toolz import itertoolz
import pandas
import datetime

try:
	import resources
except ModuleNotFoundError:
	from . import resources


class IMDBResponseParser:
	"""
		Parses the response from the IMDB API and converts it to the standardized MediaResponse format.
	"""

	def __init__(self):
		# Define the default values to use when the IMDB response is missing information.
		self.default_value_str = "N/A"
		self.default_value_float = math.nan
		self.default_value_int = 0
		self.default_value_list = []
		self.default_value_timestamp = None
		self.default_value_duration = None

		self.imdb_id_regex = re.compile("tt[\d]{7,8}")

		# Define how the types returned by the IMDB API map to those used in the standard MediaResource format.
		self.typemap = {
			'TVEpisode': 'episode',
			'Movie':     'movie',
			'TVSeries':  'series'
		}
	@staticmethod
	def _parse_actors(response: resources.IMDBResponse) -> List[str]:
		raw_actors: List[resources.IMDBEntity] = response['actor']
		actors = [i['name'] for i in raw_actors]
		return actors

	def _parse_runtime(self, response: resources.IMDBResponse) -> datetime.timedelta:
		"""
			Each response may store the duration under 'duration' or 'timeRequired', if it's available at all.
		"""

		duration_string: Optional[str] = response.get('duration', response.get('timeRequired'))

		if duration_string:
			result = timetools.Duration(duration_string).as_timedelta()
		else:
			result = self.default_value_duration

		return result

	def _parse_director(self, response: resources.IMDBResponse) -> List[str]:
		director = response.get('director')
		if director is None:
			director = self.default_value_list
		elif not isinstance(director, list):
			director = [director]

		director = [d['name'] for d in director]
		return director

	def _parse_date_published(self, response: resources.IMDBResponse) -> datetime.datetime:
		timestamp = response.get('datePublished', self.default_value_timestamp)
		if timestamp is not None:
			timestamp = timetools.Timestamp(timestamp).to_datetime()
		else:
			timestamp = self.default_value_timestamp

		return timestamp

	def _parse_imdb_rating(self, response: resources.IMDBResponse) -> Tuple[float, int]:
		"""
			Extracts the IMDB rating and vote count from the response.
		"""

		imdb_rating_data: Optional[resources.IMDBRatingAggregate] = response.get('aggregateRating')

		if imdb_rating_data:
			imdb_rating = float(imdb_rating_data['ratingValue'])
			vote_count = imdb_rating_data['ratingCount']
		else:
			imdb_rating = self.default_value_float
			vote_count = self.default_value_int

		return imdb_rating, vote_count
	@staticmethod
	def _parse_imdb_id(response: resources.IMDBResponse) -> str:
		"""
			Extracts the IMDB ID from the response.
		"""

		url = response['url']  # "/title/tt0076759/"
		imdb_id = url.split('/')[-2]

		return imdb_id

	def _parse_tags(self, response: resources.IMDBResponse) -> List[str]:
		tag_string = response.get('keywords')
		if tag_string:
			result = tag_string.split(',')
		else:
			result = self.default_value_list
		return result

	def _parse_type(self, response: resources.IMDBResponse) -> Literal[None, "movie", "series", "episode"]:
		media_type = response['type']
		result = self.typemap.get(media_type)
		return result

	def parse_response(self, response: resources.IMDBResponse):
		actors = self._parse_actors(response)

		runtime = self._parse_runtime(response)
		published = self._parse_date_published(response)
		director = self._parse_director(response)

		imdb_rating, vote_count = self._parse_imdb_rating(response)

		# This API only has the IMDB rating. Only need to include this if a rating is available
		if not math.isnan(imdb_rating):
			ratings = [
				{
					"Source": "Internet Movie Database",
					"Value":  f"{imdb_rating}/10"
				}
			]
		else:
			ratings = self.default_value_list

		result = {
			'actors':      actors,
			'awards':      self.default_value_str,
			'countries':   self.default_value_list,
			'director':    director,
			'genres':      response.get('genre', self.default_value_list),
			'imdbId':      self._parse_imdb_id(response),
			'imdbRating':  imdb_rating,
			'imdbVotes':   vote_count,
			'languages':   [],
			'plot':        response.get('description', self.default_value_str),
			'poster':      response.get('image', self.default_value_str),
			'rated':       response.get('contentRating', self.default_value_str),
			'ratings':     ratings,
			'releaseDate': published,
			'runtime':     runtime,
			'tags':        self._parse_tags(response),
			'title':       response.get('name', self.default_value_str),
			'type':        self._parse_type(response),
			'writers':     []
		}

		return result


class IMDBRequester:
	"""
		Sends requests to the IMDB Website and returns the pseudo-api JSON-formatted response.
	"""
	def __init__(self):
		self.base_url = "https://www.imdb.com/"
	def __call__(self, imdb_id: str) -> resources.IMDBResponse:
		"""
			Returns the response from the API-like data scraped from the imdb website.
		"""

		return self.request_page(imdb_id)

	@staticmethod
	def _extract_api_response(response: requests.Response) -> Dict:
		""" Extracts the JSON-formatted api response from the html source"""
		soup = BeautifulSoup(response.text, features = 'lxml')
		script = soup.find(**{'type': 'application/ld+json'})

		content = str(script)[35:-9]
		result = json.loads(content)
		return result

	def _fix_dictionary_keys(self, data: resources.IMDBResponse) -> Dict:
		"""
			The IMDB api prepends some of the keys in their JSON responses with an @ symbol, which makes defining the structure via a TypedDict
			annoying. This method should remove that character in both the given dictionary and any dictionary values.
		"""

		result = dict()

		for key, value in data.items():
			if key.startswith('@'): key = key[1:]
			if isinstance(value, dict): value = self._fix_dictionary_keys(value)
			elif isinstance(value, list): value = [(self._fix_dictionary_keys(i) if isinstance(i, dict) else i) for i in value]

			result[key] = value

		return result

	def request_page(self, imdb_id: str):
		url = f"https://www.imdb.com/title/{imdb_id}"

		response = requests.get(url)
		result = self._extract_api_response(response)
		result = self._fix_dictionary_keys(result)

		return result

	def request_page_season(self, imdb_id: str, season_index:int)->str:
		"""
			Returns the text of the webpage which shows all episodes within a single season, in HTML format.
		"""

		endpoint_template = self.base_url + "title/{imdb_id}/episodes"

		parameters = {'season': season_index}
		response = requests.get(endpoint_template.format(imdb_id = imdb_id), parameters)

		return response.text

class IMDB:
	def __init__(self):
		# https://www.imdb.com/title/tt1312171/episodes
		self.base_url = "https://www.imdb.com/"

		self.request = IMDBRequester()
		self.parser = IMDBResponseParser()

	################################################ Utilities ################################################

	########################################## Season Parser ################################################
	def _extract_episode_ids_from_season_page(self, response: str) -> List[str]:
		ids = self.parser.imdb_id_regex.findall(response)
		# Need to remove duplicate IDs from the response
		ids = itertoolz.unique(ids)

		return ids

	################################################ Media Parser ############################################

	########################################## Public Methods ###############################################

	def flatten(self, resource:resources.MediaResource)->Dict[str, Union[str,int,float]]:
		"""
			Flattens the values of a resource object so they can be inserted into a pandasDataFrame more easily.

		"""
		result = dict()
		## Probably won't need all of the ratings since only the IMDB ratings are available.
		exclude = ['ratings']
		for key, value in resource.items():
			# Convert each `list` value in to a comma-delimited string.
			if key in exclude:
				continue
			elif isinstance(value, list):
				result[key] = ",".join(value)
			else:
				result[key] = value
		return result

	def get_episodes(self, imdb_id: str)->pandas.DataFrame:
		"""
			Retrieves the MediaResource objects for all episodes corresponding to the specified ID.
		"""
		series_resource = self.get(imdb_id)
		seasons:Dict[int,List[str]] = self.get_season_episodes(imdb_id)

		episodes:List[resources.EpisodeResource] = list()

		for season_index, season_episodes in seasons.items():
			for episode_index, episode_id in enumerate(season_episodes, start = 1):
				episode_response = self.request(episode_id)
				episode_resource = self.parser.parse_response(episode_response)

				# Need to add three more attributes: 'seasonIndex', 'indexInSeason', 'seriesId'
				# The 'seasonIndex' is just which season the episode belongs to
				episode_resource['seasonIndex'] = season_index

				# The 'indexInSeason' describes where in the season the episode aired.
				episode_resource['indexInSeason'] = episode_index

				# The 'seriesId' field provides an easy way of specifying this episode in a human readable way.
				series_id = f"S{season_index:>02}E{episode_index:>02}"
				episode_resource['seriesId'] = series_id

				# Add information about the parent series
				episode_resource['parentTitle'] = series_resource['title']
				episode_resource['parentId'] = series_resource['imdbId']

				# Since these will be converted to a pandas.DataFrame, we need to flatten each of the values.
				episode_result = self.flatten(episode_resource)
				episodes.append(episode_result)

		return episodes


	def get_season_episodes(self, imdb_id: str) -> Dict[int, List[str]]:
		"""
			Returns a dictionary mapping all episode Ids to the corresponding season index.
		"""
		seasons = dict()
		endpoint_template = self.base_url + "title/{imdb_id}/episodes"
		previous = None
		for season_index in range(1, 100):
			response_html = self.request.request_page_season(imdb_id, season_index)
			episode_ids = self._extract_episode_ids_from_season_page(response_html)
			episode_ids = [i for i in episode_ids if i != imdb_id]
			if episode_ids == previous:
				break
			else:
				seasons[season_index] = episode_ids
				previous = episode_ids

		return seasons

	def get(self, imdb_id:str)->resources.MediaResource:
		"""
			Returns a MediaResource Object with all details available for the requested imdb id.
		"""

		response = self.request(imdb_id)
		resource = self.parser.parse_response(response)

		return resource


def main():
	api = IMDB()
	# /home/proginoskes/Documents/GitHub/omdbapi/tests/data_for_imdb_api/
	folder_data = Path.home() / "Documents" / "Github" / "omdbapi" / "tests" / "data_for_imdb_api"
	series_id_umbrella = 'tt1312171'
	series_id_avatar = "tt0417299"
	series_id_kings = "tt1137462"

	episode_id_sozins_comet = "tt1204265"
	episode_id_angels_take_manhattan = "tt2378951"
	episode_id_umbrella_academy_s03e02 = "tt13435916"

	movie_id_avatar = "tt0499549"
	movie_id_a_new_hope = "tt0076759"
	movie_id_avengers_endgame = "tt4154796"

	response = api.request(series_id_umbrella)

	print(folder_data.exists())
	"""
	(folder_data / "sample_response_series_umbrella.json").write_text(json.dumps(api.request(series_id_umbrella), indent = 4, sort_keys = True))
	(folder_data / "sample_response_series_avatar.json").write_text(json.dumps(api.request(series_id_avatar), indent = 4, sort_keys = True))
	(folder_data / "sample_response_series_kings.json").write_text(json.dumps(api.request(series_id_kings), indent = 4, sort_keys = True))

	(folder_data / "sample_response_episode_sozins_comet.json").write_text(
		json.dumps(api.request(episode_id_sozins_comet), indent = 4, sort_keys = True))
	(folder_data / "sample_response_episode_angels_take_manhattan.json").write_text(
		json.dumps(api.request(episode_id_angels_take_manhattan), indent = 4, sort_keys = True))
	(folder_data / "sample_response_episode_umbrella_s03e02.json").write_text(
		json.dumps(api.request(episode_id_umbrella_academy_s03e02), indent = 4, sort_keys = True))

	(folder_data / "sample_response_movie_avatar.json").write_text(json.dumps(api.request(movie_id_avatar), indent = 4, sort_keys = True))
	(folder_data / "sample_response_movie_a_new_hope.json").write_text(json.dumps(api.request(movie_id_a_new_hope), indent = 4, sort_keys = True))
	(folder_data / "sample_response_movie_avengers_endgame.json").write_text(
		json.dumps(api.request(movie_id_avengers_endgame), indent = 4, sort_keys = True))
	"""

	result = api.get_episodes(series_id_kings)
	from pprint import pprint
	pprint(result)

if __name__ == "__main__":
	main()
