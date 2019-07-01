from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


import pandas
import pendulum


@dataclass
class MiniEpisodeResource:
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: pendulum.Date
	episodeId: str
	seasonIndex:int
	indexInSeries: int
	indexInSeason: int

	def __str__(self):
		string = "EpisodeResource({} - {})".format(self.episodeId, self.title)
		return string
	@property
	def imdb_rating(self)->float:
		return self.imdbRating

@dataclass
class MediaResource:
	# Common fields between Movies and Series
	actors: List[str]
	awards: str
	country: str
	director: str
	duration: pendulum.Duration
	genres: List[str]
	imdbId: str
	language: str
	plot: str
	poster: str
	rated: str
	ratings: List[Dict[str, float]]
	releaseDate: pendulum.Date
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
	years: Tuple[int, Optional[int]]
	totalSeasons: int
	episodes: List[MiniEpisodeResource]

	def summary(self, level: int = 0):
		""" prints a summary of the media. 'level' indicates the indentation level to use."""
		indent = '' if level == 0 else '\t' * level
		print(indent, self)
		print(indent, "\timdbId:     ", self.imdbId)
		#print(indent, "\tyear(s):    ", self.years)
		print(indent, "\tduration    ", self.duration)
		print(indent, "\timdbRating: ", self.imdb_rating)
		print(indent, "\tPlot:       ", self.plot)


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
	releaseDateHome: pendulum.Date
	year: int
	production: Optional[str]


@dataclass
class EpisodeResource(MediaResource):
	seasonIndex: int
	indexInSeries: int
	seriesId: str
