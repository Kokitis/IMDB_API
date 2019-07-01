# from pytools import timetools, numbertools
from functools import partial
from pprint import pprint

pprint = partial(pprint, width = 150)
from typing import Union, Dict, Optional, List, Any
import datetime
from loguru import logger
# Import `MediaResource` for type-checking purposes
from omdbapi.api.resources import SeriesResource, FilmResource, MiniEpisodeResource
import pendulum
from infotools import numbertools, timetools

def parse_timestamp(string: str) -> pendulum.Date:
	# 08 Feb 2017]
	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	try:
		result = timetools.Timestamp(string)

	except:
		logger.error(f"Could not parse '{string}' as a timestamp.")
		result = None
	return result


def _parse_ratings(ratings: List[Dict[str, str]], votes: Optional[str] = None) -> List[Dict[str, Any]]:
	media_ratings = list()
	for r in ratings:
		source = r['Source']
		value = r['Value']
		converted_value = numbertools.to_number(value)
		# Check if the value was automatically converted to a percent.
		# For example, 7.8/10 would be converted to 0.78 rather than 7.8
		if converted_value < 1:
			converted_value *= 100
		data = {
			'source': r['Source'],
			'rating': numbertools.to_number(converted_value)
		}
		if source == 'Internet Movie Database' and votes:
			data['votes'] = numbertools.to_number(votes)

		media_ratings.append(data)
	return media_ratings


def _parse_episode_response(api_response: Dict) -> Dict:
	parsed_media_response = _parse_media_response(api_response)

	parsed_media_response['seriesId'] = api_response['seriesID']
	parsed_media_response['indexInSeason'] = numbertools.to_number(api_response['Episode'])
	parsed_media_response['seasonIndex'] = numbertools.to_number(api_response['Season'])

	return parsed_media_response


def _parse_series_response(api_response: Dict) -> Dict:
	parsed_media_response = _parse_media_response(api_response)

	# Parse the air date
	left, right = api_response['Year'].split('–')  # '–' is not '-'
	left = numbertools.to_number(left)
	right = numbertools.to_number(right, None)

	parsed_media_response['years'] = (left, right)
	parsed_media_response['totalSeasons'] = numbertools.to_number(api_response['totalSeasons'])
	parsed_media_response['episodes'] = []
	return parsed_media_response


def _parse_film_response(api_response: Dict) -> Dict:
	parsed_media_response = _parse_media_response(api_response)

	parsed_media_response['boxOffice'] = numbertools.to_number(api_response['BoxOffice'][1:])
	parsed_media_response['releaseDateHome'] = parse_timestamp(api_response['DVD'])
	parsed_media_response['year'] = numbertools.to_number(api_response['Year'])
	parsed_media_response['production'] = api_response.get('Production')
	return parsed_media_response


def _parse_media_response(api_response: Dict) -> Dict:
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
		api_response.get('imdbVotes'),
	)
	duration = pendulum.Duration(minutes = int(api_response['Runtime'].split(' ')[0]))
	duration.nanosecond = 0
	parsed_response = {
		'actors':         api_response['Actors'].split(', '),
		'awards':         api_response['Awards'],
		'country':        api_response['Country'],
		'director':       api_response['Director'],
		'genres':         api_response['Genre'].split(', '),
		'language':       api_response['Language'],
		'plot':           api_response['Plot'],
		'poster':         api_response['Poster'],
		'rated':          api_response['Rated'],
		'ratings':        media_ratings,
		'title':          api_response['Title'],
		'type':           media_type,
		'writer':         api_response['Writer'],
		'imdbId':         api_response['imdbID'],
		'responseStatus': api_response['Response'] == 'True',
		'releaseDate':    parse_timestamp(api_response['Released']),
		'duration':       duration,
		'website':        api_response.get('Website')
	}

	return parsed_response


def parse_search_response(response: Dict) -> Optional[Dict]:
	status = response['Response'] == 'True'
	if status:
		total_results = int(response['totalResults'])
		response['Response'] = status
		response['totalResults'] = total_results
	else:
		response = None
	return response


def _parse_miniepisode_response(episode: Dict[str, str], season: int = 0, previous_episodes: int = 0) -> Dict:
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


def parse_season_response(response: Dict, previous_episodes: int) -> List[MiniEpisodeResource]:
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
		episode_data = MiniEpisodeResource(**parsed_episode)
		season_episodes.append(episode_data)

	return season_episodes


def parse_api_response(response: Dict) -> Union[SeriesResource, FilmResource]:
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
		result = SeriesResource(**parsed_response)
	elif response_type == 'movie':
		parsed_response = _parse_film_response(response)
		result = FilmResource(**parsed_response)
	else:
		message = f"Not a valid response type: {response_type}"
		raise ValueError(message)

	return result
