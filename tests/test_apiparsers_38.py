import datetime
import json
import math
from pathlib import Path
from typing import Dict, Any

import pendulum
import pytest

from omdbapi.api import apiparsers

data_folder = Path(__file__).parent / "data"


@pytest.fixture
def expected_resources() -> Dict[str, Any]:
	american_gods = {
		'actors':       ["Ricky Whittle", "Emily Browning", "Crispin Glover", "Yetide Badaki"],
		'awards':       "Nominated for 2 Primetime Emmys. Another 5 wins & 32 nominations.",
		'countries':    ["USA"],
		'director':     'N/A',
		'genres':       ['drama', 'fantasy', 'mystery'],
		'languages':    ['english'],
		'plot':         "A recently released ex-convict named Shadow meets a mysterious man who calls himself \"Wednesday\" and who knows more than he first seems to about Shadow's life and past.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BYTMyYmFjYWUtYjMyOS00ZjRlLWIxODUtYjUyYTFkM2ZmMmQxXkEyXkFqcGdeQXVyNjg3MDMxNzU@._V1_SX300.jpg",
		'rated':        'TV-MA',
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "7.8/10"
			}
		],
		'releaseDate':  pendulum.date(2017, 4, 30),
		'runtime':      pendulum.Duration(minutes = 60),
		'title':        'American Gods',
		'type':         'series',
		'writers':      ["Bryan Fuller", "Michael Green"],
		'imdbId':       'tt1898069',
		'imdbRating':   7.8,
		'imdbVotes':    69569,
		'totalSeasons': 3,
	}

	vghs = {
		'actors':       ['Josh Blaylock', 'Ellary Porterfield', 'Johanna Braddy', 'Jimmy Wong'],
		'awards':       "5 wins & 17 nominations.",
		'countries':    ['USA'],
		'director':     'N/A',
		'genres':       ['action', 'romance', 'sci-fi'],
		'languages':    ['english'],
		'plot':         "In a futuristic world where gaming is the top sport, a teenager attends a school which specializes in a curriculum of video games in each genre.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BOTgxOTMwOTAxMF5BMl5BanBnXkFtZTcwMTY3MTExOA@@._V1_SX300.jpg",
		'rated':        'TV-14',
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "7.6/10"
			}
		],
		'releaseDate':  pendulum.Date(2012, 5, 11),
		'runtime':      pendulum.Duration(minutes = 42),
		'title':        'Video Game High School',
		'type':         'series',
		'writers':      [],
		'imdbId':       "tt2170584",
		'imdbRating':   7.6,
		'imdbVotes':    12452,
		'totalSeasons': 3
	}

	sherlock = {
		'actors':       ["Benedict Cumberbatch", "Martin Freeman", "Una Stubbs", "Rupert Graves"],
		'awards':       "Nominated for 1 Golden Globe. Another 88 wins & 172 nominations.",
		'countries':    ['UK', 'USA'],
		'director':     'N/A',
		'genres':       ['crime', 'drama', 'mystery', 'thriller'],
		'languages':    ['english'],
		'plot':         "A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BMWY3NTljMjEtYzRiMi00NWM2LTkzNjItZTVmZjE0MTdjMjJhL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTQ4NTc5OTU@._V1_SX300.jpg",
		'rated':        'TV-14',
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "9.1/10"
			}
		],
		'releaseDate':  pendulum.Date(2010, 10, 24),
		'runtime':      pendulum.Duration(minutes = 88),
		'title':        'Sherlock',
		'type':         'series',
		'writers':      ['Mark Gatiss', 'Steven Moffat'],
		'imdbId':       'tt1475582',
		'imdbRating':   9.1,
		'imdbVotes':    765513,
		'totalSeasons': 4
	}

	gravity = {
		'actors':          ["Sandra Bullock", "George Clooney", "Ed Harris", "Orto Ignatiussen"],
		'awards':          "Won 7 Oscars. Another 233 wins & 182 nominations.",
		'boxOffice':       274_084_951,
		'countries':       ['UK', 'USA'],
		'releaseDateHome': pendulum.Date(2014, 2, 25),
		'director':        'Alfonso Cuarón',
		'genres':          ['drama', 'sci-fi', 'thriller'],
		'languages':       ['english', 'greenlandic'],
		'plot':            "Two astronauts work together to survive after an accident leaves them stranded in space.",
		'poster':          "https://m.media-amazon.com/images/M/MV5BNjE5MzYwMzYxMF5BMl5BanBnXkFtZTcwOTk4MTk0OQ@@._V1_SX300.jpg",
		'production':      'Warner Bros. Pictures',
		'rated':           'PG-13',
		'ratings':         [
			{
				"source": "Internet Movie Database",
				"value":  "7.7/10"
			},
			{
				"source": "Rotten Tomatoes",
				"value":  "96%"
			},
			{
				"source": "Metacritic",
				"value":  "96/100"
			}
		],
		'releaseDate':     pendulum.Date(2013, 10, 4),
		'runtime':         pendulum.Duration(minutes = 91),
		'title':           'Gravity',
		'type':            'movie',
		'writers':         ['Alfonso Cuarón', 'Jonás Cuarón'],
		'imdbId':          "tt1454468",
		'imdbRating':      7.7,
		'imdbVotes':       749518

	}

	endgame = {
		'actors':          ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth"],
		'awards':          "Nominated for 1 Oscar. Another 65 wins & 103 nominations.",
		'boxOffice':       math.nan,
		'countries':       ['USA'],
		'releaseDateHome': pendulum.Date(2019, 7, 30),
		'director':        "Anthony Russo, Joe Russo",
		'genres':          ['action', 'adventure', 'drama', 'sci-fi'],
		'languages':       ['english', 'japanese', 'xhosa', 'german'],
		'plot':            "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
		'poster':          "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg",
		'production':      'Marvel Studios',
		'rated':           'PG-13',
		'ratings':         [
			{
				"source": "Internet Movie Database",
				"value":  "8.4/10"
			},
			{
				"source": "Rotten Tomatoes",
				"value":  "94%"
			},
			{
				"source": "Metacritic",
				"value":  "78/100"
			}
		],
		'releaseDate':     pendulum.Date(2019, 4, 26),
		'runtime':         pendulum.Duration(minutes = 181),
		'title':           'Avengers: Endgame',
		'type':            'movie',
		'writers':         [
			"Christopher Markus (screenplay by)", "Stephen McFeely (screenplay by)",
			"Stan Lee (based on the Marvel comics by)",
			"Jack Kirby (based on the Marvel comics by)", "Joe Simon (Captain America created by)",
			"Jack Kirby (Captain America created by)", "Steve Englehart (Star-Lord created by)",
			"Steve Gan (Star-Lord created by)", "Bill Mantlo (Rocket Raccoon created by)",
			"Keith Giffen (Rocket Raccoon created by)",
			"Jim Starlin (Thanos,  Gamora & Drax created by)",
			"Stan Lee (Groot created by)", "Larry Lieber (Groot created by)",
			"Jack Kirby (Groot created by)", "Steve Englehart (Mantis created by)",
			"Don Heck (Mantis created by)"
		],
		'imdbId':          "tt4154796",
		'imdbRating':      8.4,
		'imdbVotes':       730943
	}

	sa = {
		'actors':          ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki", "Takashi Naitô"],
		'awards':          "Won 1 Oscar. Another 57 wins & 30 nominations.",
		'boxOffice':       9_855_615,
		'countries':       ["Japan"],
		'releaseDateHome': pendulum.Date(2003, 4, 15),
		'director':        'Hayao Miyazaki',
		'genres':          ['animation', 'adventure', 'family', 'fantasy', 'mystery'],
		'languages':       ['japanese'],
		'plot':            "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
		'poster':          "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
		'rated':           "PG",
		'ratings':         [
			{
				"source": "Internet Movie Database",
				"value":  "8.6/10"
			},
			{
				"source": "Rotten Tomatoes",
				"value":  "97%"
			},
			{
				"source": "Metacritic",
				"value":  "96/100"
			}
		],
		'releaseDate':     pendulum.Date(2003, 3, 28),
		'runtime':         pendulum.Duration(minutes = 125),
		'production':      'Walt Disney Pictures',
		'title':           "Spirited Away",
		'type':            'movie',
		'writers':         ['Hayao Miyazaki'],
		'imdbId':          "tt0245429",
		'imdbRating':      8.6,
		'imdbVotes':       615596
	}

	nge = {
		'actors':       ["Spike Spencer", "Allison Keith", "Sue Ulu", "Amanda Winn Lee"],
		'awards':       "N/A",
		'countries':    ['Japan', 'USA', 'New Zealand'],
		'director':     'N/A',
		'genres':       ['animation', 'action', 'drama', 'fantasy', 'sci-fi', 'thriller'],
		'languages':    ['japanese', 'english'],
		'plot':         "A teenage boy finds himself recruited as a member of an elite team of pilots by his father.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BYjY1Y2ZmNDctZWQ3Yy00MTE3LTk2M2QtMjQ0MDA5ODVjMDEyXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
		'rated':        'TV-14',
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "8.5/10"
			}
		],
		'releaseDate':  pendulum.Date(1997, 8, 20),
		'runtime':      pendulum.Duration(minutes = 624),
		'title':        'Neon Genesis Evangelion',
		'type':         'series',
		'writers':      ['Hideaki Anno'],
		'imdbId':       'tt0112159',
		'imdbRating':   8.5,
		'imdbVotes':    44883,
		'totalSeasons': 1
	}

	sg = {
		'actors':       ["Mamoru Miyano", "Asami Imai", "Kana Hanazawa", "Ashly Burch"],
		'awards':       "N/A",
		'countries':    ['Japan'],
		'director':     'N/A',
		'genres':       ["animation", 'comedy', 'drama', 'romance', 'sci-fi', 'thriller'],
		'languages':    ['japanese', 'english'],
		'plot':         "After discovering time travel, a university student and his colleagues must use their knowledge of it to stop an evil organization and their diabolical plans.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BMjUxMzE4ZDctODNjMS00MzIwLThjNDktODkwYjc5YWU0MDc0XkEyXkFqcGdeQXVyNjc3OTE4Nzk@._V1_SX300.jpg",
		'rated':        "TV-14",
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "8.8/10"
			}
		],
		'releaseDate':  pendulum.Date(2011, 4, 6),
		'runtime':      pendulum.Duration(minutes = 24),
		'title':        'Steins;Gate',
		'type':         'series',
		'writers':      [],
		'imdbId':       "tt1910272",
		'imdbRating':   8.8,
		'imdbVotes':    38901,
		'totalSeasons': 1
	}

	konosuba = {
		'actors':       ["Jun Fukushima", "Sora Amamiya", "Rie Takahashi", "Ai Kayano"],
		'awards':       "N/A",
		'countries':    ['Japan'],
		'director':     'N/A',
		'genres':       ['animation', 'adventure', 'comedy', 'fantasy'],
		'languages':    ['japanese'],
		'plot':         "It was a happy day for Kazuma - right up to the moment he died. A goddess intervenes and offers him a second chance in a magical land.",
		'poster':       "https://m.media-amazon.com/images/M/MV5BNDNiOWM5NGItNzY4NC00MDg1LTljZjctYzViNmRlOTNhOWM2XkEyXkFqcGdeQXVyNjc3OTE4Nzk@._V1_SX300.jpg",
		'rated':        'TV-14',
		'ratings':      [
			{
				"source": "Internet Movie Database",
				"value":  "7.8/10"
			}
		],
		'releaseDate':  pendulum.Date(2016, 1, 12),
		'runtime':      pendulum.Duration(minutes = 24),
		'title':        "Konosuba: God's Blessing on This Wonderful World!",
		'type':         'series',
		'writers':      [],
		'imdbId':       "tt5370118",
		'imdbRating':   7.8,
		'imdbVotes':    4279,
		'totalSeasons': 2

	}

	responses = {
		# Series
		'tt1898069': american_gods,
		'tt2170584': vghs,
		'tt1475582': sherlock,
		# Movies
		"tt1454468": gravity,
		"tt4154796": endgame,
		"tt0245429": sa,
		# Anime
		"tt0112159": nge,
		'tt1910272': sg,
		'tt5370118': konosuba
	}

	return responses


@pytest.mark.parametrize(
	"imdb_id", [
		# Series
		'tt1898069', 'tt2170584', 'tt1475582',
		# Movies
		"tt1454468", "tt4154796", "tt0245429",
		# Anime
		"tt0112159", 'tt1910272', 'tt5370118'
	]
)
def test_api_parsers(expected_resources, imdb_id):
	filename_response = data_folder / f"{imdb_id}.json"
	content = filename_response.read_text()
	response = json.loads(content)
	expected_resource = expected_resources[imdb_id]

	result = apiparsers.parse_api_response(response)

	if 'episodes' in result:
		result.pop('episodes')

	assert result == expected_resource


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
