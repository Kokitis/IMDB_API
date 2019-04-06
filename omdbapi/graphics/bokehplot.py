from typing import Union

import pandas
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from omdbapi import MediaResource, table_columns
from omdbapi.graphics.colorscheme import get_colorscheme


def plot_series(series: Union[MediaResource, pandas.DataFrame], by = 'index'):
	colorscheme = get_colorscheme('graphtv')
	x_variable = table_columns.index_in_series if by == 'index' else table_columns.release_date
	plot_width, plot_height = 1280, 720
	if not isinstance(series, pandas.DataFrame):
		series = series.toTable()
	# Add a 'color' column to the dataframe so that bokeh can color the points correctly.
	series['color'] = series[table_columns.season_index].apply(colorscheme.get_color)
	series_title = series[table_columns.series_title].iloc[0]
	data = ColumnDataSource(series)
	fig = figure(plot_width = plot_width, plot_height = plot_height, title = series_title)
	fig.background_fill_color = colorscheme.background

	fig.circle(x_variable, table_columns.imdb_rating, source = data, color = 'color', size = 20)

	seasons = series.groupby(by = table_columns.season_index)
	for season_index, season in seasons:
		start = season[table_columns.index_in_series].min()
		stop = season[table_columns.index_in_series].max()
		rating = season[table_columns.imdb_rating].mean()
		color = season['color'].iloc[0]

		fig.line([start, stop], [rating, rating], line_color = color)
	tooltips = [('episode', '@episodeId - @title'), ('imdbRating', '@imdbRating')]
	hover = fig.add_tools(HoverTool(tooltips = tooltips))

	show(fig)


if __name__ == "__main__":
	from bokeh.models import HoverTool
	from bokeh.io import show
	from omdbapi import omdb_api

	response = omdb_api.find('legion')
	plot_series(response)
