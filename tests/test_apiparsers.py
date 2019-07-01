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


@pytest.fixture
def response_episode() -> Dict:
	data = {
		'Actors':     'Kiernan Shipka, Ross Lynch, Lucy Davis, Chance Perdomo',
		'Awards':     'N/A',
		'Country':    'USA',
		'Director':   'Lee Toland Krieger',
		'Episode':    '1',
		'Genre':      'Drama, Fantasy, Horror, Mystery, Thriller',
		'Language':   'English',
		'Metascore':  'N/A',
		'Plot':       'While Greendale readies for a Halloween eclipse, Sabrina faces a crucial decision and Harvey makes an unexpected declaration.',
		'Poster':     'https://m.media-amazon.com/images/M/MV5BMjM4OTA4ODk2MF5BMl5BanBnXkFtZTgwODkwMjUzNjM@._V1_SX300.jpg',
		'Rated':      'N/A',
		'Ratings':    [{'Source': 'Internet Movie Database', 'Value': '7.8/10'}],
		'Released':   '26 Oct 2018',
		'Response':   'True',
		'Runtime':    '62 min',
		'Season':     '1',
		'Title':      'Chapter One: October Country',
		'Type':       'episode',
		'Writer':     'Roberto Aguirre-Sacasa (developed by), Roberto Aguirre-Sacasa',
		'Year':       '2018',
		'imdbID':     'tt7584356',
		'imdbRating': '7.8',
		'imdbVotes':  '1735',
		'seriesID':   'tt7569592'
	}
	return data


@pytest.fixture
def search_response():
	data = {
		'Response':     'True',
		'Search':       [
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BNjk0ZjEzNGEtOTg5Yy00ZTU3LWE1NTQtNWI4MTJmMTlkMTVhXkEyXkFqcGdeQXVyNDc0NDgwODI@._V1_SX300.jpg',
				'Title':  'The 100',
				'Type':   'series',
				'Year':   '2014–',
				'imdbID': 'tt2661044'
			},
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BNDUyMzU5MTk5MF5BMl5BanBnXkFtZTgwNjcxNDQxNTE@._V1_SX300.jpg',
				'Title':  'The 100 Year-Old Man Who Climbed Out the Window and Disappeared',
				'Type':   'movie',
				'Year':   '2013',
				'imdbID': 'tt2113681'
			},
			{'Poster': 'N/A', 'Title': 'The 100 Scariest Movie Moments', 'Type': 'series', 'Year': '2004–', 'imdbID': 'tt0450892'},
			{
				'Poster': 'https://ia.media-imdb.com/images/M/MV5BMTcyNTE3NzU0NF5BMl5BanBnXkFtZTcwOTU0MzIyOA@@._V1_SX300.jpg',
				'Title':  '100 Ghost Street: The Return of Richard Speck',
				'Type':   'movie',
				'Year':   '2012',
				'imdbID': 'tt2297108'
			},
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BNGUyMDE2ZjUtYjgzOC00NjNlLThkZDUtOTM5NWM5YTgxZTBmXkEyXkFqcGdeQXVyMTA5MTg3NzY@._V1_SX300.jpg',
				'Title':  '100 Years at the Movies',
				'Type':   'movie',
				'Year':   '1994',
				'imdbID': 'tt0179624'
			},
			{
				'Poster': 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTM4MzY2OTE3M15BMl5BanBnXkFtZTYwMjA0MTU5._V1_SX300.jpg',
				'Title':  'The Second 100 Years',
				'Type':   'movie',
				'Year':   '1927',
				'imdbID': 'tt0018368'
			},
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BMTkxMjM2MTUxN15BMl5BanBnXkFtZTcwNDQyNTMyMQ@@._V1_SX300.jpg',
				'Title':  '100 Days Before the Command',
				'Type':   'movie',
				'Year':   '1991',
				'imdbID': 'tt0100694'
			},
			{
				'Poster': 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTcwOTc1OTkwOF5BMl5BanBnXkFtZTcwNTg0MDEyMQ@@._V1_SX300.jpg',
				'Title':  "Having Our Say: The Delany Sisters' First 100 Years",
				'Type':   'movie',
				'Year':   '1999',
				'imdbID': 'tt0196603'
			},
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BNDU5MTMxMjI3M15BMl5BanBnXkFtZTgwOTcyMzUxNzE@._V1_SX300.jpg',
				'Title':  '100 Days in the Jungle',
				'Type':   'movie',
				'Year':   '2002',
				'imdbID': 'tt0303580'
			},
			{
				'Poster': 'https://m.media-amazon.com/images/M/MV5BMTQ5NDgzMjQ1MV5BMl5BanBnXkFtZTgwMzg3NzM5NTE@._V1_SX300.jpg',
				'Title':  'The 100 Years Show',
				'Type':   'movie',
				'Year':   '2015',
				'imdbID': 'tt3861876'
			}],
		'totalResults': '148'
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
		'episodes':       []
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
		'episodeId':     'S01E05',
		'title':         'Chapter Five: Dreams in a Witch House',
		'imdbId':        'tt7697934',
		'releaseDate':   datetime.datetime(2018, 10, 26),
		'imdbRating':    7.7,
		'seasonIndex':   1,
		'indexInSeason': 5,
		'indexInSeries': 5
	}
	result = apiparsers._parse_miniepisode_response(test_input, 1, 0)
	assert result == expected_response


def test_parse_season_response(response_season):
	expected_result = [
		MiniEpisodeResource(
			title = 'Chapter One: October Country',
			releaseDate = datetime.datetime(2018, 10, 26),
			imdbId = 'tt7584356',
			imdbRating = 7.8,
			seasonIndex = 2,
			episodeId = "S02E01",
			indexInSeason = 1,
			indexInSeries = 12
		),
		MiniEpisodeResource(
			title = 'Chapter Ten: The Witching Hour',
			releaseDate = datetime.datetime(2018, 10, 26),
			imdbId = 'tt7697928',
			imdbRating = 8.7,
			seasonIndex = 2,
			episodeId = "S02E10",
			indexInSeason = 10,
			indexInSeries = 21
		)
	]

	result = apiparsers.parse_season_response(response_season, previous_episodes = 11)
	from dataclasses import asdict
	assert asdict(result[0]) == asdict(expected_result[0])
	assert result == expected_result


def test_parse_episode_resposne(response_episode):
	expected = {
		'actors':        ['Kiernan Shipka', 'Ross Lynch', 'Lucy Davis', 'Chance Perdomo'],
		'awards':        'N/A',
		'country':       'USA',
		'director':      'Lee Toland Krieger',
		'genres':        ['Drama', 'Fantasy', 'Horror', 'Mystery', 'Thriller'],
		'language':      'English',
		'plot':          'While Greendale readies for a Halloween eclipse, Sabrina faces a crucial decision and Harvey makes an unexpected declaration.',
		'poster':        'https://m.media-amazon.com/images/M/MV5BMjM4OTA4ODk2MF5BMl5BanBnXkFtZTgwODkwMjUzNjM@._V1_SX300.jpg',
		'rated':         'N/A',
		'ratings':       [{'source': 'Internet Movie Database', 'rating': 78, 'votes': 1735}],
		'releaseDate':      datetime.datetime(2018, 10, 26),  # '26 Oct 2018',
		'responseStatus':      True,
		'duration':       datetime.timedelta(minutes = 62),  # '62 min',
		'seasonIndex':   1,
		'indexInSeason': 1,
		'title':         'Chapter One: October Country',
		'type':          'episode',
		'writer':        'Roberto Aguirre-Sacasa (developed by), Roberto Aguirre-Sacasa',
		'imdbId':        'tt7584356',
		'seriesId':      'tt7569592',
		'website': None
	}

	result = apiparsers._parse_episode_response(response_episode)

	assert expected == result
