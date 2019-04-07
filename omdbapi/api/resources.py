from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, NamedTuple

import pandas

from pytools import timetools


@dataclass
class MiniEpisodeResource:
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: timetools.Timestamp
	episodeId: str
	seasonIndex:int
	indexInSeries: int
	indexInSeason: int

	def __str__(self):
		string = "EpisodeResource({} - {})".format(self.episodeId, self.title)
		return string


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
	language: str
	plot: str
	poster: str
	rated: str
	ratings: List[Dict[str, float]]
	releaseDate: timetools.Timestamp
	responseStatus: bool
	title: str

	type: str
	writer: str
	website: Optional[str]

	def __str__(self):
		class_name = self.__class__.split('.')[-1]
		string = f"{class_name}('{self.title}')"
		return string

	def imdb_rating(self) -> float:
		r = [i for i in self.ratings if i['source'] == 'Internet Movie Database'][0]['rating']
		return r


@dataclass
class SeriesResource(MediaResource):
	years: Tuple[timetools.Timestamp, Optional[timetools.Timestamp]]
	totalSeasons: int
	episodes: List[MiniEpisodeResource]

	def get_episode(self, key: str) -> MiniEpisodeResource:
		""" Retrives an episode based on SnnEnn"""

		season_number, episode_number = key.lower().split('e')
		season = self.get_season(season_number)
		if season is None:
			episode = None
		else:
			episode = season.get_episode(int(episode_number))

		return episode

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
		for episode in self.episodes:
			element = asdict(episode)
			element['seriesTitle'] = series_title
			element['seriesId'] = series_id
			element['season'] = episode.seasonIndex
			table.append(element)
		df = pandas.DataFrame(table)

		df = df.set_index('imdbId')
		return df


@dataclass
class FilmResource(MediaResource):
	boxOffice: int
	releaseDateHome: timetools.Timestamp
	year: int
	production: Optional[str]


@dataclass
class EpisodeResource(MediaResource):
	indexInSeason: int = 0
	indexInSeries: int = 0
	episodeId: str = 'N/A'
