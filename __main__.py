#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from omdbapi import api
from omdbapi import graphics
from typing import *

def create_parser(args:Optional[List[str]]) -> argparse.Namespace:
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
	if args:
		result = parser.parse_args(args)
	else:
		result = parser.parse_args()

	return result


def main():
	parameters = ["Designated Survivor"]
	parser = create_parser(parameters)
	search_term = parser.label
	series = api.find(search_term, 'series')
	table = series.toTable()
	print(table.to_string())
	if True:
		import matplotlib.pyplot as plt
		graphics.pyplot_plot(table)
		plt.show()


if __name__ == "__main__":
	main()