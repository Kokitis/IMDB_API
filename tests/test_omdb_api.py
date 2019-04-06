import pytest
from typing import Dict
from pytools.timetools import Duration
import datetime
from omdbapi import omdb_api
import math


@pytest.fixture
def response_show() -> Dict:
	data = {
		'Actors':       ['Kiernan Shipka', 'Ross Lynch', 'Lucy Davis', 'Chance Perdomo'],
		'Awards':       'N/A',
		'Country':      'USA',
		'Director':     'N/A',
		'Genre':        'Drama, Fantasy, Horror, Mystery, Thriller',
		'Language':     'English',
		'Metascore':    'N/A',
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
		'totalSeasons': '2',
		'metascore':    math.nan
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


def test_parse_media_response(response_show):
	expected = {
		'actors':         'Kiernan Shipka, Ross Lynch, Lucy Davis, Chance Perdomo',
		'awards':         'N/A',
		'country':        'USA',
		'director':       'N/A',
		'genres':         ['Drama', 'Fantasy', 'Horror', 'Mystery', 'Thriller'],
		'language':       'English',
		'metascore':      math.nan,
		'plot':           'As her 16th birthday nears, Sabrina must choose between the witch '
						  'world of her family and the human world of her friends. Based on the '
						  'Archie comic.',
		'poster':         'https://m.media-amazon.com/images/M/MV5BMTg3MjY1MDUxMV5BMl5BanBnXkFtZTgwMzczNTU2NzM@._V1_SX300.jpg',
		'rating':         'TV-14',
		'ratings':        [{'Source': 'Internet Movie Database', 'Value': '7.8/10'}],
		'releaseDate':    datetime.datetime(year = 2018, month = 10, day = 26),  # '26 Oct 2018',
		'responseStatus': True,
		'duration':       datetime.timedelta(minutes = 60),  # '60 min',
		'title':          'Chilling Adventures of Sabrina',
		'type':           'series',
		'writer':         'Roberto Aguirre-Sacasa',
		'year':           '2018–',
		'imdbId':         'tt7569592',
		'imdbRating':     7.8,
		'imdbVotes':      39297,
		# 'totalSeasons': 2,
		'seasons':        []
	}
	result = omdb_api._parse_media_response(response_show)

	assert result == expected
