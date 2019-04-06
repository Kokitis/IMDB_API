import math
import re

from omdbapi.github import numbertools, timetools

to_number = numbertools.to_number


def _convert_to_timestamp(value) -> timetools.Timestamp:
	return timetools.Timestamp(value) if value != "N/A" else math.nan


def _convert_to_duration(value) -> timetools.Duration:
	return timetools.Duration(minutes = int(value.split(' ')[0])) if value != 'N/A' else math.nan


def _is_imdb_id(string) -> bool:
	""" Checks if a given string matches the format of an IMDB string."""
	pattern = "tt[\d]{7}"
	return bool(re.search(pattern, string))
