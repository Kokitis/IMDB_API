from typing import Union

import pandas
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from omdbapi.api import resources
from omdbapi.graphics.colorscheme import get_colorscheme


def bokeh_plot(series: Union[resources.SeriesResource, pandas.DataFrame], by = 'index'):
	colorscheme = get_colorscheme('graphtv')
	x_variable = 'indexInSeries' if by == 'index' else 'releaseDate'
	plot_width, plot_height = 1280, 720
	if not isinstance(series, pandas.DataFrame):
		series = series.toTable()
	# Add a 'color' column to the dataframe so that bokeh can color the points correctly.
	series['color'] = series['season'].apply(colorscheme.get_color)
	series_title = series['seriesTitle'].iloc[0]
	data = ColumnDataSource(series)
	fig = figure(plot_width = plot_width, plot_height = plot_height, title = series_title)
	fig.background_fill_color = colorscheme.background

	fig.circle(x_variable, 'imdbRating', source = data, color = 'color', size = 20)

	seasons = series.groupby(by = 'season')
	for season_index, season in seasons:
		start = season['indexInSeries'].min()
		stop = season['indexInSeries'].max()
		rating = season['imdbRating'].mean()
		color = season['color'].iloc[0]

		fig.line([start, stop], [rating, rating], line_color = color)
	tooltips = [('episode', '@episodeId - @title'), ('imdbRating', '@imdbRating')]
	hover = fig.add_tools(HoverTool(tooltips = tooltips))

	show(fig)


if __name__ == "__main__":
	from bokeh.models import HoverTool
	from bokeh.io import show
	from omdbapi.api import apiio

	response = apiio.find('legion')
	bokeh_plot(response)
