from typing import *

import pendulum


class MiniEpisodeResource(TypedDict):
	title: str
	imdbId: str
	imdbRating: float
	releaseDate: pendulum.Date
	episodeId: str
	seasonIndex: int
	indexInSeries: int
	indexInSeason: int


class MediaResource(TypedDict):
	actors: List[str]
	awards: str
	countries: List[str]
	director: str
	runtime: pendulum.Duration
	genres: List[str]
	imdbId: str
	imdbRating: float
	imdbVotes: int
	languages: List[str]
	plot: str
	poster: str
	rated: str
	ratings: List[Dict[str, float]]
	releaseDate: pendulum.Date
	title: str

	type: Literal['series', 'movie']
	writers: List[str]


class SeriesResource(MediaResource):
	totalSeasons: int
	episodes: List[MiniEpisodeResource]


class MovieResource(MediaResource):
	boxOffice: int
	releaseDateDVD: pendulum.Date
	production: str


class EpisodeResource(MediaResource):
	seasonIndex: int
	indexInSeries: int
	seriesId: str
