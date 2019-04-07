import itertools
from typing import Optional, Union

import pandas
import pygal

from omdbapi import table_columns
from omdbapi.graphics.colorscheme import get_colorscheme


def convert_to_pygal_annotation(row: pandas.Series, by: str, color: Optional[str]):
	episode_name = row[table_columns.episode_title]
	episode_index = row[table_columns.episode_id]
	rating = row[table_columns.imdb_rating]
	result = {
		'value': (row[by], rating),
		'label': f"{episode_index}: {episode_name} - {rating}"
	}
	if color:
		result['color'] = color
	return result


def plot_series(series: Union[pandas.DataFrame], by: str = 'index'):
	if not isinstance(series, pandas.DataFrame):
		series = series.toTable()
	x_variable = table_columns.index_in_series if by == 'index' else table_columns.release_date
	current_colorscheme = get_colorscheme('graphtv')

	# Set up a custom pygal style so that both episodes and season series are the correct color.
	custom_pygal_style = pygal.style.Style(
		colors = list(itertools.chain.from_iterable([(i, i) for i in current_colorscheme.palette]))
	)
	series_title = series[table_columns.series_title].iloc[0]
	xy_chart = pygal.XY(stroke = False, style = custom_pygal_style)
	xy_chart.title = series_title
	seasons = series.groupby(table_columns.season_index)
	for index, season in seasons:
		color = current_colorscheme.get_color(index)
		y = season[table_columns.imdb_rating].mean()
		data = [convert_to_pygal_annotation(row, x_variable, None) for _, row in season.iterrows()]
		xy_chart.add('', data)
		xy_chart.add(
			f"season {index}",
			[(season[x_variable].min(), y), (season[x_variable].max(), y)]
			, stroke = True, show_dots = False)


# xy_chart.render_to_file('chart.svg')

if __name__ == "__main__":
	from omdbapi import apiio

	response = apiio.find('Legion')
	plot_series(response)
