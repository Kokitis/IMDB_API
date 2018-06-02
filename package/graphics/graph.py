import random
import math
import matplotlib.pyplot as plt

from typing import *


def checkValue(value, *items):
	""" Raises a ValueError if 'value' is not in 'items'"""
	value = value.lower()
	if value not in items:
		message = "'{}' is not an available option. Expected one of {}".format(value, items)
		raise ValueError(message)
	return value


class SeriesPlot:
	def __init__(self, series, scheme: str = 'graphtv', by = 'index', **kwargs):
		""" Plots every episode's rating
			Parameters
			----------
				series: MediaResource
					Response from the IMDB API.
				scheme: {'graphtv'}
				by: {'index', 'date'}
				ax: matplotlib.axes._subplots.AxesSubplot; default None
					If provided, the graph to plot the episode rating on.
					If not provided, a new one will be created
			Returns
			----------
				fig, ax :  tuple
					*fig: matplotlib.figure.Figure
						The pyplot figure object that contains the graph
					*ax:  matplotlib.axes._subplots.AxesSubplot
						The ax obbject that contains the graph
		"""
		# series_info = show.summary()
		self.scheme = checkValue(scheme, 'graphtv')
		self.by = checkValue(by, 'index', 'date')

		self.x_variable = 'indexInSeries' if self.by == 'index' else 'releaseDate'

		if self.by not in {'index', 'date'}:
			raise ValueError

		self.fig, self.ax = self.plotSeries(series)
		self.ax = self._formatPlot(self.ax, series)
	# return fig, ax

	def plotSeries(self, series):
		""" Plots each season
			Parameters
			----------
			series: MediaResource
				Response from the OmdbApi, with include_seasons set to True.
			Returns
			----------
			ax : matplotlib.axes._subplots.AxesSubplot
		"""
		fig, ax = plt.subplots(figsize = (20, 10))
		#ax = self._formatPlot(ax)

		for element in series['seasons']:
			season = self._getSeasonParameters(element)
			x = [i[0] for i in season['episodes']]

			y = [i[1] for i in season['episodes']]
			color = season['color']
			regression_y = season['mean']

			ax.scatter(x, y, color = color)
			ax.plot([min(x), max(x)], [regression_y, regression_y], color = color)

		return fig, ax

	def _formatPlot(self, ax, series):
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

		# change the label colors
		[i.set_color("#999999") for i in plt.gca().get_yticklabels()]
		[i.set_color("#999999") for i in plt.gca().get_xticklabels()]

		# Change tick size
		ax.tick_params(axis = 'y', which = 'major', labelsize = 22)
		ax.tick_params(axis = 'y', which = 'minor', labelsize = 22)
		ax.yaxis.grid(True)
		ax.xaxis.grid(False)

		# Add series parameters

		episode_indicies = [
			float(episode[self.x_variable]) for season in series.seasons for episode in season
		]

		# Set plot bounds

		x_min = min(episode_indicies)
		x_max = max(episode_indicies)

		if self.by == 'index':
			x_max += 1
		else:
			x_min -= 1 / 12
			x_max += 1 / 12

		ax.set_xlim((x_min, x_max))
		ax.set_ylim(ymax = 10)

		plt.xlabel(self.x_variable, fontsize = 16, color = "#999999")
		plt.ylabel('imdbRating', fontsize = 16, color = "#999999")
		plt.title(series.title, fontsize = 24, color = "#999999")


		return ax

	def _getSeasonParameters(self, season) -> Dict[str, Any]:
		season_color = self._getSeasonColor(season['seasonIndex'])
		season_episodes = [(i[self.x_variable], i['imdbRating']) for i in season['episodes']]
		_i = [i[1] for i in season_episodes if not math.isnan(i[1])]

		season_values = {
			'color':    season_color,
			'episodes': season_episodes,
			'mean': sum(_i) / len(_i)
		}
		return season_values

	def _getSeasonColor(self, index):
		""" Generates a list of colors to use in the graph
			Parameters
			----------
				index: int
		"""
		colorschemes = {
			'graphtv': [
				'#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
				'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
				'#79CEF2'
			]
		}
		if self.scheme in colorschemes:
			colors = colorschemes[self.scheme]
			color = colors[index % len(colors)]

		else:
			lower = 100
			upper = 256
			red = random.randrange(lower, upper)
			blue = random.randrange(lower, upper)
			green = random.randrange(lower, upper)
			color = '#{0:02X}{1:02X}{2:02X}'.format(red, blue, green)

		return color

