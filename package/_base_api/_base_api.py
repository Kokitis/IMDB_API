
import math
from pprint import pprint
from functools import partial
pprint = partial(pprint, width = 200)
import requests

from ..github import timetools


def _toNumber(value, default = math.nan):
	if value in {'N/A', None}:
		result = default
	elif isinstance(value, str):
		value = value.replace(',', '')
		if '.' in value:
			result = float(value)
		else:
			result = int(value)
	elif isinstance(value, (int,float)):
		result = value
	else:
		result = default
	return result

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
	def __init__(self, api_key):
		self.endpoint = ""
		self.api_key = api_key

	@staticmethod
	def _parseEpisode(episode_response, season_number, previous_episodes):

		imdb_rating = _toNumber(episode_response.get('imdbRating', ' N/A'))
		release_date = _toTimestamp(episode_response['Released'])
		episode_id = "S{:>02}E{:>02}".format(season_number, episode_response['Episode'])
		episode_index = previous_episodes + int(episode_response['Episode'])
		parsed_episode = {
			'title':         episode_response['Title'],
			'imdbId':        episode_response['imdbID'],
			'imdbRating':    imdb_rating,
			'releaseDate':   release_date,
			'id':            episode_id,
			'indexInSeries': episode_index,
			'indexInSeason': _toNumber(episode_response['Episode'])
		}
		return parsed_episode


	def _parseMediaResponse(self, api_response, include_seasons):
		media_type = api_response['Type']
		imdb_id = api_response['imdbID']
		imdb_votes = _toNumber(api_response['imdbVotes'].replace(',', ''))
		imdb_rating = _toNumber(api_response['imdbRating'])



		api_response_status = api_response['Response'] == 'True'
		#years = api_response['Year'].split('-')
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
			'metaScore':      metacritic_score,
			'plot':           api_response['Plot'],
			# 'poster': api_response['Poster'],
			'rating':         api_response['Rated'],
			'ratings':        api_response['Ratings'],
			'title':          api_response['Title'],
			'type':           media_type,
			'writer':         api_response['Writer'],
			'year':          years,
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


	def search(self, string, kind = None):

		parameters = {
			's':    string,
		}
		if kind is not None:
			parameters['type'] = kind
		response = self.request(**parameters)
		return response

	def find(self, string, kind = 'series'):
		""" Searches the api for a show title and returns the first result. """
		search_response = self.search(string, kind)
		if search_response['Response'] != 'True':
			result = None
		else:
			first_result = search_response['Search'][0]

			first_result_id = first_result['imdbID']

			result = self.get(first_result_id, True)
		return result

	def get(self, string, include_seasons = False):
		"""
			Parameters
			----------
				*'i': IMDB ID
				*'s': Search term
				*'season': int
					Requests a specific season from the api.
		"""
		if string.startswith('tt'):
			_key = 'i'
		else:
			_key = 't'
		parameters = {
			_key: string
		}
		response = self.request(**parameters)
		# Should include error checking
		# if result is None or 'season' in parameters:
		if 'Type' not in response:
			pprint(response)
			result = response
		else:
			result = self._parseMediaResponse(response, include_seasons)

		return result

	def getSeasons(self, series_id):
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
				season_result = {
					'episodes': season_episodes,
					'seasonIndex': _toNumber(response['Season']),
					'length': len(season_episodes),
					'seriesTitle': response['Title']
				}
				seasons.append(season_result)
				previous_episodes += len(season_episodes)
			else:
				break
		return seasons

	def request(self, **parameters):
		parameters['apikey'] = self.api_key
		url = "http://www.omdbapi.com/"
		response = requests.get(url, parameters)
		response = response.json()
		return response
