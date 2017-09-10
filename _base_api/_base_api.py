
import requests
from pprint import pprint
import os
import math
#import matplotlib.pyplot as plt 
from scipy import stats

_api_filename = os.path.join(os.getenv("HOMEPATH"), "Documents", "Github", "api_keys.txt")

with open(_api_filename, 'r') as file1:
	API_KEY = file1.read()

class OmdbApi:
	def __init__(self):
		self.endpoint = ""
		self.api_key = API_KEY
	def __call__(self, string):
		"""

		"""


		pass
	@staticmethod
	def _tonum(value):
		""" Converts a string to a valid numerical type"""
		try:
			if '.' in value: number = float(value)
			else: number = int(value)
		except:
			number = math.nan
		return number
	def _request(self, raw = None, include_seasons = False, **parameters):
		"""
			Parameters
			----------
				*'i': IMDB ID
				*'s': Search term
				*'season': int
					Requests a specific season from the api.
		"""
		if raw:
			test_id = raw['i']
			parameters = {'i': test_id}
		elif 'i' in parameters:
			pass
		endpoint = "http://www.omdbapi.com/"
		

		parameters['apikey'] = self.api_key 

		result = requests.get(endpoint, parameters)

		# Should include error checking

		result = result.json()
		if result['Response'] == 'False':
			print("Endpoint: ", endpoint)
			pprint(parameters)
			result = None
		#pprint(result)
		#if result is None or 'season' in parameters:
		if 'Type' not in result:
			pass
		elif result['Type'] == 'series':
			result = self._parseSeries(result, include_seasons)
		elif result['Type'] == 'movie':
			result = self._parseMovie(result)

		return result


	def _parseMovie(self, raw_result):
		print("PARSING MOVIE")
		return raw_result
	def _parseSeason(self, raw_result, start = 1):
		""" 
			Parameters
			----------
				raw_result: dict<>
				start: int
					Since seasons are parsed one at a time, this establishes the starting point when determining episode numbers.

		"""
		processed_season = list()
		for episode in raw_result['Episodes']:

			_season_number = int(raw_result['Season'])
			_episode_number= int(episode['Episode'])
			notation = "S{:>02}E{:>02}".format(_season_number, _episode_number)
			title = episode['Title']
			processed_episode = {
				'index': 	start + _episode_number,
				'name':		"{} - {}".format(notation, title),
				'episode': 	notation,
				'season': 	int(raw_result['Season']),
				'seasonIndex': _episode_number,
				'date': 	episode['Released'],
				'title': 	title,
				'imdbId': 	episode['imdbID'],
				'imdbRating': self._tonum(episode['imdbRating'])
			}
			processed_season.append(processed_episode)

		processed_season = Season(processed_season)
		return processed_season

	def _parseSeries(self, raw_result, include_seasons = False):
		""" """
		raw_result['totalSeasons'] = int(raw_result['totalSeasons'])
		series_id = raw_result['imdbID']
		total_seasons = raw_result['totalSeasons']
		
		seasons = list()
		if include_seasons:
			_total_episodes = 0
			for season_num in range(0, total_seasons):
				print("Parsing season number {}".format(season_num))
				s = self._request(i = series_id, season = season_num + 1)
				s = self._parseSeason(s, start = _total_episodes)
				seasons.append(s)
				_total_episodes += len(s)
			
		raw_result['seasons'] = seasons

		return raw_result

	def _getSeriesStatus(self, raw_result):
		pass

	def request(self, string, include_seasons = False):
		"""
		"""

		if string.startswith('tt'):
			key = 'i'
		else:
			key = 't'

		result = self._request({key:string}, include_seasons)
		return result

	def findOne(self):
		pass

	def search(self):
		pass

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

		