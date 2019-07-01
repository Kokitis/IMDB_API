
import os

import pandas


def gnu_plot(series):
	import gnuplotlib # Avoids ImportError when using conda environments
	if isinstance(series, pandas.DataFrame):
		table = series
	else:
		table = series.toTable()

	terminal_size = os.get_terminal_size()
	terminal_width = terminal_size.columns
	terminal_height = terminal_size.lines - 10

	seasons = table.groupby(by = 'seasonIndex')
	data = list()
	for index, season in seasons:
		data.append((season['indexInSeries'], season['imdbRating'], {'with': 'points'}))

	gnuplotlib.plot(
		*data,
		title = series.title,
		terminal = f'dumb {terminal_width} {terminal_height}',
		unset = ['grid'],
		tuplesize = 2
	)
