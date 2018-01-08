import requests
from pprint import pprint
import os
import json
import matplotlib.pyplot as plt
import math
plt.style.use('fivethirtyeight')
CACHE_FILENAME = "imdb_cache_file.json"
_api_filename = os.path.join(os.getenv("USERPATH"), "Documents", "Github", "api_keys.txt")

with open(_api_filename, 'r') as file1:
	API_KEY = file1.read()

class IMDBAPI:
	def __init__(self):
		self.cache_file = self._loadCacheFile()
	def _getFromCache(self, parameters):
		""" Searches the cache for a specific_value.
		"""
		_imdbId = parameters.get('i')
		_title  = parameters.get('t')
		key_value = parameters.get(_imdbId, _title)
		if key_value in self.cache_file:
			pass
	def _loadCacheFile(self):
		if os.path.exists(CACHE_FILENAME):
			with open(CACHE_FILENAME, 'r') as file1:
				reader = json.loads(file1.read())
			return reader
		else:
			return dict()
	def _saveCacheFile(self):
		with open(CACHE_FILENAME, 'w') as file1:
			file1.write(json.dumps(self.cache_file, sort_keys = True, indent = 4))
	def _parseResponse(self, response):
		response['Response'] = response['Response'] == 'True'
		return response
	def _parseSeasons(self, seasons):
		episode_list = list()
		episode_number = 0
		for season_number, season in enumerate(seasons, start = 1):
			season_num = self._tonum(season['Season'])
			episodes = season['Episodes']
			new_episodes = list()
			for episode in episodes:
				episode_number += 1
				notation = "S{0:>02}E{1:>02}".format(season_num, episode['Episode'])
				new_episode = {
					'imdbId': 		episode['imdbID'],
					'imdbRating': 	self._tonum(episode['imdbRating']),
					'index':  		episode_number,
					'name': 		"{0} - {1}".format(notation, episode['Title']),
					'notation': 	notation,
					'number': 		self._tonum(episode['Episode']),
					'title': 		episode['Title'],
					'released': 	episode['Released'],
					'season':		season_number
				}

				episode_list.append(new_episode)
		return episode_list
	@staticmethod
	def _tonum(value):
		""" Converts a string to a valid numerical type"""
		try:
			if '.' in value: number = float(value)
			else: number = int(value)
		except:
			number = math.nan
		return number

	def request(self, **parameters):
		url = ""

		response = requests.get(url, parameters)

		response = response.json()

		return response

	def _request(self, **parameters):
		""" Retrieves by IMDB ID or title. 
			The supplied title must e explicitly defined.
			Parameters
			----------
				i: string
					The IMDB ID number for a given title
				t: string
					The title to search for
				_type: {'movie', 'series', 'episode'}; default ''
					The type of show to return
				y: string; default ''
					Year of release
				plot: {'short', 'long'}; default 'short'
					Whether to return short or long plot descriptions
				r: {'json', 'xml'}; default 'json'
					The format to return the data in
				tomatoes: bool; default False
					Whether to include ratings from Rotten Tomatoes
				callback: string
					JSONP callback name
				v: int; default 1
					API version (reserved for future use)
			Returns
			----------
				series : dict<>
					***: movie-only
					---: TV-show only
					--------------------- Common Keys ---------------------
					*'Actors': string 
						A short list of the show frontrunners
					*'Awards': string
						A summary of any awards the show has been awarded.
						Ex. "Won 2 Golden Globes. Another 132 wins & 213 nominations."
					*'Country': string
						The primary country of origin
					*'Director': string
						The primary director for the series
					*'Genre': string
						A list of any genres the show falls under
						Ex. "Drama, Sci-Fi, Thriller"
					*'Language': string
						The primary language(s) spoken in the show
						Ex. "English"
					***'Metascore': string; default 'N/A'
						pass
					*'Plot': string
						A short description of the plot of the show.
					*'Production': string
						The company that produced the show/film
					*'Poster': string (URL)
						A URL link to a poster of the show
					*'Rated': link; default 'N/A'
						The maturity rating of the production.
						Ex. 'TV-PG'
					*'Released': string (date)
						The date the show was released. If a TV show, this will be the
						broadcast date of the first episode.
						Ex. "12 Jun 2015"
					*'Response': bool
						Whether a response was received from the servers
					*'Runtime': string (duration)
						The total length of the production. If a TV show, this will
						be a typical length of a single episode.
						Ex. "42 min"
					*'Title': string
						The title of the production.
					*'Type': {'movie', 'series', 'episode'}
						The type of production
					*'Writer': string
						The lead writer(s) for the show.
						Ex. "Joseph Mallozzi, Paul Mullie"
					*'Year': string (year-year)
						The year the production started and the year it ended.
						If the show is still running, the end year is omitted.
						Ex. "2015-"
					*'imdbID': string
						The unique ID assigned to the production via IMDB.
					*'imdbRating': string<float>
						The rating of the production on IMDB
					*'imdbVotes': string<int>
						The number of users who have given the production a rating.
						Ex. "18,184"
					---'totalSeasons': string<int>
						The current number of seasons produced or planned for the show.
					-------------------------- TV Show Keys -------------------------
					
					--------------------------- Film Keys --------------------------
					*'BoxOffice': string
						The box office performance of the movie.
						Ex. 
					*'DVD': string
						The date the film was released as a DVD.
						Ex. '18 Dec 2007'
					*'Metascore': int
						The score assigned to the film on Metacritic.com
					--------------------- Rotten Tomatoes Addon ---------------------
					***'tomatoConsensus': string
						 A summary of the critic reviews available on rotten tomatoes.
					***'tomatoImage': string
						The rotten tomatoes image to display next to the movie's score.
						Ex. 'certified'
					***'tomatoMeter': string<int>
						The Rotten Tomatoes critic-based metric.
					***'tomatoRating': string<float>
						The average critic review of the movie, out of ten
					***'tomatoReviews': string<int>
						The total number of critics whos reviews were taken into account.
					***'tomatoFresh': string<int>
						The total number of critics that gave the movie a positive review.
					***'tomatoRotten': string<int>
						The total number of critics that gave the film a negative review.
					***'tomatoURL': string (URL)
						The URL that links the the film's page on rotten tomatoes.
					***'tomatoUserRating': string<int>
						The average rating (out of five) given by the users of the Rotten Tomatoes
						website.
					***'tomatoUserReviews': string<int>
						The total number of users that gave the film a rating.
		"""
		#self._getFromCache(parameters)
		endpoint = "http://www.omdbapi.com/"
		_expected = '&'.join(["{0}={1}".format(i,j) for i,j in sorted(parameters.items())])
		if _expected in self.cache_file:
			response = self.cache_file[_expected]
		else:
			response = requests.get(endpoint, parameters)
			_key_url = response.url.replace(endpoint + '?', '')
			response = response.json()
			self.cache_file[_key_url] = response
			self._saveCacheFile()


		response = self._parseResponse(response)
		return response

	def find(self, title):
		""" Searches the IMDB database and returns the first result found.
			Parameters
			----------
				title: string
					The title of a Movie, TV show, or episode. imdbIds
					are also accepted. 
			Returns
			----------
				series : dict<> (from self.by_uid())
				If the series is not found, returns
				{'Response': 'False', 'Error': 'Movie not found!'}
		"""
		if title[:2] == 'tt' and any(s.isdigit() for s in title[2:]):
			first_id = title
		else:
			response = self.search(s = title)
			if 'Search' not in response:
				message = "Error when using api.find(title = '{}')".format(title)
				pprint(response)
				raise ValueError(message)
			else:
				first_id = response['Search'][0]['imdbID']

		first_show = self._request(
			i = first_id,
			tomatoes = False)
		first_show['episodeList'] = self.getSeasons(i = first_id)

		return first_show

	def search(self, **kwargs):
		""" Searches IMDB for a specific title
			Parameters
			----------
				s: string
					The movie title to search for
				type: {'movie', 'series', 'episode'}
					Type of result to return
				y: string
					year of release
				r: {'json', 'xml'}; default 'json'
					The format to return
				page: int [1-100]; default 1
					The page number to return
				callback: string
					JSONP callback name
				v: int
					API version (reserved for future use)
			Returns
			----------
				production: dict<>
					A dictionary containing a list of matches to
					the supplied arguements.
						'Response': bool; default True,
							Whether a response was received
						'totalResults': int,
							The total number of matches that were found.
						'Search': list<dict<>>
							A list of dictionaries with the followinf keys:
								'Poster': string (url)
									A URL linking to a poster for the production.
								'Title': string
									The title of the production.
								'Type': {'series', 'movie', 'episode'}
									The type of production
								'Year': string
									The year the production was released.
								'imdbID' string
									The unique ID for the production.
		"""
		s = kwargs.get('s', kwargs.get('t', kwargs.get('i')))
		if s is None:
			message = "Did not include a search keyword ('s', 't', 'i')!"
			raise ValueError(message)
		
		response = self._request(s = s)
		return response
	
	def getSeasons(self, **kwargs):
			""" Retrieves all seasons for a show
				Keyword Parameters
				----------
					i, imdbID: string
						The show's IMDB ID number.
				Returns
				----------
					episodes : list of dicts
						A list containing basic information about each season
						'Response' bool
							Whether a response was received from the servers.
						'Title': string
							The name of the production
						'Season': The show season
						'episodes' = list<dict<>>
							A list of each season
									 'Episode': string: episode number
									 'Released': ISO date string
									 'Title': Name of the episode
									 'imdbID': string
									 'imdbRating': string

			"""
			if 'i' in kwargs.keys():
				imdbID = kwargs['i']
			elif 'imdbID' in kwargs.keys():
				imdbID = kwargs['imdbID']
			elif 't' in kwargs.keys():
				pprint(self.request(i = kwargs['t']))
				imdbID = self.request(i = kwargs['t'])['imdbID']
			elif 'Title' in kwargs.keys():
				imdbID = self.request(i = kwargs['Title'])['imdbID']

			seasons = list()
			season_number = 0
			while True:
				season_number += 1
				response = self._request(i = imdbID, season = season_number)
				if 'Error' in response.keys(): break
				seasons.append(response)
			seasons = self._parseSeasons(seasons)
			return seasons

	def getEpisodeTitles(self, **kwargs):
		pass
	def getImdbId(self, **kwargs):
		"""  
		"""
		pass
	def getShowStatus(self):
		""" Determines whether a show is still airing new seasons or 
			it has completed its run.
		"""
		pass



api = IMDBAPI()
if __name__ == "__main__":
	test_string = "Wayward Pines"
	result = api.find(test_string)
	pprint(result)