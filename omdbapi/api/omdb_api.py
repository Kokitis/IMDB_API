import math
from pprint import pprint
from functools import partial

pprint = partial(pprint, width = 150)
import requests
from typing import Union, Dict, Optional, List
from omdbapi.github import omdb_api_key
from omdbapi.api.resources import EpisodeResource, MediaResource, SeasonResource
from omdbapi.api.widgets import _convert_to_timestamp, _convert_to_duration, _is_imdb_id, to_number

API_KEY = omdb_api_key


def _is_valid_response(response: Dict) -> bool:
	""" Checks if a given response is successfull."""
	return 'Type' in response


def _get_request_parameters(string: str, episode_format: Optional[str]) -> Dict[str, str]:
	assert episode_format in {'long', 'short', None}
	_key = 'i' if _is_imdb_id(string) else 't'
	return {_key: string}


def _get_search_parameters(search_term: str, kind: Optional[str]) -> Dict[str, str]:
	assert kind in {'series', 'movie', None}
	parameters = {
		's': search_term
	}
	if kind is not None:
		parameters['Type'] = kind
	return parameters


def _get_season_parameters(series_id: str, index: int) -> Dict:
	parameters = {
		'i':      series_id,
		'Season': index
	}
	return parameters


def _parse_api_response(response: Dict, episode_format) -> Optional[MediaResource]:
	if _is_valid_response(response):
		# Not a media response. Usually due to an error
		result = _parse_media_response(response, episode_format)
		result = MediaResource(**result)
	else:
		result = None
	return result


def _parse_episode_response(episode: dict, season: int, previous: int) -> Union[
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

	Returns
	-------
	EpisodeResponse
	"""
	imdb_rating = to_number(episode.get('imdbRating', ' N/A'))
	release_date = _convert_to_timestamp(episode['Released'])
	episode_id = "S{:>02}E{:>02}".format(season, episode['Episode'])
	episode_index = previous + int(episode['Episode'])

	episode_data = dict(
		title = episode['Title'],
		imdbId = episode['imdbID'],
		imdbRating = float(imdb_rating),
		releaseDate = release_date,
		episodeId = episode_id,
		indexInSeries = episode_index,
		indexInSeason = to_number(episode['Episode'])
	)

	episode_resource = EpisodeResource(**episode_data)
	return episode_resource


def _parse_media_response(api_response: Dict, episode_format: Optional[str]) -> Dict:
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
	imdb_votes = to_number(api_response['imdbVotes'].replace(',', ''))
	imdb_rating = to_number(api_response['imdbRating'])

	api_response_status = api_response['Response'] == 'True'
	# years = api_response['Year'].split('-')
	years = api_response['Year']
	release_date = api_response['Released']
	release_date = _convert_to_timestamp(release_date)

	runtime = _convert_to_duration(api_response['Runtime'])
	metacritic_score = to_number(api_response['Metascore'])

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
	if media_type == 'series' and episode_format:
		total_seasons = to_number(api_response['totalSeasons'])

		series_seasons = get_seasons(imdb_id, episode_format = episode_format)

		parsed_response['totalSeasons'] = total_seasons
		parsed_response['seasons'] = series_seasons
	else:
		parsed_response['seasons'] = []

	return parsed_response


def _parse_search_response(response: Dict) -> Optional[Dict]:
	status = response['Response'] == 'True'
	if status:
		total_results = int(response['totalResults'])
		response['Response'] = status
		response['totalResults'] = total_results
	else:
		response = None
	return response


def _parse_season_response(response: Dict, previous_episodes: int) -> Optional[SeasonResource]:
	response_status = response.get('Response', 'False') == 'True'
	if response_status:
		season_number = response['Season']
		season_episodes = [
			_parse_episode_response(episode, season_number, previous_episodes) for episode in response['Episodes']
		]

		season_result = SeasonResource(
			episodes = season_episodes,
			seasonIndex = season_number,
			length = len(season_episodes),
			seriesTitle = response['Title']
		)
	else:
		season_result = None
	return season_result


def search(string: str, kind: Optional[str] = None) -> Dict:
	"""
		Searches the api for a string.
	Parameters
	----------
	string
	kind: {'series', 'movie', None}
		Assumes both if `None`

	Returns
	-------
	SearchResource: dict
		-`Response`: bool
		-`Search`: list<Dict>
			- `Poster`: url
			- `Title`: str
			- `Type`: {'series', 'movie'}
			- `Year`: str
			- `imdbID`: str
		- `totalResults`: int
	"""
	parameters = _get_search_parameters(string, kind)
	response = request(**parameters)
	result = _parse_search_response(response)
	return result


def find(string: str, kind: str = 'series', **kwargs) -> Optional[MediaResource]:
	"""
		Searches the api for a show title and returns the first result.
	Parameters
	----------
	string: str
		The search term.
	kind: {`series`, `movie`, `any`}; default `any`

	Keyword Arguments:
	- episode_format: {`short`, `long`}; default `short`

	Returns
	-------
	Optional[MediaResource]
	"""
	kwargs['episode_format'] = kwargs.get('episode_format', 'short')
	if _is_imdb_id(string):
		result = get(string, **kwargs)
	else:
		search_response = search(string, kind)
		if not search_response:
			result = None
		else:
			first_result = search_response['Search'][0]
			first_result_id = first_result['imdbID']
			result = get(first_result_id, **kwargs)
	return result


def get_seasons(series_id: str, episode_format: str = 'short') -> List[SeasonResource]:
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
	if not episode_format: return []
	seasons = list()
	previous_episodes = 0
	for index in range(1, 100):  # There shouldn't be more than 100 seasons.
		response = request(**_get_season_parameters(series_id, index))
		season_result = _parse_season_response(response, previous_episodes)
		if season_result:
			seasons.append(season_result)
			previous_episodes += max((i.indexInSeason for i in season_result.episodes))
		else:
			break
	return seasons


def get(string: str, episode_format: Optional[str] = None, asdict = False, **kwargs) -> MediaResource:
	"""
		Sends a request to the OMDB API and parses the result. Using a raw title string may result in a similar,
		but incorrect media.
		Parameters
		----------
		string: str
			One of the following:
			-`i`: IMDB ID
			-`s`: Search term
		episode_format: {None, 'short', 'full'}; default None
			- `None`: Do not include seasons.
			- `short`: Retrieve short-form episodes
			- `long`: Retrieve long-form episodes.
		asdict: bool; default False
			Return the response from the api as a dict rather than a resource.
		Returns
		-------
		MediaResponse
	"""

	response = request(**_get_request_parameters(string, episode_format))
	result = _parse_api_response(response, episode_format)

	return result


def request(**parameters) -> Dict:
	parameters['apikey'] = API_KEY
	url = "http://www.omdbapi.com/"
	response = requests.get(url, parameters)
	response = response.json()
	return response


if __name__ == "__main__":
	term = "Legion"
	_result = find(term, episode_format = 'long')
	print(_result.toTable().to_string())
