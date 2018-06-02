from dataclasses import dataclass, fields, asdict
import pendulum
from typing import Dict, List
import pandas


class BasicResource:

	def __post_init__(self):
		self._keys = tuple(i.name for i in fields(self))
		for field in fields(self):
			self._checkType(field)

	def __getitem__(self, item):
		if item not in self.keys():
			message = "'{}' does not exist in the keys.".format(item)
			raise KeyError(message)
		return getattr(self, item)

	def _checkType(self, field):
		value = self[field.name]
		try:
			if not isinstance(value, field.type):
				message = f"Expected type '{field.type}' in field '{field.name}', got '{value}' instead."

				print("WARNING: ", message)
		except TypeError:
			# isinstance doesn't work with parametrized generics.
			pass

	def keys(self):
		return self._keys


@dataclass
class EpisodeResource(BasicResource):
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: pendulum
	episodeId: str
	indexInSeries: int
	indexInSeason: int

	def __str__(self):
		string = "EpisodeResource({} - {})".format(self.episodeId, self.title)
		return string


@dataclass
class SeasonResource(BasicResource):
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
class MediaResource(BasicResource):
	actors: str
	awards: str
	country: str
	director: str
	duration: pendulum.Interval
	genre: str
	imdbId: str
	imdbRating: float
	imdbVotes: int
	language: str
	metascore: float
	plot: str
	rating: str
	ratings: List[Dict[str, str]]
	releaseDate: pendulum.Pendulum
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

	def summary(self, level:int = 0):
		""" prints a summary of the media. 'level' indicates the indentation level to use."""
		indent = '' if level == 0 else '\t' * level
		print(indent, self)
		print(indent, "\timdbId:     ", self.imdbId)
		print(indent, "\tyear(s):    ", self.year)
		print(indent, "\tduration    ", self.duration)
		print(indent, "\timdbRating: ", self.imdbRating)
		print(indent, "\tPlot:       ", self.plot)
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
