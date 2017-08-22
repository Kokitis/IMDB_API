#%matplotlib inline
import notebook
#IPython.utils.load_extension('usability/codefolding/main');
import random
import numpy
import pandas
import math
import json
import requests
import matplotlib.pyplot as plt
import pandas
import os
import re

#import timetools as tt
import scipy.stats as stats
from pprint import pprint
from itertools import chain
#import seaborn as sns
plt.style.use('fivethirtyeight')
CACHE_FILENAME = "imdb_cache_file.json"

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
		pprint(parameters)
		response = requests.get(endpoint, parameters)

		response = response.json()
		pprint(response)
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
				print("Warning: In API.find({0}):".format(title))
				pprint(response)
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

class Parser:
	""" Parses information saved as a file and outputs relevant 
		information regarding each saved show.
	"""
	def __init__(self, io):
		""" Parses a file containing show titles/IDs.
			Parameters
			----------
				io: string ['.json', 'xls', 'xlsx']
					Path to the the file.
		"""
		ext = os.path.splitext(io)[1]
		data = self._read_file(io, ext)
	def _read_file(self, filename, ext):

		with open(filename, 'r') as file1:
			if ext == '.json':
				import json
				data = json.loads(file1.read())
			elif ext in {'.csv', 'tsv'}:
				data = readCSV(filename)
			elif ext in {'.xls', 'xlsx'}:
				data = pandas.read_excel(filename)
		return data

class GraphTV:
	def __init__(self, show, ax = None, kind = 'linear', show_dots = True, colorscheme = 'GraphTV'):
		""" Plots every episode's rating
			Parameters
			----------
				show: dict<>
					Response from the IMDB API.
				ax: matplotlib.axes._subplots.AxesSubplot; default None
					If provided, the graph to plot the episode rating on.
					If not provided, a new one will be created
				kind: {'linear', 'moving average'}; default 'linear'
					The type of regression line to draw
						*'linear': Least-squares linear regression line
						*'moving average': The 5-point moving average
				show_dots: bool; default True
					Whether to show each episode's rating as a scatter plot
			Returns
			----------
				fig, ax :  tuple
					*fig: matplotlib.figure.Figure
						The pyplot figure object that contains the graph
					*ax:  matplotlib.axes._subplots.AxesSubplot
						The ax obbject that contains the graph
		"""
		episode_df = pandas.DataFrame(show['episodeList'])
		if ax is None:
			self.fig, self.ax = plt.subplots(figsize = (20,5))
			self.fig.patch.set_facecolor('#333333')
		else:
			self.fig = None
		colors = self._generate_colors(
			bins = episode_df['seasonNumber'].unique(), 
			kind = colorscheme)
		self.ax = self._format_ax(self.ax)
		

		self.ax      = self._plot_seasons(self.ax, episode_df, colors, 
						regression_type = kind, show_dots = show_dots)
		
		total_episodes = len(episode_df)
		print("Total Episodes: ", total_episodes)
		self.ax.set_xlim((0, total_episodes + 1))
		self.ax.set_ylim(ymax = 10)
		
		#return fig, ax

	def _plot_seasons(self, ax, episodes, colors, regression_type = 'linear', show_dots = True):
		""" Plots each season
			Parameters
			----------
				ax: matplotlib.axes._subplots.AxesSubplot
					The plot to add each series to
				episodes: pandas.DataFrame
					A list of every season and episode in the show
					[[(episode number, rating)]]
				colors: list
					A list of the colors to use
				regression_line : list of (x, y) pairs
					The regression series that was calculated 
					for the given series
				show_dots: bool; default True
					Whether to show each episode's rating as a scatter plot
			Returns
			----------
				ax : matplotlib.axes._subplots.AxesSubplot
		"""
		_num_episodes = 0
		seasons = episodes.groupby(by = 'seasonNumber')
		for season_number, season_episodes in seasons:
			x = season_episodes['episodeIndex'].values
			y = season_episodes['imdbRating'].values

			if show_dots:
				ax.scatter(x, y, color = colors[season_number], s = 100)
			series = list(zip(x, y))
			if len(series) > 0:
				rseries = self._calculateRegression(series, kind = regression_type)
				rx, ry = zip(*rseries)
				ax.plot(rx, ry, color = colors[season_number])
		return ax
	@staticmethod
	def _calculateRegression(series, kind = 'average'):
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
				
	@staticmethod
	def _format_ax(ax):
		""" Formats the plot aesthetics
			Parameters
			----------
				ax: matplotlib.axes._subplots.AxesSubplot
					The plot to format
			Returns
			----------
				ax : matplotlib.axes._subplots.AxesSubplot
		"""
		BACKGROUND_COLOR = '#333333'
		ax.patch.set_facecolor(BACKGROUND_COLOR)
		ax.spines['bottom'].set_color(BACKGROUND_COLOR)
		ax.spines['top'].set_color(BACKGROUND_COLOR)
		ax.spines['left'].set_color(BACKGROUND_COLOR)
		ax.spines['right'].set_color(BACKGROUND_COLOR)
		
		#change the label colors
		[i.set_color("#999999") for i in plt.gca().get_yticklabels()]
		[i.set_color("#999999") for i in plt.gca().get_xticklabels()]
		
		#Change tick size
		ax.tick_params(axis='y', which='major', labelsize=22)
		ax.tick_params(axis='y', which='minor', labelsize=22)
		ax.yaxis.grid(True)
		ax.xaxis.grid(False)
		return ax						
	def _generate_colors(self, bins, kind = 'GraphTV'):
		""" Generates a list of colors to use in the graph
			Parameters
			----------
				bins: iterable
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
			colors = ['#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
					'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
					'#79CEF2']
		else:
			for categ in bins:
				lower = 100
				upper = 256
				red   = random.randrange(lower, upper)
				blue  = random.randrange(lower, upper)
				green = random.randrange(lower, upper)
				color = '#{0:02X}{1:02X}{2:02X}'.format(red, blue, green)
				colors[categ] = color

		return colors

class Show:
	""" Wrapper around the output from the IMDB API. Contains
		convienience methods for accessing show attributes.
		Attributes
		----------
			show: dict<>
				Output from the IMDB API.
	"""
	def __init__(self, show):
		"""
			Parameters
			----------
				show: string, dict<>
					The title or imdbId of a show, or the output from the IMDB API.
		"""
		if isinstance(show, str):
			show = API.find(show)
		self.show = show

		self.episode_order_regex = re.compile("s(?P<season>[\d]+)e(?P<episode>[\d]+)")

	def __call__(self, *args):
		""" Returns a specific episode from the season or a metadata value.
			Parameters
			----------
				one argument retrieves a metadata value, if present, or a season
				notation string of the form SXXEXX. Two areguments designate a
				season and episode value pair to retrieve an episode.
		"""
		if len(args) == 1:
			value = self.show.get(args[0])
		else:
			value = self.selectEpisode(args[0], args[1])
		return value

	def __str__(self):
		string = "Show(id = {0}, title = {1})".format(
			self.show['imdbID'], self.show['Title'])
		return string

	def selectEpisode(self, season, episode):
		""" Finds a specific episode in a series.
			Parameters
			----------
				season: int
				episode: int
					The episode number. May be either the order of
					the episode within the season or the overall index.
			Returns
			-------
				episode: dict<>
		"""
		for element in self.show['episodeList']:
			if element['season'] == season:
				number = element['number']
				index = element['index']
				if number == episode or index == episode:
					return element
		return None

def _removeIllegalCharacters(string):
		for char in ['<', '>', ':', '"','/', '\\', '|', '?', '*']:
			string = string.replace(char, '')
		return string
def parseFolder(show, folder, regex = None, rename = False):
	""" Collects episode names from a folder and retrieves the file names.
		Parameters
			show: string
				The show title or imdbId
			folder: string
				path to a folder
			regex: string
				A regular expression that produces a valid groupdict
				with both 'season' end 'episode' groups for each filename.
				defaults to "(?P<season>s[\d]+)(?P<episode>e[\d]+)"
			rename: bool; default False
				Whether to rename the files.
	"""
	show = Show(show)

	#template = "{0} S{1:>02}E{2:>02} - {3}"
	if regex is None:
		regex = {
			'KEY01': re.compile("s(?P<season>[\d]+)[\s\.]?e[\s]?(?P<episode>[\d]+)"),
			'KEY02': re.compile("(?P<season>[\d]+)x(?P<episode>[\d]+)"),
			'KEY03': re.compile("season[\s](?P<season>[\d]+)[\s]episode[\s](?P<episode>[\d]+)")
		}
	else:
		regex = re.compile(regex)
	for fn in os.listdir(folder):
		ext = os.path.splitext(fn)[-1]
		if isinstance(regex, dict):
			for k, r in regex.items():
				match = r.search(fn.lower())
				if match is not None: break
		else:
			match = regex.search(fn.lower())
		if match is None: continue
		groups = match.groupdict()
		season_number = int(groups['season'])
		episode_number = int(groups['episode'])
		matched_episode = show(season_number, episode_number)
		if matched_episode is None:
			#print("WARNING: Info for {} could not be found!".format(fn))
			template = "{show} S{s:>02}E{e:>02}"
			title = ""
		else:
			template = "{show} S{s:>02}E{e:>02} - {t}"
			title = matched_episode['title']
			title = _removeIllegalCharacters(title)
		dest = template.format(
			show = _removeIllegalCharacters(show('Title')), 
			s = groups['season'], 
			e = groups['episode'], 
			t = title)
		source = os.path.join(folder, fn)
		destination = os.path.join(folder, dest) + ext
		print(source)
		print(destination)
		if rename:
			_filename = os.path.join(folder, 'file_rename_log.txt')
			with open(_filename, 'a') as file1:
				file1.write(source + ' -> ' + destination + '\n')
			os.rename(source, destination)


API = IMDBAPI()
"""Note: The graphTV color scheme only supports up to ~11 seasons, sow shows like supernatural break the program.
"""
if __name__ == "__main__":
	test_id = 'tt2618986'
	result = API.find(test_id)
	pprint(result)
	pprint(requests.get("http://www.omdbapi.com/?i=tt2618986").json())
