import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, push_notebook, show
# output to static HTML file
output_file("line.html")

p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

# show the results
show(p)
class SeriesPlot:
	def __init__(self, series, scheme:str = 'graphtv'):
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
		self.figure = figure(plot_width = 400, plot_height = 400)

		for season in series['seasons']:
			episodes = season['episodes']
			x = [episode.indexInSeries for episode in episodes]
			y = [episode.imdbRating for episode in episodes]
			self.figure.circle(x, y, size = 10, alpha = 0.75)
	def render(self):
		pass

if __name__ == "__main__":
	pass

