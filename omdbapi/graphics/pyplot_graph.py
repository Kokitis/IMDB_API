import matplotlib.pyplot as plt
from matplotlib.figure import Axes, Figure
from omdbapi import MediaResource, table_columns

import pandas

try:
	from .colorscheme import get_colorscheme, ColorScheme
except ModuleNotFoundError:
	from colorscheme import get_colorscheme, ColorScheme


def checkValue(value: str, *items) -> str:
	""" Raises a ValueError if 'value' is not in 'items'"""
	value = value.lower()
	if value not in items:
		message = "'{}' is not an available option. Expected one of {}".format(value, items)
		raise ValueError(message)
	return value


def get_plot_formatting(ax: Axes, series: pandas.DataFrame, index_attribute: str, color_scheme: ColorScheme) -> Axes:
	""" Formats the plot aesthetics
		Parameters
		----------
		ax: matplotlib.axes._subplots.AxesSubplot
			The plot to format
		series: pandas.DataFrame
			The table representation of the series. Used to determin the episode indicies and title of the plot.
		index_attribute: {'indexInSeason', 'releaseDate'}
			The x_variable used when plotting the episodes.
		color_scheme: ColorScheme
			The colorscheme being used.
		Returns
		----------
		ax : matplotlib.axes._subplots.AxesSubplot
	"""
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

	# Set plot bounds
	series_title = series[table_columns.series_title].iloc[0]
	indicies = series[index_attribute].apply(float)
	x_min: int = min(indicies)
	x_max: int = max(indicies)

	# Add some spacing so the points don't overlap the plot edge.
	if index_attribute == table_columns.index_in_series:
		x_max += 1
	else:
		x_min -= 1 / 12
		x_max += 1 / 12

	ax.set_xlim(left = x_min, right = x_max)
	ax.set_ylim(top = 10)

	plt.xlabel(index_attribute, fontsize = 16, color = font_color)
	plt.ylabel(table_columns.imdb_rating, fontsize = 16, color = font_color)
	plt.title(series_title, fontsize = 24, color = font_color)

	return ax


def plot_series(series: pandas.DataFrame, scheme: str = 'graphtv', by = 'index'):
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
	if not isinstance(series, pandas.DataFrame):
		series = series.toTable()

	scheme = checkValue(scheme, 'graphtv')
	by = checkValue(by, 'index', 'date')
	x_variable = table_columns.index_in_series if by == 'index' else table_columns.release_date
	current_colorscheme = get_colorscheme(scheme)
	fig, ax = plt.subplots(figsize = (20, 10))

	seasons = series.groupby(by = table_columns.season_index)
	for index, season in seasons:
		x = season[x_variable].apply(float)  # To convert Timestamp to a regular number.
		y = season[table_columns.imdb_rating]
		color = current_colorscheme.get_color(index)
		# plot all episodes in the season.
		ax.scatter(x.values, y.values, color = color)
		# Plot the mean rating of the season
		ax.plot([x.min(), x.max()], [y.mean(), y.mean()], color = color)
	ax = get_plot_formatting(ax, series, x_variable, current_colorscheme)

	return fig, ax


if __name__ == "__main__":
	from omdbapi.api import omdb_api

	response = omdb_api.find('Legion')
	plot_series(response)
	print(response.toTable().to_string())
	plt.show()