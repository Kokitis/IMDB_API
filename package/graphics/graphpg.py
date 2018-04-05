import random
import pygal
from typing import *
import pathlib
class SeriesPlot:
	def __init__(self, series, scheme: str = 'graphtv', **kwargs):
		""" Plots every episode's rating
			Parameters
			----------
				series: MediaResource<>
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

		self.scheme = scheme.lower()
		self.chart = pygal.XY()

		for index, season in enumerate(series['seasons']):
			label = "Season {}".format(index)
			season_parameters = self._getSeasonParameters(season)
			season_episodes = season_parameters['episodes']
			season_mean = sum([i[1] for i in season_episodes]) / len(season_episodes)
			self.chart.add(label, season_episodes)
			self.chart.add(label,[(season_episodes[0][0],season_mean), (season_episodes[0][0], season_mean)])

		self.chart.render_to_file('test_plot.svg')
	@staticmethod
	def _getSeasonParameters(season: Dict):
		season_episodes = [(i['indexInSeries'], i['imdbRating']) for i in season['episodes']]
		season_values = {
			'color': None,
			'episodes': season_episodes
		}
		return season_values
	def save(self):
		filename = pathlib.Path(__file__)
		filename = filename.with_name('testpg.png')
		self.chart.render_to_png(str(filename))

	def render(self):
		html_pygal = """
		<!DOCTYPE html>
		<html>
		  <head>
		  <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/svg.jquery.js"></script>
		  <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js"></script>
		    <!-- ... -->
		  </head>
		  <body>
		    <figure>
		      {pygal_render}
		    </figure>
		  </body>
		</html>
		"""
		html_data = html_pygal.format(pygal_render = self.chart.render())
		return html_data