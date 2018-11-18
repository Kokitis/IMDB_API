from typing import Dict, List
import pandas

from pathlib import Path
from pytools import timetools
from pytools.datatools import dataclass

@dataclass
class EpisodeResource:
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: timetools.Timestamp
	episodeId: str
	indexInSeries: int
	indexInSeason: int

	def __str__(self):
		string = "EpisodeResource({} - {})".format(self.episodeId, self.title)
		return string


@dataclass
class SeasonResource:
	episodes: List[EpisodeResource]
	seasonIndex: int
	length: int
	seriesTitle: str

	def __str__(self):
		string = "SeasonResource(S{} - {})".format(self.seasonIndex, self.seriesTitle)
		return string

	def __iter__(self):
		for i in self.episodes:
			yield i

	def get_episode(self, key):
		candidates = [i for i in self.episodes if i.indexInSeason == int(key)]

		if len(candidates) == 0:
			episode = None
		else:
			episode = candidates[0]
		return episode

	def summary(self, level: int = 0) -> None:
		missing_string = "<--missing-->"
		indent = '' if level == 0 else '\t' * level
		print(indent, self)
		index = None
		for episode in self.episodes:
			if index is not None:
				distance = episode.indexInSeries - index - 1
				if distance > 0:
					print(indent + "\t " + "\n{}\t ".format(indent).join(missing_string for i in range(distance)))
			index = episode.indexInSeries

			print(indent + '\t', episode)


@dataclass
class MediaResource:
	actors: str
	awards: str
	country: str
	director: str
	duration: timetools.Duration
	genre: str
	imdbId: str
	imdbRating: float
	imdbVotes: int
	language: str
	metascore: float
	plot: str
	rating: str
	ratings: List[Dict[str, str]]
	releaseDate: timetools.Timestamp
	responseStatus: bool
	title: str

	type: str
	writer: str
	year: str

	# Only useful for 'series' objects.
	totalSeasons: int = 0
	seasons: List[SeasonResource] = None

	# Only useful for 'episode' objects.
	indexInSeason: int = 0
	indexInSeries: int = 0
	episodeId: str = 'N/A'

	def __str__(self):
		string = "MediaResource('{}', '{}')".format(self.type, self.title)
		return string

	def get_episode(self, key: str) -> EpisodeResource:
		""" Retrives an episode based on SnnEnn"""

		season_number, episode_number = key.lower().split('e')
		season = self.get_season(season_number)
		if season is None:
			episode = None
		else:
			episode = season.get_episode(int(episode_number))

		return episode

	def get_season(self, key: str) -> SeasonResource:
		"""Retrieves a season. Key should be formatted as Sn"""
		try:
			season_number = int(key[1:])
			season = self.seasons[season_number - 1]
		except IndexError:
			season = None
		return season

	def summary(self, level: int = 0):
		""" prints a summary of the media. 'level' indicates the indentation level to use."""
		indent = '' if level == 0 else '\t' * level
		print(indent, self)
		print(indent, "\timdbId:     ", self.imdbId)
		print(indent, "\tyear(s):    ", self.year)
		print(indent, "\tduration    ", self.duration)
		print(indent, "\timdbRating: ", self.imdbRating)
		print(indent, "\tPlot:       ", self.plot)
		if self.seasons:
			for season in self.seasons:
				season.summary(level + 1)

	def toTable(self) -> pandas.DataFrame:
		series_title = self.title
		series_id = self.imdbId

		table = list()
		for season in self.seasons:
			season_index = season.seasonIndex
			for episode in season:
				element = asdict(episode)
				element['seriesTitle'] = series_title
				element['seriesId'] = series_id
				element['season'] = season_index
				table.append(element)

		return pandas.DataFrame(table)

