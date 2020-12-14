from imdbapi.imdbapi import IMDBResponseParser
import pytest
from pathlib import Path
import json
import pendulum
import math
from infotools import timetools

folder_data = Path(__file__).parent / "data_for_imdb_api" / "responses"
response_filenames = [
	folder_data / "sample_response_episode_angels_take_manhattan.json",
	folder_data / "sample_response_episode_sozins_comet.json",
	folder_data / "sample_response_episode_umbrella_s03e02.json",

	folder_data / "sample_response_movie_a_new_hope.json",
	folder_data / "sample_response_movie_avatar.json",
	folder_data / "sample_response_movie_avengers_endgame.json",

	folder_data / "sample_response_series_avatar.json",
	folder_data / "sample_response_series_kings.json",
	folder_data / "sample_response_series_umbrella.json"
]

responses = [json.loads(filename.read_text()) for filename in response_filenames]


resources = [
	{
		'actors':      ["Matt Smith", "Karen Gillan", 'Arthur Darvill', 'Alex Kingston'],
		'awards':      "N/A",
		'countries':   [],
		'director':    ["Nick Hurran"],
		'runtime':     pendulum.parse("PT44M"),
		'genres':      ['Adventure', 'Drama', 'Family', 'Mystery', 'Sci-Fi'],
		'imdbId':      "tt2378951",
		'imdbRating':  9.0,
		'imdbVotes':   7025,
		'languages':   [],
		'plot':        "The Angels Take Manhattan is an episode of Doctor Who starring Matt Smith, Karen Gillan, and Arthur Darvill. After Rory has an encounter with a weeping angel, the doctor and Amy travel to 1930's New York to save him, but they soon...",
		'poster':      "https://m.media-amazon.com/images/M/MV5BNjM0NTk2MTM2NF5BMl5BanBnXkFtZTcwMjgyNTQ1OA@@._V1_.jpg",
		'rated':       "TV-PG",
		'ratings':     [
			{
				"Source": "Internet Movie Database",
				"Value":  "9.0/10"
			}
		],
		'releaseDate': pendulum.parse("2012-09-29"),
		'tags':        ["weeping angel", "new york city", "eleventh doctor", "statue of liberty", "central park manhattan new york city"],
		'title':       "The Angels Take Manhattan",
		'type':        "episode",
		'writers':     []
	},
	{
		'actors':      ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher', 'Alec Guinness'],
		'awards':      "N/A",
		'countries':   [],
		'director':    ["George Lucas"],
		'runtime':     pendulum.parse("PT2H1M"),
		'genres':      ['Action', 'Adventure', 'Fantasy', 'Sci-Fi'],
		'imdbId':      "tt0076759",
		'imdbRating':  8.6,
		'imdbVotes':   1219511,
		'languages':   [],
		"plot": "Star Wars is a movie starring Mark Hamill, Harrison Ford, and Carrie Fisher. Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle...",
		'poster':      "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
		'rated':       "PG",
		'ratings':     [
			{
				"Source": "Internet Movie Database",
				"Value":  "8.6/10"
			}
		],
		'releaseDate': pendulum.parse("1977-05-25"),
		'tags':        ["rebellion","galactic war","space opera","princess" ,"droid"],
		'title':       "Star Wars",
		'type':        "movie",
		'writers':     []
	},
	{
		'actors':      ['Ian McShane', 'Christopher Egan', 'Susanna Thompson', 'Allison Miller'],
		'awards':      "N/A",
		'countries':   [],
		'director':    [],
		'runtime':     None,
		'genres':      ["Drama", "Sci-Fi"],
		'imdbId':      "tt1137462",
		'imdbRating':  8.2,
		'imdbVotes':   8102,
		'languages':   [],
		"plot": "Kings is a TV series starring Ian McShane, Christopher Egan, and Susanna Thompson. A modern day, alternate-reality drama about a hero who rises to become the King of his nation, based on the biblical story of King David.",
		'poster':      "https://m.media-amazon.com/images/M/MV5BOTcwNDQ4MDA1OF5BMl5BanBnXkFtZTcwMjYwOTQ3Mw@@._V1_.jpg",
		'rated':       "TV-14",
		'ratings':     [
			{
				"Source": "Internet Movie Database",
				"Value":  "8.2/10"
			}
		],
		'releaseDate': pendulum.parse("2009-03-15"),
		'tags':        ["king","crown prince","twin","fictional country","kingdom"],
		'title':       "Kings",
		'type':        "series",
		'writers':     []
	},
	{
		'actors':      ["Elliot Page", 'Aidan Gallagher', 'Robert Sheehan', 'Tom Hopper'],
		'awards':      "N/A",
		'countries':   [],
		'director':    [],
		'runtime':     None,
		'genres':      ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Sci-Fi"],
		'imdbId':      "tt13435916",
		'imdbRating':  math.nan,
		'imdbVotes':   0,
		'languages':   [],
		"plot":        "N/A",
		'poster':      "N/A",
		'rated':       "N/A",
		'ratings':     [],
		'releaseDate': None,
		'tags':        [],
		'title':       "Episode #3.2",
		'type':        "episode",
		'writers':     []
	}
]


def test_fix_dictionary_keys():
	sample_1 = {'@type': 'Person', 'name': 'Elliot Page', 'url': '/name/nm0680983/'}

	expected_1 = {
		'type': 'Person',
		'name': 'Elliot Page',
		'url':  '/name/nm0680983/'
	}

	sample_2 = {
		'@type':        'VideoObject',
		'description':  'Same weird family. New weird problems. The Umbrella Academy returns on July 31.',
		'embedUrl':     '/video/imdb/vi772128281',
		'name':         'Official Trailer',
		'thumbnail':    {
			'@type':      'ImageObject',
			'contentUrl': 'https://m.media-amazon.com/images/M/MV5BMjY2YmRkZjYtMjQ0NC00NTljLTlmYTUtMDhkOWMyZmIyYWQ5XkEyXkFqcGdeQWRvb2xpbmhk._V1_.jpg'
		},
		'thumbnailUrl': 'https://m.media-amazon.com/images/M/MV5BMjY2YmRkZjYtMjQ0NC00NTljLTlmYTUtMDhkOWMyZmIyYWQ5XkEyXkFqcGdeQWRvb2xpbmhk._V1_.jpg',
		'uploadDate':   '2020-07-08T15:24:44Z'
	}

	expected_2 = {
		'type':         'VideoObject',
		'description':  'Same weird family. New weird problems. The Umbrella Academy returns on July 31.',
		'embedUrl':     '/video/imdb/vi772128281',
		'name':         'Official Trailer',
		'thumbnail':    {
			'type':       'ImageObject',
			'contentUrl': 'https://m.media-amazon.com/images/M/MV5BMjY2YmRkZjYtMjQ0NC00NTljLTlmYTUtMDhkOWMyZmIyYWQ5XkEyXkFqcGdeQWRvb2xpbmhk._V1_.jpg'
		},
		'thumbnailUrl': 'https://m.media-amazon.com/images/M/MV5BMjY2YmRkZjYtMjQ0NC00NTljLTlmYTUtMDhkOWMyZmIyYWQ5XkEyXkFqcGdeQWRvb2xpbmhk._V1_.jpg',
		'uploadDate':   '2020-07-08T15:24:44Z'
	}

	sample_3 = {
		'actor': [
			{'@type': 'Person', 'name': 'Elliot Page', 'url': '/name/nm0680983/'},
			{'@type': 'Person', 'name': 'Tom Hopper', 'url': '/name/nm2584392/'},
			{'@type': 'Person', 'name': 'David Castañeda', 'url': '/name/nm3244078/'},
			{'@type': 'Person', 'name': 'Emmy Raver-Lampman', 'url': '/name/nm8287501/'}
		]
	}

	expected_3 = {
		'actor': [
			{'type': 'Person', 'name': 'Elliot Page', 'url': '/name/nm0680983/'},
			{'type': 'Person', 'name': 'Tom Hopper', 'url': '/name/nm2584392/'},
			{'type': 'Person', 'name': 'David Castañeda', 'url': '/name/nm3244078/'},
			{'type': 'Person', 'name': 'Emmy Raver-Lampman', 'url': '/name/nm8287501/'}
		]
	}
	api = IMDBResponseParser()
	result_1 = api._fix_dictionary_keys(sample_1)
	assert result_1 == expected_1

	result_2 = api._fix_dictionary_keys(sample_2)
	assert result_2 == expected_2

	result_3 = api._fix_dictionary_keys(sample_3)
	assert result_3 == expected_3


@pytest.mark.parametrize(
	"actors, expected",
	[
		(responses[0], ['Matt Smith', 'Karen Gillan', 'Arthur Darvill', 'Alex Kingston']),
		(responses[1], ['Zach Tyler', 'Mae Whitman', 'Jack De Sena', 'Michaela Jill Murphy']),
		(responses[2], ['Elliot Page', 'Aidan Gallagher', 'Robert Sheehan', 'Tom Hopper']),
		(responses[3], ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher', 'Alec Guinness']),
		(responses[4], ['Sam Worthington', 'Zoe Saldana', 'Sigourney Weaver', 'Michelle Rodriguez']),
		(responses[5], ['Robert Downey Jr.', 'Chris Evans', 'Mark Ruffalo', 'Chris Hemsworth']),
		(responses[6], ['Zach Tyler', 'Mae Whitman', 'Jack De Sena', 'Dee Bradley Baker']),
		(responses[7], ['Ian McShane', 'Christopher Egan', 'Susanna Thompson', 'Allison Miller']),
		(responses[8], ['Elliot Page', 'Tom Hopper', "David Casta\u00f1eda", 'Emmy Raver-Lampman'])
	]
)
def test_parse_actors(actors, expected):
	api = IMDBResponseParser()

	result = api._parse_actors(actors)

	assert result == expected


@pytest.mark.parametrize(
	"response, expected",
	[
		(responses[0], "PT44M"),
		(responses[1], "PT1H32M"),
		(responses[2], None),
		(responses[3], "PT2H1M"),
		(responses[4], "PT2H42M"),
		(responses[5], "PT3H1M"),
		(responses[6], None),
		(responses[7], None),
		(responses[8], None)
	]
)
def test_parse_runtime(response, expected):
	api = IMDBResponseParser()
	result = api._parse_runtime(response)
	if expected is not None:
		expected = timetools.Duration(expected).as_timedelta()
	assert result == expected


@pytest.mark.parametrize(
	"response, expected",
	[
		(responses[0], "2012-09-29"),
		(responses[1], "2008-07-19"),
		(responses[2], None),
		(responses[3], "1977-05-25"),
		(responses[4], "2009-12-16"),
		(responses[5], "2019-04-24"),
		(responses[6], "2005-02-21"),
		(responses[7], "2009-03-15"),
		(responses[8], "2019-02-15")
	]
)
def test_parse_date_published(response, expected):
	if expected is not None: expected = timetools.Timestamp(expected).to_datetime()

	result = IMDBResponseParser()._parse_date_published(response)

	assert result == expected


@pytest.mark.parametrize(
	"response, expected",
	[
		(responses[0], ["Nick Hurran"]),
		(responses[1], ["Joaquim Dos Santos"]),
		(responses[2], []),
		(responses[3], ["George Lucas"]),
		(responses[4], ["James Cameron"]),
		(responses[5], ["Anthony Russo", "Joe Russo"]),
		(responses[6], []),
		(responses[7], []),
		(responses[8], [])
	]
)
def test_parse_director(response, expected):
	result = IMDBResponseParser()._parse_director(response)
	assert result == expected


@pytest.mark.parametrize(
	"response, expected_rating, expected_count",
	[
		(responses[0], 9.0, 7025),
		(responses[1], 9.9, 6422),
		(responses[2], math.nan, 0),
		(responses[3], 8.6, 1219511),
		(responses[4], 7.8, 1111751),
		(responses[5], 8.4, 786947),
		(responses[6], 9.2, 240659),
		(responses[7], 8.2, 8102),
		(responses[8], 8.0, 150126)
	]
)
def test_parse_imdb_rating(response, expected_rating, expected_count):
	result_rating, result_count = IMDBResponseParser()._parse_imdb_rating(response)

	assert result_rating == expected_rating or (math.isnan(result_rating) and math.isnan(expected_rating))
	assert result_count == expected_count


@pytest.mark.parametrize(
	"response, expected",
	[
		(responses[0], resources[0]),
		(responses[3], resources[1]),
		(responses[7], resources[2]),
		(responses[2], resources[3])
	]
)
def test_parse_response(response, expected):
	result = IMDBResponseParser().parse_response(response)
	assert result == expected
