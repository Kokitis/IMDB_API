import random
import math
import matplotlib.pyplot as plt
from matplotlib.figure import Axes, Figure
from omdbapi import MediaResource, SeasonResource
from typing import Any, Dict, Union, Tuple, List, NewType
from pathlib import Path
from dataclasses import dataclass

def checkValue(value:str, *items)->str:
	""" Raises a ValueError if 'value' is not in 'items'"""
	value = value.lower()
	if value not in items:
		message = "'{}' is not an available option. Expected one of {}".format(value, items)
		raise ValueError(message)
	return value

@dataclass
class ColorScheme:
	name: str
	palette: List[str]
	background: str
	ticks: str
	font: str

_colorschemes: List[ColorScheme] = [
	ColorScheme('graphtv',
		palette = [
			'#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
			'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
			'#79CEF2'
			],
		background = "#333333",
		ticks = "#999999",
		font = "#999999"

	)
]
colorschemes:Dict[str,ColorScheme] = {i.name: i for i in _colorschemes}


def get_plot_formatting(ax:Axes, series:MediaResource, index_attribute:str, by:str, scheme:str)->Axes:
	""" Formats the plot aesthetics
		Parameters
		----------
		ax: matplotlib.axes._subplots.AxesSubplot
			The plot to format
		Returns
		----------
		ax : matplotlib.axes._subplots.AxesSubplot
	"""
	color_scheme_label = scheme if scheme in colorschemes else 'graphtv'
	color_scheme = colorschemes.get(color_scheme_label)
	background_color = color_scheme.background
	tick_color = color_scheme.ticks
	font_color = color_scheme.font

	ax.patch.set_facecolor(background_color)
	ax.spines['bottom'].set_color(background_color)
	ax.spines['top'].set_color(background_color)
	ax.spines['left'].set_color(background_color)
	ax.spines['right'].set_color(background_color)

	# change the label colors
	[i.set_color(tick_color) for i in plt.gca().get_yticklabels()]
	[i.set_color(tick_color) for i in plt.gca().get_xticklabels()]

	# Change tick size
	ax.tick_params(axis = 'y', which = 'major', labelsize = 22)
	ax.tick_params(axis = 'y', which = 'minor', labelsize = 22)
	ax.yaxis.grid(True)
	ax.xaxis.grid(False)

	# Add series parameters
	episode_indicies = [
		float(episode[index_attribute]) for season in series.seasons for episode in season
	]

	# Set plot bounds

	x_min = min(episode_indicies)
	x_max = max(episode_indicies)

	if by == 'index':
		x_max += 1
	else:
		x_min -= 1 / 12
		x_max += 1 / 12

	ax.set_xlim((x_min, x_max))
	ax.set_ylim(ymax = 10)

	plt.xlabel(index_attribute, fontsize = 16, color = font_color)
	plt.ylabel('imdbRating', fontsize = 16, color = font_color)
	plt.title(series.title, fontsize = 24, color = font_color)

	return ax
def get_season_color_from_palette(self, index:int)->str	:
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
				- fig: matplotlib.figure.Figure
					The pyplot figure object that contains the graph
				- ax:  matplotlib.axes._subplots.AxesSubplot
					The ax obbject that contains the graph
		"""
		# series_info = show.summary()
		self.scheme = checkValue(scheme, 'graphtv')
		self.by = checkValue(by, 'index', 'date')
		self.x_variable = 'indexInSeries' if self.by == 'index' else 'releaseDate'

		self.fig, self.ax = self.plotSeries(series)

		self.ax = get_plot_formatting(self.ax, series, self.x_variable, self.by, self.scheme)
	# return fig, ax

	def plotSeries(self, series:MediaResource)->Tuple[Figure, Axes]:
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

		for element in series.seasons:
			color, regression_y, x, y = self._getSeasonParameters(element)

			ax.scatter(x, y, color = color)
			ax.plot([min(x), max(x)], [regression_y, regression_y], color = color)

		return fig, ax




	def _getSeasonParameters(self, season:SeasonResource) -> Tuple[str,float,List[int], List[float]]:
		season_color = get_season_color_from_palette(season.seasonIndex)
		season_episodes = [(i[self.x_variable], i.imdbRating) for i in season.episodes]
		_i = [i[1] for i in season_episodes if not math.isnan(i[1])]
		season_mean = sum(_i) / len(_i)
		x, y = zip(*season_episodes)

		return season_color, season_mean, x, y



	def save(self, filename:Union[str,Path]):
		plt.savefig(str(filename), dpi = 250)