from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, Tuple

import pandas

from pytools import timetools


class TableColumns(NamedTuple):
	episode_id: str = 'episodeId'
	imdb_id: str = 'imdbId'
	imdb_rating: str = 'imdbRating'
	index_in_season: str = 'indexInSeason'
	index_in_series: str = 'indexInSeries'
	release_date: str = 'releaseDate'
	season_index: str = 'season'
	series_id: str = 'seriesId'
	series_title: str = 'seriesTitle'
	episode_title: str = 'title'


table_columns = TableColumns()


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

	def to_dict(self) -> Dict:
		return {
			table_columns.episode_title:   self.title,
			table_columns.imdb_rating:     self.imdbRating,
			table_columns.release_date:    self.releaseDate,
			table_columns.episode_id:      self.episodeId,
			table_columns.index_in_series: self.indexInSeries,
			table_columns.index_in_season: self.indexInSeason,
			'imdbId':                      self.imdbId
		}


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
	# Common fields between Movies and Series
	actors: List[str]
	awards: str
	country: str
	director: str
	duration: timetools.Duration
	genres: List[str]
	imdbId: str
	imdbRating: float
	imdbVotes: int
	language: str
	metascore: float
	plot: str
	poster:str
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
		class_name = self.__class__.split('.')[-1]
		string = f"{class_name}('{self.title}')"
		return string


class SeriesResource(MediaResource):
	aired: Tuple[timetools.Timestamp, Optional[timetools.Timestamp]]
	totalSeasons: int
	seasons: List[SeasonResource]

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
		""" Converts the MediaResource Series to a pandas.DataFrame object.

		Returns
		-------
		pandas.DataFrame
			A table with rows corresponding to individual episodes.
			columns:
				`episodeId`
				`imdbRating`
				`indexInSeason`
				`indexInSeries`
				`releaseDate`
				`season`
				`seriesId`
				`seriesTitle`
				`title`
			index: `imdbId`
		"""
		series_title = self.title
		series_id = self.imdbId

		table = list()
		for season in self.seasons:
			season_index = season.seasonIndex
			for episode in season:
				element = episode.to_dict()
				element[table_columns.series_title] = series_title
				element[table_columns.series_id] = series_id
				element[table_columns.season_index] = season_index
				table.append(element)
		df = pandas.DataFrame(table)
		df = df.set_index(table_columns.imdb_id)
		df = df[list(i for i in table_columns if i != table_columns.imdb_id)]
		df[table_columns.season_index] = df[table_columns.season_index].astype(int)
		return df


class FilmResource(MediaResource):
	boxOffice: int
	dvd: timetools.Timestamp

class EpisodeResource(MediaResource):
	indexInSeason: int = 0
	indexInSeries: int = 0
	episodeId: str = 'N/A'

if __name__ == "__main__":
	class ABCClass:
		pass
	print(ABCClass().__class__)