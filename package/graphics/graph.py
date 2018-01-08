import random

import matplotlib.pyplot as plt


class SeriesPlot:
	def __init__(self, series, scheme = 'graphtv', **kwargs):
		""" Plots every episode's rating
			Parameters
			----------
				show: dict<>
					Response from the IMDB API.
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
		self.scheme = scheme.lower()

		self.fig, self.ax = self.plotSeries(series)
		total_episodes = 0
		for i in series['seasons']:
			total_episodes += i['length']
		print("Total Episodes: ", total_episodes)

		self.ax.set_xlim((0, total_episodes + 1))
		self.ax.set_ylim(ymax = 10)

	# return fig, ax

	def plotSeries(self, series):
		""" Plots each season
			Parameters
			----------
				series: dict<>
					Response from the OmdbApi, with include_seasons set to True.
			Returns
			----------
				ax : matplotlib.axes._subplots.AxesSubplot
		"""
		fig, ax = plt.subplots(figsize = (20, 10))
		ax = self._formatPlot(ax)

		for element in series['seasons']:
			season = self._getSeasonParameters(element)
			x = [i[0] for i in season['episodes']]
			y = [i[1] for i in season['episodes']]
			color = season['color']
			regression_y = sum(y) / len(y)
			ax.scatter(x, y, color = color)
			ax.plot([min(x), max(x)], [regression_y, regression_y])

		return fig, ax

	@staticmethod
	def _formatPlot(ax):
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
		return ax

	def _getSeasonParameters(self, season):

		season_color = self._getSeasonColor(season['seasonIndex'])
		season_episodes = [(i['indexInSeries'], i['imdbRating']) for i in season['episodes']]

		season_values = {
			'color':    season_color,
			'episodes': season_episodes,
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


# api = IMDB_API()

"""Note: The graphTV color scheme only supports up to ~11 seasons, sow shows like supernatural break the program.
"""
