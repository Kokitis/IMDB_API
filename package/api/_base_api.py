import math
from pprint import pprint
from functools import partial

pprint = partial(pprint, width = 150)
import requests
from typing import *
from ..github import timetools, numbertools, omdb_api_key
from dataclasses import dataclass, fields

_toNumber = numbertools.toNumber


class BasicResource:

	def __post_init__(self):
		self._keys = tuple(i.name for i in fields(self))
		for field in fields(self):
			self._checkType(field)

	def __getitem__(self, item):
		if item not in self.keys():
			message = "'{}' does not exist in the keys.".format(item)
			raise KeyError(message)
		return getattr(self, item)

	def _checkType(self, field):
		value = self[field.name]
		try:
			if not isinstance(value, field.type):
				message = "Expected type '{}' in field '{}', got '{}' instead ('{}').".format(
					field.type,
					field.name,
					type(value),
					value
				)
				print("WARNING: ", message)
		except TypeError:
			# isinstance doesn't work with parametrized generics.
			pass

	def keys(self):
		return self._keys


@dataclass
class EpisodeResource(BasicResource):
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: timetools.Timestamp
	id: str
	indexInSeries: int
	indexInSeason: int


@dataclass
class SeasonResource(BasicResource):
	episodes: List[EpisodeResource]
	seasonIndex: int
	length: int
	seriesTitle: str

	def summary(self):
		print("{} Season {}".format(self.seriesTitle, self.seasonIndex))
		for i in self.episodes:
			print("\t{}. {}".format(i.indexInSeason, i))
	def __iter__(self):
		for i in self.episodes:
			yield i


@dataclass
class MediaResource(BasicResource):
	actors: str
	awards: str
	country: str
	director: str
	duration: timetools.Duration
	genre: str
	imdbId: str
	imdbRating: float
	imdbVotes: int
	language: str
	metascore: float
	plot: str
	rating: str
	ratings: List[Dict[str, str]]
	releaseDate: timetools.Timestamp
	responseStatus: bool
	title: str
	totalSeasons: int
	type: str
	writer: str
	year: str
	seasons: Optional[List[SeasonResource]]


def _toTimestamp(value, default = math.nan):
	if value == 'N/A':
		result = default
	else:
		result = timetools.Timestamp(value)
	return result


def _toDuration(value, default = math.nan):
	if value == 'N/A':
		result = default
	else:
		result = value.split(' ')
		result = int(result[0])
		result = timetools.Duration(minutes = result)
	return result


class OmdbApi:
	def __init__(self, api_key: str = omdb_api_key):

		self.api_key: str = api_key

	@staticmethod
	def _parseEpisode(episode_response: dict, season_number: int, previous_episodes: int) -> EpisodeResource:
		"""

		Parameters
		----------
		episode_response: EpisodeResponse
		season_number: int
		previous_episodes:int

		Returns
		-------
		EpisodeResponse
		"""
		imdb_rating = _toNumber(episode_response.get('imdbRating', ' N/A'))
		release_date = _toTimestamp(episode_response['Released'])
		episode_id = "S{:>02}E{:>02}".format(season_number, episode_response['Episode'])
		episode_index = previous_episodes + int(episode_response['Episode'])

		parsed_episode = EpisodeResource(
			title = episode_response['Title'],
			imdbId = episode_response['imdbID'],
			imdbRating = float(imdb_rating),
			releaseDate = release_date,
			id = episode_id,
			indexInSeries = episode_index,
			indexInSeason = _toNumber(episode_response['Episode'])
		)
		return parsed_episode

	def _parseMediaResponse(self, api_response: Dict, include_seasons: bool) -> Dict:
		"""

		Parameters
		----------
		api_response
		include_seasons

		Returns
		-------
		MediaResponse
		"""
		media_type = api_response['Type']
		imdb_id = api_response['imdbID']
		imdb_votes = _toNumber(api_response['imdbVotes'].replace(',', ''))
		imdb_rating = _toNumber(api_response['imdbRating'])

		api_response_status = api_response['Response'] == 'True'
		# years = api_response['Year'].split('-')
		years = api_response['Year']
		release_date = api_response['Released']
		release_date = _toTimestamp(release_date)

		runtime = _toDuration(api_response['Runtime'])
		metacritic_score = _toNumber(api_response['Metascore'])

		parsed_response = {
			'actors':         api_response['Actors'],
			'awards':         api_response['Awards'],
			'country':        api_response['Country'],
			'director':       api_response['Director'],
			'genre':          api_response['Genre'],
			'language':       api_response['Language'],
			'metascore':      metacritic_score,
			'plot':           api_response['Plot'],
			# 'poster': api_response['Poster'],
			'rating':         api_response['Rated'],
			'ratings':        api_response['Ratings'],
			'title':          api_response['Title'],
			'type':           media_type,
			'writer':         api_response['Writer'],
			'year':           years,
			'imdbId':         imdb_id,
			'responseStatus': api_response_status,
			'imdbRating':     imdb_rating,
			'imdbVotes':      imdb_votes,
			'releaseDate':    release_date,
			'duration':       runtime,
		}
		if media_type == 'series':
			total_seasons = _toNumber(api_response['totalSeasons'])

			if include_seasons:
				series_seasons = self.getSeasons(imdb_id)
			else:
				series_seasons = list()

			parsed_response['totalSeasons'] = total_seasons
			parsed_response['seasons'] = series_seasons

		return parsed_response

	def search(self, string: str, kind: Optional[str] = None) -> Dict:
		"""
			Searches the api for a string.
		Parameters
		----------
		string
		kind: {'series', 'movie', 'any'}

		Returns
		-------
		SearchResource: dict
			*'Response': bool
			*'Search': list<Dict>
				* 'Poster': url
				* 'Title': str
				* 'Type': {'series', 'movie'}
				* 'Year': str
				* 'imdbID': str
			* 'totalResults': int
		"""

		parameters = {
			's': string
		}
		if kind is not None:
			parameters['type'] = kind
		response = self.request(**parameters)

		status = response['Response'] == 'True'
		total_results = int(response['totalResults'])
		response['Response'] = status
		response['totalResults'] = total_results

		return response

	def find(self, string: str, kind: str = 'series') -> Optional[MediaResource]:
		""" Searches the api for a show title and returns the first result. """
		search_response = self.search(string, kind)

		if not search_response['Response']:
			result = None
		else:
			first_result = search_response['Search'][0]

			first_result_id = first_result['imdbID']

			result = self.get(first_result_id, True)
		return result

	def get(self, string: str, include_seasons: bool = False) -> MediaResource:
		"""
			Parameters
			----------
			string: str
				One of the following:
				*'i': IMDB ID
				*'s': Search term
			include_seasons: bool; default False
			Returns
			-------
			MediaResponse
		"""
		_key = 'i' if string.startswith('tt') else 't'

		parameters = {
			_key: string
		}
		response = self.request(**parameters)
		# Should include error checking

		if 'Type' not in response:
			pprint(response)
			result = response
		else:
			result = self._parseMediaResponse(response, include_seasons)

		result = MediaResource(**result)

		return result

	def getSeasons(self, series_id: str) -> List[SeasonResource]:
		seasons = list()
		index = 0
		previous_episodes = 0
		while True:
			index += 1
			parameters = {
				'i':      series_id,
				'Season': index
			}
			response = self.request(**parameters)
			response_status = response.get('Response', 'False') == 'True'
			if response_status:
				season_number = response['Season']

				season_episodes = [self._parseEpisode(e, season_number, previous_episodes) for e in
								   response['Episodes']]

				season_result = SeasonResource(
					episodes = season_episodes,
					seasonIndex = _toNumber(response['Season']),
					length = len(season_episodes),
					seriesTitle = response['Title']
				)
				seasons.append(season_result)
				previous_episodes += len(season_episodes)
			else:
				break
		return seasons

	def request(self, **parameters) -> Dict:
		parameters['apikey'] = self.api_key
		url = "http://www.omdbapi.com/"
		response = requests.get(url, parameters)
		response = response.json()
		return response
