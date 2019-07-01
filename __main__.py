#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from omdbapi import api
from omdbapi import graphics

def create_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"label",
		help = "The search term."
	)
	parser.add_argument(
		"-m", "--matplotlib",
		help = "Use the matplotlib plotting backend rather than the terminalplot.",
		action = 'store_true',
		dest = 'use_matplotlib_backend'
	)

	return parser


def main():
	parser = create_parser().parse_args()
	search_term = parser.label
	series = api.find(search_term, 'series')
	table = series.toTable()

	if parser.use_matplotlib_backend:
		import matplotlib.pyplot as plt
		graphics.pyplot_plot(table)
		plt.show()
	else:
		#graphics.terminal_plot(table['indexInSeries'].values, table['imdbRating'].values, size = 100)
		graphics.gnu_plot(series)

if __name__ == "__main__":
	main()