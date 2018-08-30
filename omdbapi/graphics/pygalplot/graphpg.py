import random
import pygal
from pygal.style import NeonStyle
import pathlib
from pprint import pprint
import math

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
		self.chart = pygal.XY(style = NeonStyle)

		for season in series['seasons']:
			#label = "Season {}".format(series['seasonIndex'])
			season_parameters = self._getEpisodeParameters(season['episodes'])
			season_episodes = season_parameters['episodes']
			if len(season_episodes) == 0: continue


			season_mean = season_parameters['mean']
			trendline_start = (season_episodes[0]['value'][0], season_mean)
			trendline_end = (season_episodes[-1]['value'][0], season_mean)
			trendline = [trendline_start, trendline_end]
			print(trendline)
			self.chart.add('', season_episodes)
			self.chart.add('',trendline)

	@staticmethod
	def _getEpisodeParameters(season):
		season_values = list()
		total = 0
		index = 0
		for episode in season:
			rating = episode['imdbRating']
			ep = {
				#'x': episode['indexInSeries'],
				'value': (episode['indexInSeries'], rating),
				'label': episode['title']
			}
			if not math.isnan(rating):
				season_values.append(ep)
				total += rating
				index += 1
		if index == 0:
			mean = None
		else:
			mean = total/index
		season_parameters = {
			'episodes': season_values,
			'mean': mean
		}
		return season_parameters
	def save(self):
		filename = pathlib.Path(__file__)
		svgfilename = filename.with_name('testpg.svg')
		print(svgfilename)
		self.chart.render_to_file(svgfilename)


