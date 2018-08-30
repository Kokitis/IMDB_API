import math
from pprint import pprint
from functools import partial

pprint = partial(pprint, width = 150)
import requests
from typing import *
from ..github import numbertools, omdb_api_key, timetools
from .resources import EpisodeResource, MediaResource, SeasonResource

_toNumber = numbertools.to_number

#pendulum.DateTime.__float__ = lambda s: s.year + s.day_of_year / 365  # So ax.scatter can convert the dates.


def checkValue(value, *items):
	""" Raises a ValueError if 'value' is not in 'items'. If None is passed, will return the first element of items."""
	if value is not None:
		value = value.lower()
		if value not in items:
			message = "'{}' is not an available option. Expected one of {}".format(value, items)
			raise ValueError(message)
	else:
		value = items[0]

	return value


_toTimestamp = lambda value: timetools.Timestamp(value) if value  != "N/A" else math.nan

_toDuration = lambda value: timetools.Duration(minutes = int(value.split(' ')[0])) if value != 'N/A' else math.nan


class OmdbApi:
	def __init__(self, api_key: str = omdb_api_key):

		self.api_key: str = api_key

	def _parseEpisode(self, episode: dict, season: int, previous: int, form: Optional[str]) -> Union[
		EpisodeResource, MediaResource]:
		"""

		Parameters
		----------
		episode: Dict
			The short-form response from the api.
		season: int
			The season index.
		previous:int
			Number of episodes occuring in the season prior to this one.
		form: str; default None

		Returns
		-------
		EpisodeResponse
		"""
		as_media_resource = form == 'long'
		imdb_rating = _toNumber(episode.get('imdbRating', ' N/A'))
		release_date = _toTimestamp(episode['Released'])
		episode_id = "S{:>02}E{:>02}".format(season, episode['Episode'])
		episode_index = previous + int(episode['Episode'])

		episode_data = dict(
			title = episode['Title'],
			imdbId = episode['imdbID'],
			imdbRating = float(imdb_rating),
			releaseDate = release_date,
			episodeId = episode_id,
			indexInSeries = episode_index,
			indexInSeason = _toNumber(episode['Episode'])
		)
		if as_media_resource:
			episode_resource = self.get(episode_data['imdbId'], asdict = True)
			episode_data.update(episode_resource)
			episode_resource = MediaResource(**episode_data)
		else:
			episode_resource = EpisodeResource(**episode_data)
		return episode_resource

	def _parseMediaResponse(self, api_response: Dict, episode_format: Optional[str]) -> Dict:
		"""

		Parameters
		----------
		api_response
		episode_format: {None, 'short', 'long'};  default 'long'}

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

			series_seasons = self.getSeasons(imdb_id, episode_format = episode_format)

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
		kind = checkValue(kind, 'series', 'movie', 'any')
		parameters = {
			's': string
		}
		if kind is not None:
			parameters['type'] = kind
		response = self.request(**parameters)

		status = response['Response'] == 'True'
		if status:
			total_results = int(response['totalResults'])
			response['Response'] = status
			response['totalResults'] = total_results
		else:
			response = None
		return response

	def find(self, string: str, kind: str = 'series', **kwargs) -> Optional[MediaResource]:
		""" Searches the api for a show title and returns the first result. """
		kwargs['episode_format'] = kwargs.get('episode_format', 'short')
		search_response = self.search(string, kind)

		if not search_response or not search_response['Response']:
			result = None
		else:
			first_result = search_response['Search'][0]

			first_result_id = first_result['imdbID']

			result = self.get(first_result_id, **kwargs)
		return result

	def get(self, string: str, episode_format: Optional[str] = None, asdict = False, **kwargs) -> MediaResource:
		"""
			Parameters
			----------
			string: str
				One of the following:
				*'i': IMDB ID
				*'s': Search term
			episode_format: {None, 'short', 'full'}; default None
				*  None: Do not include seasons.
				* 'short': Retrieve short-form episodes
				* 'long': Retrieve long-form episodes.
			asdict: bool; default False
				Return the response from the api as a dict rather than a resource.
			Returns
			-------
			MediaResponse
		"""
		episode_format = checkValue(episode_format, None, 'short', 'long')
		_key = 'i' if string.startswith('tt') else 't'

		parameters = {
			_key: string
		}
		response = self.request(**parameters)
		# Should include error checking

		if 'Type' not in response:
			result = response
		else:
			result = self._parseMediaResponse(response, episode_format)
		if not asdict:
			#pprint(result)
			result = MediaResource(**result)

		return result

	def getSeasons(self, series_id: str, episode_format: str = 'short') -> List[SeasonResource]:
		"""
			Gathers all episodes for the given series.
		Parameters
		----------
		series_id: str
		episode_format: {None, 'short', 'long'}
			Controls if episodes are represented by the short-form EpisodeResource or the long-form Media Resource.

		Returns
		-------

		"""
		if episode_format == 'empty': return []
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
				season_episodes = [
					self._parseEpisode(e, season_number, previous_episodes, form = episode_format)
					for e in response['Episodes']
				]

				season_result = SeasonResource(
					episodes = season_episodes,
					seasonIndex = _toNumber(response['Season']),
					length = len(season_episodes),
					seriesTitle = response['Title']
				)
				seasons.append(season_result)
				previous_episodes += max(season_episodes, key = lambda s: s.indexInSeason).indexInSeason
			else:
				break
		return seasons

	def request(self, **parameters) -> Dict:
		parameters['apikey'] = self.api_key
		url = "http://www.omdbapi.com/"
		response = requests.get(url, parameters)
		response = response.json()
		return response
