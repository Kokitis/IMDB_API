from typing import *
from omdbapi.api import resources
import pandas
from pprint import pprint
def to_table(series: resources.SeriesResource)->pandas.DataFrame:

	table = pandas.DataFrame(series['episodes'])
	table['seriesTitle'] = series['title']
	table['seriesId'] = series['imdbId']

	return table


if __name__ == "__main__":
	from omdbapi import api
	imdb_id = "tt0965394"

	result = api.get(imdb_id)

	to_table(result)
