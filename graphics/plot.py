import matplotlib.pyplot as plt


class GraphTv:
	def __init__(self, show, ax = None, kind = 'average', show_dots = True, colorscheme = 'GraphTV'):
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
		#episode_df = pandas.DataFrame(show['episodeList'])
		if ax is None:
			self.fig, self.ax = plt.subplots(figsize = (20,10))
			self.fig.patch.set_facecolor('#333333')
		else:
			self.fig = None

		self.ax = self._formatPlot(self.ax)
		
		self.ax = self._plotSeasons(
			self.ax, 
			show['seasons'], 
			show_dots = show_dots
		)
		
		total_episodes = sum(len(s) for s in show['seasons'])

		self.ax.set_xlim((0, total_episodes + 1))
		self.ax.set_ylim(ymax = 10)
		


	def _plotSeasons(self, ax, seasons, show_dots = True):
		""" Plots each season
			Parameters
			----------
				ax: matplotlib.axes._subplots.AxesSubplot
					The plot to add each series to
				seasons: list<list<matplotlib.axes>>
					* 'date': str
					* 'episode': str
						The episode designation. Ex. 'S04E03'
					* 'imdbId': str
					* 'imdbRating': float
					* 'index': int
					* 'name': str
					* 'season': int
					* 'seasonIndex': int
					* 'title': str
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

		for season in seasons:
			x = list(season.index)
			y = list(season.ratings)

			if show_dots:
				ax.scatter(x, y, color = season.color, s = 100)

			season_rating = season.rating

			ax.plot(x, [season_rating for i in x], color = season.color)
		return ax

				
	@staticmethod
	def _formatPlot(ax, style = 'graphtv'):
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



if __name__ == "__main__":
	pass