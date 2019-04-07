import pytest
from typing import Dict
import datetime
from omdbapi.api import apiparsers
from omdbapi.api.resources import MiniEpisodeResource


@pytest.fixture
def response_show() -> Dict:
	data = {
		'Actors':       'Kiernan Shipka, Ross Lynch, Lucy Davis, Chance Perdomo',
		'Awards':       'N/A',
		'Country':      'USA',
		'Director':     'N/A',
		'Genre':        'Drama, Fantasy, Horror, Mystery, Thriller',
		'Language':     'English',
		'Metascore':    '74',
		'Plot':         'As her 16th birthday nears, Sabrina must choose between the witch '
						'world of her family and the human world of her friends. Based on the '
						'Archie comic.',
		'Poster':       'https://m.media-amazon.com/images/M/MV5BMTg3MjY1MDUxMV5BMl5BanBnXkFtZTgwMzczNTU2NzM@._V1_SX300.jpg',
		'Rated':        'TV-14',
		'Ratings':      [{'Source': 'Internet Movie Database', 'Value': '7.8/10'}],
		'Released':     '26 Oct 2018',
		'Response':     'True',
		'Runtime':      '60 min',
		'Title':        'Chilling Adventures of Sabrina',
		'Type':         'series',
		'Writer':       'Roberto Aguirre-Sacasa',
		'Year':         '2018–',
		'imdbID':       'tt7569592',
		'imdbRating':   '7.8',
		'imdbVotes':    '39,297',
		'totalSeasons': '2'
	}
	return data


@pytest.fixture
def response_movie() -> Dict:
	data = {
		'Actors':     'Johnny Depp, Geoffrey Rush, Orlando Bloom, Keira Knightley',
		'Awards':     'Nominated for 5 Oscars. Another 36 wins & 96 nominations.',
		'BoxOffice':  '$305,343,252',
		'Country':    'USA',
		'DVD':        '02 Dec 2003',
		'Director':   'Gore Verbinski',
		'Genre':      'Action, Adventure, Fantasy',
		'Language':   'English',
		'Metascore':  '63',
		'Plot':       'Blacksmith Will Turner teams up with eccentric pirate "Captain" Jack '
					  "Sparrow to save his love, the governor's daughter, from Jack's "
					  'former pirate allies, who are now undead.',
		'Poster':     'https://m.media-amazon.com/images/M/MV5BNGYyZGM5MGMtYTY2Ni00M2Y1LWIzNjQtYWUzM2VlNGVhMDNhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
		'Production': 'Buena Vista Pictures',
		'Rated':      'PG-13',
		'Ratings':    [{'Source': 'Internet Movie Database', 'Value': '8.0/10'},
			{'Source': 'Metacritic', 'Value': '63/100'}],
		'Released':   '09 Jul 2003',
		'Response':   'True',
		'Runtime':    '143 min',
		'Title':      'Pirates of the Caribbean: The Curse of the Black Pearl',
		'Type':       'movie',
		'Website':    'https://pirates.disney.com/pirates-of-the-caribbean-the-curse-of-the-black-pearl',
		'Writer':     'Ted Elliott (screen story), Terry Rossio (screen story), Stuart '
					  'Beattie (screen story), Jay Wolpert (screen story), Ted Elliott '
					  '(screenplay), Terry Rossio (screenplay)',
		'Year':       '2003',
		'imdbID':     'tt0325980',
		'imdbRating': '8.0',
		'imdbVotes':  '955,774'
	}
	return data


@pytest.fixture
def response_season() -> Dict:
	data = {
		'Episodes':     [
			{
				'Episode':    '1',
				'Released':   '2018-10-26',
				'Title':      'Chapter One: October Country',
				'imdbID':     'tt7584356',
				'imdbRating': '7.8'
			},
			{
				'Episode':    '10',
				'Released':   '2018-10-26',
				'Title':      'Chapter Ten: The Witching Hour',
				'imdbID':     'tt7697928',
				'imdbRating': '8.7'
			}
		],
		'Response':     'True',
		'Season':       '2',
		'Title':        'Chilling Adventures of Sabrina',
		'totalSeasons': '2'
	}
	return data


def test_parse_media_response_series(response_show):
	expected = {
		'actors':         ['Kiernan Shipka', 'Ross Lynch', 'Lucy Davis', 'Chance Perdomo'],
		'awards':         'N/A',
		'country':        'USA',
		'director':       'N/A',
		'genres':         ['Drama', 'Fantasy', 'Horror', 'Mystery', 'Thriller'],
		'language':       'English',
		'plot':           'As her 16th birthday nears, Sabrina must choose between the witch '
						  'world of her family and the human world of her friends. Based on the '
						  'Archie comic.',
		'poster':         'https://m.media-amazon.com/images/M/MV5BMTg3MjY1MDUxMV5BMl5BanBnXkFtZTgwMzczNTU2NzM@._V1_SX300.jpg',
		'rated':          'TV-14',
		'ratings':        [
			{'source': 'Internet Movie Database', 'rating': 78, 'votes': 39297}
		],
		'releaseDate':    datetime.datetime(year = 2018, month = 10, day = 26),  # '26 Oct 2018',
		'responseStatus': True,
		'duration':       datetime.timedelta(minutes = 60),  # '60 min',
		'title':          'Chilling Adventures of Sabrina',
		'type':           'series',
		'writer':         'Roberto Aguirre-Sacasa',
		'imdbId':         'tt7569592',
		'years':          (2018, None),
		'totalSeasons':   2,
		'website':        None,
		'episodes': []
	}
	result = apiparsers._parse_series_response(response_show)
	assert result['ratings'] == expected['ratings']
	assert result == expected


def test_parse_media_response_film(response_movie):
	expected = {
		'actors':          ['Johnny Depp', 'Geoffrey Rush', 'Orlando Bloom', 'Keira Knightley'],
		'awards':          'Nominated for 5 Oscars. Another 36 wins & 96 nominations.',
		'boxOffice':       305343252,
		'country':         'USA',
		'releaseDateHome': datetime.datetime(2003, 12, 2),  # '02 Dec 2003',
		'director':        'Gore Verbinski',
		'genres':          ['Action', 'Adventure', 'Fantasy'],
		'language':        'English',
		'plot':            'Blacksmith Will Turner teams up with eccentric pirate "Captain" Jack '
						   "Sparrow to save his love, the governor's daughter, from Jack's "
						   'former pirate allies, who are now undead.',
		'poster':          'https://m.media-amazon.com/images/M/MV5BNGYyZGM5MGMtYTY2Ni00M2Y1LWIzNjQtYWUzM2VlNGVhMDNhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
		'production':      'Buena Vista Pictures',
		'rated':           'PG-13',
		'ratings':         [
			{'source': 'Internet Movie Database', 'rating': 80, 'votes': 955774},
			{'source': 'Metacritic', 'rating': 63}
		],
		'releaseDate':     datetime.datetime(2003, 7, 9),
		'responseStatus':  True,
		'duration':        datetime.timedelta(minutes = 143),
		'title':           'Pirates of the Caribbean: The Curse of the Black Pearl',
		'type':            'movie',
		'website':         'https://pirates.disney.com/pirates-of-the-caribbean-the-curse-of-the-black-pearl',
		'writer':          'Ted Elliott (screen story), Terry Rossio (screen story), Stuart '
						   'Beattie (screen story), Jay Wolpert (screen story), Ted Elliott '
						   '(screenplay), Terry Rossio (screenplay)',
		'year':            2003,
		'imdbId':          'tt0325980'
	}
	result = apiparsers._parse_film_response(response_movie)

	assert result == expected


def test_parse_api_response(response_show, response_movie):
	result_series = apiparsers.parse_api_response(response_show)
	assert result_series.__class__.__name__.split('.')[0] == 'SeriesResource'

	result_film = apiparsers.parse_api_response(response_movie)
	assert result_film.__class__.__name__.split('.')[0] == 'FilmResource'


def test_parse_miniepisode_response():
	test_input = {
		'Episode':    '5',
		'Released':   '2018-10-26',
		'Title':      'Chapter Five: Dreams in a Witch House',
		'imdbID':     'tt7697934',
		'imdbRating': '7.7'
	}
	expected_response = {
		'episodeId': 'S01E05',
		'title': 'Chapter Five: Dreams in a Witch House',
		'imdbId': 'tt7697934',
		'releaseDate': datetime.datetime(2018,10,26),
		'imdbRating': 7.7,
		'seasonIndex': 1,
		'indexInSeason': 5,
		'indexInSeries': 5
	}
	result = apiparsers._parse_miniepisode_response(test_input, 1, 0)
	assert result == expected_response

def test_parse_season_response(response_season):
	expected_result = [
		MiniEpisodeResource(
			title = 'Chapter One: October Country',
			releaseDate  = datetime.datetime(2018,10,26),
			imdbId = 'tt7584356',
			imdbRating = 7.8,
			seasonIndex = 2,
			episodeId = "S02E01",
			indexInSeason = 1,
			indexInSeries = 12
		),
		MiniEpisodeResource(
			title = 'Chapter Ten: The Witching Hour',
			releaseDate  = datetime.datetime(2018,10,26),
			imdbId = 'tt7697928',
			imdbRating = 8.7,
			seasonIndex = 2,
			episodeId = "S02E10",
			indexInSeason = 10,
			indexInSeries = 21
		)
	]

	result  = apiparsers.parse_season_response(response_season, previous_episodes = 11)
	from dataclasses import asdict
	assert asdict(result[0]) == asdict(expected_result[0])
	assert result == expected_result





