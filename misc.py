import re
from pprint import pprint
pprint('')
import pandas
import pendulum
import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from omdbapi import api, graphics

def convert_duration(value:str):
	duration = value.split(':')
	duration = [int(i.strip()) for i in duration]
	if len(duration) == 3:
		hours, minutes, seconds = duration
	elif len(duration) == 2:
		hours = 0
		minutes, seconds = duration
	elif len(duration) == 1:
		hours = minutes = 0
		seconds = duration[0]
	else:
		message = f"Duration: '{duration}'"
		raise ValueError(message)
	seconds = (hours * 3600) + (minutes * 60) + seconds
	duration = datetime.timedelta(seconds = seconds)
	return duration

def main():
	series_id = 'tt1312171'
	response = api.get(series_id)

	pprint(response)

	seasons = api.get_seasons(series_id)
	seasons = pandas.DataFrame(seasons)
	seasons['seriesTitle'] = response['title']
	print(seasons.to_string())

	graphics.pyplot_plot(seasons)
	plt.show()

if __name__ == "__main__":
	main()



