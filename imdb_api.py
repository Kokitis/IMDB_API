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

#import timetools as tt
import scipy.stats as stats
from pprint import pprint
from itertools import chain
#import seaborn as sns
plt.style.use('fivethirtyeight')

class IMDBAPI:
	def __init__(self):
		pass

	def _parseResponse(self, response):
		response['Response'] = response['Response'] == 'True'
		return response
	def _parseSeasons(self, seasons):
		new_seasons = list()
		episode_number = 0
		for season in seasons:
			season_num = self._tonum(season['Season'])
			episodes = season['Episodes']
			new_episodes = list()
			for episode in episodes:
				episode_number += 1
				episode['Episode'] = self._tonum(episode['Episode'])
				episode['episodeNumber'] = "S{0:>02}E{1:>02}".format(season_num, episode['Episode'])
				episode['episodeOrder'] = episode_number
				episode['imdbRating'] = self._tonum(episode['imdbRating'])
				new_episodes.append(episode)
			new_season = {
				'Episodes': new_episodes,
				'Response': season['Response'],
				'Season': self._tonum(season['Season']),
				'Title': season['Title'],
				'totalSeasons': self._tonum(season['totalSeasons'])
			}
			new_seasons.append(new_season)
		return new_seasons
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
		endpoint = "http://www.omdbapi.com/"
		response = requests.get(endpoint, parameters)
		response = response.json()
		response = self._parseResponse(response)
		return response

	def find(self, title):
		""" Searches the IMDB database and returns the first result found.
			Parameters
			----------
				title: string
					The title of a Movie, TV show, or episode. 
			Returns
			----------
				series : dict<> (from self.by_uid())
				If the series is not found, returns
				{'Response': 'False', 'Error': 'Movie not found!'}
		"""
		
		response = self.search(s = title)
		
		first_id = response['Search'][0]['imdbID']
		first_show = self._request(
			i = first_id,
			tomatoes = True)
		first_show['Seasons'] = self.getSeasons(i = first_id)

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
				#url = self.root_url + "i={0}&season={1}".format(i = imdbID, season = season_number)
				response = self._request(i = imdbID, season = season_number)
				if 'Error' in response.keys(): break
				seasons.append(response)
			seasons = self._parseSeasons(seasons)
			return seasons



class Parser:
	""" Accesses the IMDB database via the Open Movie Database API
		Site: http://www.omdbapi.com/"""
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
			elif ext in {'.xls', 'xlsx'}
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
		_num_episodes = 0
		#series_info = show.summary()
		
		if ax is None:
			colors  = self._generate_colors(response = show, kind = colorscheme)
			self.fig, self.ax = plt.subplots(figsize = (20,5))
			self.fig.patch.set_facecolor('#333333')
		else:
			colors = self._generate_colors(response = show, kind = 'random')
			self.fig = None
		self.ax = self._format_ax(self.ax)
		
		#Plot the individual seasons
		
		#seasons = self._get_seasons()
		seasons = show['Seasons']
		self.ax      = self._plot_seasons(self.ax, seasons, colors, 
						regression_type = kind, show_dots = show_dots)
		
		total_episodes = sum(len(s['Episodes']) for s in seasons)
		print("Total Episodes: ", total_episodes)
		self.ax.set_xlim((0, total_episodes + 1))
		self.ax.set_ylim(ymax = 10)
		
		#return fig, ax

	def _plot_seasons(self, ax, seasons, colors, regression_type = 'linear', show_dots = True):
		""" Plots each season
			Parameters
			----------
				ax: matplotlib.axes._subplots.AxesSubplot
					The plot to add each series to
				seasons: list of dicts
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
		
		for index, season in enumerate(seasons):
			season = season['Episodes']
			season = [(episode['episodeOrder'], episode['imdbRating']) for episode in season]
			x, y = zip(*season)
			#print(y)
			if show_dots:
				ax.scatter(x, y, color = colors[index], s = 100)
			series = [(i, j) for i, j in zip(x, y) if j is not None]
			if len(series) > 0:
				rseries = self._calculate_regression(series, kind = regression_type)
				x, y = zip(*rseries)
				ax.plot(x, y, color = colors[index])
		return ax
	@staticmethod
	def _calculate_regression(series, kind = 'average'):
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
	def _generate_colors(self, response, kind = 'GraphTV'):
		""" Generates a list of colors to use in the graph
			Parameters
			----------
				kind: {'GraphTV', 'random'}; default 'GraphTV'
					The color map to use
					*'GraphTV': The series of colors used on the GraphTV webpage
					*'random': A randomly generated series of colors
		"""
		colors = list()
		if kind == 'GraphTV':
			colors = ['#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
					'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
					'#79CEF2']
		else:
			for season in response['Seasons']:
				lower = 100
				upper = 256
				red   = random.randrange(lower, upper)
				blue  = random.randrange(lower, upper)
				green = random.randrange(lower, upper)
				color = '#{0:02X}{1:02X}{2:02X}'.format(red, blue, green)
				colors.append(color)

		return colors

#api = IMDB_API()

"""Note: The graphTV color scheme only supports up to ~11 seasons, sow shows like supernatural break the program.
"""
if __name__ == "__main__":
	api = IMDBAPI()
	title = 'Blindspot'

	response = api.find(title)
	#pprint(response)
	graph = GraphTV(show = response, kind = 'average', colorscheme = 'random')
	plt.show()
