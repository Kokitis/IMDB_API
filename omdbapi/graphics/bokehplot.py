from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from omdbapi import MediaResource
from omdbapi.graphics import colorscheme

def plot_series(series:MediaResource):
	plot_width, plot_height = 1280, 720
	series_df = series.toTable()
	series_df['color'] = [colorscheme.GRAPHTV.get_season_color(i).to_hex() for i in series_df['season'].tolist()]
	data = ColumnDataSource(series_df)
	fig = figure(plot_width = plot_width, plot_height = plot_height, title = series.title)
	fig.background_fill_color = colorscheme.GRAPHTV.background.to_hex()

	fig.circle('indexInSeries', 'imdbRating', source = data, color = 'color', size = 20)

	seasons = series_df.groupby(by = 'season')
	for season_index, season in seasons:
		start = season['indexInSeries'].min()
		stop = season['indexInSeries'].max()
		rating = season['imdbRating'].mean()
		color = colorscheme.GRAPHTV.get_season_color(season_index).to_hex()

		fig.line([start, stop], [rating, rating], line_color = color)
	tooltips = [('episode', '@episodeId - @title'), ('imdbRating', '@imdbRating')]
	hover = fig.add_tools(HoverTool(tooltips=tooltips))

	show(fig)

if __name__ == "__main__":
	from bokeh.models import HoverTool
	from bokeh.io import show
	from omdbapi import OmdbApi
	api = OmdbApi()
	response = api.find('legion')
	plot_series(response)
