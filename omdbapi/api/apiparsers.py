# from pytools import timetools, numbertools
from functools import partial
from pprint import pprint
import math
pprint = partial(pprint, width = 150)
from typing import Union, Dict, Optional, List

from loguru import logger
# Import `MediaResource` for type-checking purposes
from omdbapi.api import resources, responses
import pendulum
from infotools import numbertools, timetools

#####################################################################################################################
##################################################### Utilities #####################################################
#####################################################################################################################


def parse_timestamp(string: str) -> pendulum.Date:
	# 08 Feb 2017]
	try:
		result = timetools.Timestamp(string).date()
	except:
		logger.error(f"Could not parse '{string}' as a timestamp.")
		result = None
	return result

def _split_list(string:str, delimiter = ',', lower: bool = False)->List[str]:
	""" Splits a string into individual elements while removing whitespace.
		It also converts the elements to lowercase if `lower` is True. If
		`string` is 'N/A', an empty list is returned.
	"""
	values = [i.strip() for i in string.split(delimiter)]
	values = [i for i in values if i != 'N/A']
	if lower:
		values = [i.lower() for i in values]
	return values
def _parse_ratings(ratings: List[Dict[str, str]], ) -> List[Dict[str, str]]:
	media_ratings = list()
	for r in ratings:
		source = r['Source']
		value = r['Value']
		data = {
			'source': source,
			'value': value
		}
		media_ratings.append(data)
	return media_ratings

#####################################################################################################################
################################################ Media Parsers ######################################################
#####################################################################################################################

def _parse_episode_response(api_response: Dict) -> Dict:
	parsed_media_response = _parse_media_response(api_response)

	parsed_media_response['seriesId'] = api_response['seriesID']
	parsed_media_response['indexInSeason'] = numbertools.to_number(api_response['Episode'])
	parsed_media_response['seasonIndex'] = numbertools.to_number(api_response['Season'])

	return parsed_media_response


def _parse_series_response(api_response: Dict) -> resources.SeriesResource:
	parsed_media_response = _parse_media_response(api_response)

	#parsed_media_response['years'] = (left, right)
	parsed_media_response['totalSeasons'] = numbertools.to_number(api_response['totalSeasons'])
	parsed_media_response['episodes'] = []
	return parsed_media_response


def _parse_film_response(api_response: Dict) -> resources.MovieResource:
	parsed_media_response = _parse_media_response(api_response)
	box_office = numbertools.to_number(api_response['BoxOffice'][1:])
	if not math.isnan(box_office): box_office = int(box_office)
	parsed_media_response['boxOffice'] = box_office
	parsed_media_response['releaseDateHome'] = parse_timestamp(api_response['DVD'])
	#parsed_media_response['year'] = numbertools.to_number(api_response['Year'])
	parsed_media_response['production'] = api_response.get('Production')
	return parsed_media_response


def _parse_media_response(api_response: Dict) -> resources.MediaResource:
	"""
	Parses the fields common between Series and Films.
	Parameters
	----------
	api_response: Dict
		The raw response from the OMDB API.

	Returns
	-------
	MediaResponse
	"""
	media_type = api_response['Type']

	# parse the ratings for this media source.

	media_ratings = _parse_ratings(
		api_response['Ratings'],
	)
	runtime = api_response['Runtime']
	if runtime == 'N/A':
		duration = None
	else:
		logger.debug(f"Runtime: '{runtime}'")
		duration = pendulum.Duration(minutes = int(api_response['Runtime'].split(' ')[0]))
		duration.nanosecond = 0
	parsed_response = {
		'actors':         api_response['Actors'].split(', '),
		'awards':         api_response['Awards'],
		'countries':      _split_list(api_response['Country']),
		'director':       api_response['Director'],
		'genres':         _split_list(api_response['Genre'], lower = True),
		'languages':      _split_list(api_response['Language'], lower = True),
		'plot':           api_response['Plot'],
		'poster':         api_response['Poster'],
		'rated':          api_response['Rated'],
		'ratings':        media_ratings,
		'title':          api_response['Title'],
		'type':           media_type,
		'writers':        _split_list(api_response['Writer']),
		'imdbId':         api_response['imdbID'],
		'imdbRating':	float(api_response['imdbRating']),
		'imdbVotes': 	int(numbertools.to_number(api_response['imdbVotes'])),
		'releaseDate':    parse_timestamp(api_response['Released']),
		'runtime':       duration,
	}

	return parsed_response

#####################################################################################################################
################################################## Other Parsers ####################################################
#####################################################################################################################

def parse_search_response(response: responses.SearchResponse) -> Optional[Dict]:
	status = response['Response'] == 'True'
	if status:
		total_results = int(response['totalResults'])
		response['Response'] = status
		response['totalResults'] = total_results
	else:
		response = None
	return response


def _parse_miniepisode_response(episode: responses.SeasonItem, season: int = 0, previous_episodes: int = 0) -> resources.MiniEpisodeResource:
	"""
		Converts the episode response from the API into either a `MediaResource` or `EpisodeResource` object.
	Parameters
	----------
	episode: Dict[str,str]
		The short-form response from the api.
	season: int
		The index of the season containing the episode.
	previous_episodes:int
		Number of episodes occuring in the season prior to this one. Used to determine the episode number and the episode label.

	Returns
	-------
	EpisodeResponse
	"""
	index_in_season = int(numbertools.to_number(episode['Episode']))
	episode_id = f"S{season:>02}E{index_in_season:>02}"
	index_in_series = index_in_season + previous_episodes
	data = {
		'episodeId':     episode_id,
		'title':         episode['Title'],
		'releaseDate':   parse_timestamp(episode['Released']),
		'imdbId':        episode['imdbID'],
		'imdbRating':    numbertools.to_number(episode['imdbRating']),
		'seasonIndex':   season,
		'indexInSeason': index_in_season,
		'indexInSeries': index_in_series
	}
	return data


def parse_season_response(response: responses.SeasonResponse, previous_episodes: int) -> List[resources.MiniEpisodeResource]:
	"""
		Converts a season response from the API into a list of `MiniEpisodeResource` objects representing all episodes in the season.
	Parameters
	----------
	response: Dict
		The raw response from the `Season` endpoint
	previous_episodes: int
		Used to calculate the index of each episode within each season.

	Returns
	-------
	List[MiniEpisode]
	"""

	season_index = int(numbertools.to_number(response['Season']))

	season_episodes = list()
	for episode in response['Episodes']:
		parsed_episode = _parse_miniepisode_response(episode, season_index, previous_episodes)
		season_episodes.append(parsed_episode)

	return season_episodes


def parse_api_response(response: Dict[str,str]) -> Union[resources.SeriesResource, resources.MovieResource]:
	""" Converts a raw api response into a `MediaResource` object.

		Parameters
		----------
		response: Dict[str,str]
			The raw json-formatted response from the api.
	"""

	# Not a media response. Usually due to an error
	response_type = response['Type']
	if response_type == 'series':
		parsed_response = _parse_series_response(response)
	elif response_type == 'movie':
		parsed_response = _parse_film_response(response)
	else:
		message = f"Not a valid response type: {response_type}"
		raise ValueError(message)

	return parsed_response

