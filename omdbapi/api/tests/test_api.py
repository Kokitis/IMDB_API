import unittest
from omdbapi import OmdbApi, MediaResource
from pytools import timetools
import math


class TestOmdbApiSeries(unittest.TestCase):
	def setUp(self):
		self.api = OmdbApi()
		self.series_key = 'tt5114356'  # Legion
		self.movie_key = 'tt2488496'  # The force awakens
		self.series_title = "Legion"
		self.movie_title = 'Star Wars: The Force Awakens'

		self.series_data = MediaResource(
			actors = 'Dan Stevens, Rachel Keller, Aubrey Plaza, Bill Irwin',
			awards = '2 wins & 13 nominations.',
			country = 'USA',
			director = 'N/A',
			duration = timetools.Duration('PT1H'),
			genre = 'Action, Drama, Sci-Fi',
			imdbId = 'tt5114356',
			imdbRating = 8.4,
			imdbVotes = 65565,
			language = 'English',
			metascore = math.nan,
			plot = 'David Haller is a troubled young man diagnosed as schizophrenic, but after a strange encounter, he discovers special powers that will change his life forever.',
			rating = 'TV-MA',
			ratings = [{'Source': 'Internet Movie Database', 'Value': '8.4/10'}],
			releaseDate = timetools.Timestamp(2017, 2, 8, 0, 0, 0),
			responseStatus = True,
			title = 'Legion',
			type = 'series',
			writer = 'Noah Hawley',
			year = '2017–',
			totalSeasons = 2,
			seasons = [],
			indexInSeason = 0,
			indexInSeries = 0,
			episodeId = 'N/A'
		)

		self.movie_data = MediaResource(
			actors = 'Harrison Ford, Mark Hamill, Carrie Fisher, Adam Driver',
			awards = 'Nominated for 5 Oscars. Another 57 wins & 123 nominations.',
			country = 'USA',
			director = 'J.J. Abrams',
			duration = timetools.Duration('PT2H16M'),
			genre = 'Action, Adventure, Fantasy',
			imdbId = 'tt2488496',
			imdbRating = 8,
			imdbVotes = 751557,
			language = 'English',
			metascore = 81,
			plot = "Three decades after the Empire's defeat, a new threat arises in the militant First Order. Stormtrooper defector Finn and the scavenger Rey are caught up in the Resistance's search for the missing Luke Skywalker.",
			rating = 'PG-13',
			ratings = [
				{'Source': 'Internet Movie Database', 'Value': '8.0/10'},
				{'Source': 'Rotten Tomatoes', 'Value': '93%'},
				{'Source': 'Metacritic', 'Value': '81/100'}
			],
			releaseDate = timetools.Timestamp(2015, 12, 18, 0, 0, 0),
			responseStatus = True,
			title = 'Star Wars: The Force Awakens',
			type = 'movie',
			writer = 'Lawrence Kasdan, J.J. Abrams, Michael Arndt, George Lucas (based on characters created by)',
			year = '2015',
			totalSeasons = 0,
			seasons = [],
			indexInSeason = 0,
			indexInSeries = 0,
			episodeId = 'N/A'
		)

	def test_series_get_by_id(self):
		response = self.api.get(self.series_key)
		response.seasons = []

		self.assertEqual(self.series_data, response)

	def test_series_find_by_id(self):
		response = self.api.find(self.series_key)
		response.seasons = []
		self.assertEqual(self.series_data, response)

	def test_series_find_by_title(self):
		response = self.api.find(self.series_title)
		response.seasons = []
		self.assertEqual(self.series_data, response)

	def test_movie_get_by_id(self):
		response = self.api.get(self.movie_key)
		self.assertEqual(self.movie_data, response)

	def test_movie_find_by_id(self):
		response = self.api.find(self.movie_key, kind = 'movie')

		self.assertEqual(self.movie_data, response)

	def test_movie_find_by_name(self):
		response = self.api.find(self.movie_title, kind = 'movie')
		self.assertEqual(self.movie_data, response)


if __name__ == "__main__":
	unittest.main()
