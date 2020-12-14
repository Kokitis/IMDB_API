import math
import re


import pendulum

def _convert_to_timestamp(value) -> pendulum.Date:
	return pendulum.parse(value) if value != "N/A" else math.nan


def _convert_to_duration(value) -> pendulum.Duration:
	return pendulum.Duration(minutes = int(value.split(' ')[0])) if value != 'N/A' else math.nan


def _is_imdb_id(string) -> bool:
	""" Checks if a given string matches the format of an IMDB string."""
	pattern = "tt[\d]{7,8}"
	return bool(re.search(pattern, string))

def get_ombd_api_key()->str:
	pass