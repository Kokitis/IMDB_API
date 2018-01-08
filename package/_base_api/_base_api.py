
import requests
from pprint import pprint
import os
import math
import random
#import matplotlib.pyplot as plt 
from scipy import stats

class OmdbApi:
	def __init__(self, api_key):
		self.endpoint = ""
		self.api_key = api_key


	def get(self, string):
		"""
			Parameters
			----------
				*'i': IMDB ID
				*'s': Search term
				*'season': int
					Requests a specific season from the api.
		"""

		parameters = {

		}
		response = self.request(**parameters)
		# Should include error checking
		#if result is None or 'season' in parameters:
		if 'Type' not in response:
			pass
		elif response['Type'] == 'series':
			result = self._parseSeries(response)
		elif response['Type'] == 'movie':
			result = self._parseMovie(response)

		return result

	def _parseSeason(self, api_response, start = 1):
		""" 
			Parameters
			----------
				api_response: dict<>
				start: int
					Since seasons are parsed one at a time, this establishes the starting point when determining episode numbers.

		"""
		processed_season = list()
		for episode in api_response['Episodes']:

			_season_number = int(api_response['Season'])
			_episode_number= int(episode['Episode'])
			notation = "S{:>02}E{:>02}".format(_season_number, _episode_number)
			title = episode['Title']
			processed_episode = {
				'index': 	start + _episode_number,
				'name':		"{} - {}".format(notation, title),
				'episode': 	notation,
				'season': 	int(api_response['Season']),
				'seasonIndex': _episode_number,
				'date': 	episode['Released'],
				'title': 	title,
				'imdbId': 	episode['imdbID'],
				'imdbRating': self._tonum(episode['imdbRating'])
			}
			processed_season.append(processed_episode)

		processed_season = Season(processed_season)
		return processed_season

	def _parseSeries(self, api_response, include_seasons = False):
		""" """
		series_id = api_response['imdbID']
		total_seasons = api_response['totalSeasons']
		
		seasons = list()
		if include_seasons:
			_total_episodes = 0
			for season_num in range(0, total_seasons):
				print("Parsing season number {}".format(season_num))
				s = self._request(i = series_id, season = season_num + 1)
				s = self._parseSeason(s, start = _total_episodes)
				seasons.append(s)
				_total_episodes += len(s)
			
		api_response['seasons'] = seasons

		return api_response

	def _parseMovie(self, api_response):
		pass

	def search(self):
		pass

	def request(self, **parameters):
		parameters['apikey'] = self.api_key
		url = "http://www.omdbapi.com/"
		response = requests.get(url, parameters)
		response = response.json()
		return response

class Season:
	def __init__(self, season):
		""" Handles common season operations.
			Parameters
			----------
				season: list<dict<>>
		"""
		self._graphtv_colors = [
			'#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
			'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
			'#79CEF2'
		]

		self._episode_list = season

		if len(self._episode_list) > 0:
			self.number = self._episode_list[0]['season']



	def __iter__(self):
		for i in self._episode_list:
			yield i

	def __len__(self):
		return len(self._episode_list)

	def _calculateRegression(self, kind = 'average'):
		""" Calculates regression lines for the given series
			Parameters
			----------
				series: list of (x, y) pairs
					The series to calculate a regression series for
				kind: {'linear', 'moving average', 'static'}; default 'linear'
					The type of regression to calculate.
					* 'linear': Standard linear regression per season.
					* 'moving average': Calculates regressing as a moving average.
					* 'average': returns the average per season.
			Returns
			----------
				regression_line : list of (x, y) pairs
					The regression series that was calculated 
					for the given series
		"""
		x, y = zip(*series)
		
		regression_line = list()
		if kind == 'linear':
			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			regression_line = [(i, slope*i+intercept) for i in x]
		elif kind == 'moving average':
			period = 3
			for index in range(len(y)):
				if index < period:
					previous = y[:index+1]
				else:
					previous = y[index - period+1:index+1]
				mean = sum(previous) / len(previous)
				regression_line.append((x[index], mean))
		elif kind == 'average':
			_y = [i for i in y if not math.isnan(i)]
			if len(_y) > 0:
				average = sum(_y) / len(_y)
			else:
				average = math.nan
			regression_line = [(i, average) for i in x]
		return regression_line
	
	def _generateColor(self, kind = 'GraphTV'):
		""" Generates a list of colors to use in the graph
			Parameters
			----------
				bins: int
					A list of the bin keys to asign colors to.
				kind: {'GraphTV', 'random'}; default 'GraphTV'
					The color map to use
					*'GraphTV': The series of colors used on the GraphTV webpage
					*'random': A randomly generated series of colors
			Returns
			-------
				colors: dict<>
		"""
		colors = dict()
		if kind == 'GraphTV':
			color = self._graphtv_colors[self.number]
		else:
			lower = 100
			upper = 256
			red   = random.randrange(lower, upper)
			blue  = random.randrange(lower, upper)
			green = random.randrange(lower, upper)
			color = '#{0:02X}{1:02X}{2:02X}'.format(red, blue, green)

		return color

	@property
	def index(self):
		for episode in self:
			yield episode['index']
	@property
	def ratings(self):
		for episode in self:
			yield episode['imdbRating']

	@property
	def rating(self):

		total = sum(self.ratings)
		length = len(self)
		return total / length

	@property
	def color(self):
		return self._generateColor()



if __name__ == "__main__":
	API = OmdbApi()
	test_show = "tt1898069" # American Gods
	test_movie= "tt0848228" # The Avengers
	vd = "tt1405406" # The Vampire Diaries

	result = API.request(vd, True)
	pprint(result)
	graph = GraphTv(result)
	plt.show()

		