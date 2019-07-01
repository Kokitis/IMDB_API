from functools import partial
from pprint import pprint

pprint = partial(pprint, width = 150)
import requests
from typing import Dict, Optional, List, Union
from loguru import logger
try:
	from omdbapi.github import omdb_api_key
	# Import `MediaResource` for type-checking purposes
	from omdbapi.api.resources import SeriesResource, FilmResource, MiniEpisodeResource
	from omdbapi.api.widgets import _is_imdb_id
	from omdbapi.api import apiparsers
except ModuleNotFoundError:
	from ..github import omdb_api_key
	from .resources import SeriesResource, FilmResource, MiniEpisodeResource
	from .widgets import _is_imdb_id
	from . import apiparsers

API_KEY = omdb_api_key


def _is_valid_response(response: Dict) -> bool:
	""" Checks if a given response is successfull."""
	return response['Response'] == 'True'


def _get_request_parameters(string: str) -> Dict[str, str]:
	""" Returns the basic parameters needed for an API request."""
	_key = 'i' if _is_imdb_id(string) else 't'
	return {_key: string}


def _get_search_parameters(search_term: str, kind: Optional[str] = None) -> Dict[str, str]:
	"""
	Returns the API parameters when sending a search request.

	Parameters
	----------
	search_term: str
		The string to search for.
	kind: {'series', 'movie'}
		Indicates what type of content to search for. A value of `None` will search for any and all media.

	Returns
	-------
	Dict
		A dictionary with the basic parameters needed to send a search request.
	"""
	assert kind in {'series', 'movie', None}
	parameters = {
		's': search_term
	}
	if kind is not None:
		parameters['Type'] = kind
	return parameters


def _get_season_parameters(series_id: str, index: int) -> Dict:
	"""
		Returns API parameters required when getting information about a series season.
	Parameters
	----------
	series_id:str
	index:int
		The season number.

	Returns
	-------

	"""
	parameters = {
		'i':      series_id,
		'Season': index
	}
	return parameters


def search(string: str, kind: Optional[str] = None) -> Dict:
	"""
		Searches the api for a string.
	Parameters
	----------
	string:str
		The search term to include in the request.
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
	result = apiparsers.parse_search_response(response)
	return result

def find(string: str, kind: str = 'series') -> Union[None,SeriesResource, FilmResource]:
	"""
		Searches the api for a show title and returns the first result.

	Parameters
	----------
	string: str
		The search term.
	kind: str; default `any`
		Should be one of {`series`, `movie`, `any`}

	Keyword Arguments
	-----------------
	- episode_format: {`short`, `long`}; default `short`

	Returns
	-------
	Optional[MediaResource]
		The MediaResource object.
	"""
	if _is_imdb_id(string):
		result = get(string)
	else:
		search_response = search(string, kind)
		if not search_response:
			result = None
		else:
			first_result = search_response['Search'][0]
			first_result_id = first_result['imdbID']
			result = get(first_result_id)
	return result


def get_seasons(series_id: str) -> List[MiniEpisodeResource]:
	"""
		Gathers all episodes for the given series.
	Parameters
	----------
	series_id: str

	Returns
	-------

	"""
	series_episodes = list()
	previous_episodes = 0
	for index in range(1, 100):  # There shouldn't be more than 100 seasons.
		response = request(**_get_season_parameters(series_id, index))
		if _is_valid_response(response):
			season_episodes = apiparsers.parse_season_response(response, previous_episodes)

			if season_episodes:
				series_episodes += season_episodes
				previous_episodes += max((i.indexInSeason for i in season_episodes))
			else:
				break
		else:
			break
	return series_episodes


def get(string: str) -> Union[FilmResource, SeriesResource]:
	"""
		Sends a request to the OMDB API and parses the result. Using a raw title string may result in a similar,
		but incorrect media.
		Parameters
		----------
		string: str
			One of the following:
			-`i`: IMDB ID
			-`s`: Search term
		Returns
		-------
		MediaResponse
	"""

	response = request(**_get_request_parameters(string))
	result = apiparsers.parse_api_response(response)
	if result.type == 'series':
		result.episodes = get_seasons(result.imdbId)

	return result


def request(**parameters) -> Dict:
	"""Sends a request to the API"""
	parameters['apikey'] = API_KEY
	url = "http://www.omdbapi.com/"
	response = requests.get(url, parameters)
	response = response.json()
	return response


if __name__ == "__main__":
	term = 'tt7584356'
	_result = request(**_get_request_parameters(term))

	pprint(_result)
