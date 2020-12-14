from typing import *
import datetime
ContentRatingMovie = Literal['G', 'PG', 'PG-13', 'R', 'NC-17']
ContentRatingSeries = Literal['TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-PG', 'TV-14', 'TV-MA']

class IMDBItem(TypedDict):
	type: Literal['Person', 'Organization', 'CreativeWork']
	url: str  # "/name/nm0000434/", "/company/co0071326/"


class IMDBEntity(IMDBItem):
	name: str


class IMDBRating(TypedDict):
	bestRating: str
	ratingValue: str
	type: Literal['AggregateRating']
	worstRating: str


class IMDBRatingAggregate(IMDBRating):
	ratingCount: int


class IMDBReview(TypedDict):
	author: IMDBEntity
	dateCreated: str  # "2005-12-25"
	inLanguage: Literal['English']
	itemReviewed: IMDBItem
	name: str
	reviewBody: str
	reviewRating: IMDBRating
	type: Literal['Review']


class IMDBThumbnail(TypedDict):
	contentUrl: str  # "https://m.media-amazon.com/images/M/MV5BMTUzNDY0NjY4Nl5BMl5BanBnXkFtZTgwNjY4MTQ0NzE@._V1_.jpg"
	type: Literal['ImageObject']


class IMDBTrailer(TypedDict):
	description: str
	embedUrl: str  # "/video/imdb/vi1317709849"
	name: str
	thumbnail: IMDBThumbnail
	thumbnailUrl: str
	type: Literal['VideoObject']
	uploadDate: str  # "2013-10-13T13:57:04Z"


class IMDBRawResponseBase(TypedDict):
	actor: List[IMDBEntity]
	aggregateRating: IMDBRatingAggregate
	context: Literal["http://schema.org"]
	creator: List[IMDBEntity]
	datePublished: str  # "1977-05-25"
	description: str
	genre: List[Literal['Action', 'Adventure', 'Animation', 'Family', 'Fantasy', 'Mystery', 'Sci-Fi']]
	image: str  # "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg"
	keywords: str  # "rebellion,galactic war,space opera,princess,droid"
	name: str
	review: IMDBReview
	type: Literal['Movie']
	url: str  # "/title/tt0076759/"


class IMDBRawResponseSeries(IMDBRawResponseBase):
	contentRating: ContentRatingSeries
	trailer: IMDBTrailer


class IMDBRawResponseMovie(IMDBRawResponseBase):
	contentRating: ContentRatingMovie
	director: IMDBEntity
	duration: str  # "PT2H1M", "PT2H42M"
	trailer: IMDBTrailer


class IMDBRawResponseEpisode(IMDBRawResponseBase):
	contentRating: ContentRatingSeries
	director: IMDBEntity
	timeRequired:str # "PT1H32M"


IMDBResponse = Union[IMDBRawResponseSeries, IMDBRawResponseEpisode, IMDBRawResponseMovie]


class MediaResource(TypedDict):
	actors: List[str]
	awards: str
	countries: List[str]
	director: str
	runtime: datetime.timedelta
	genres: List[str]
	imdbId: str
	imdbRating: float
	imdbVotes: int
	languages: List[str]
	plot: str
	poster: Optional[str]
	rated: str
	ratings: List[Dict[str, float]]
	releaseDate: datetime.datetime
	tags: List[str]
	title: str

	type: Literal['series', 'movie']
	writers: List[str]

class EpisodeResource(MediaResource):
	seasonIndex: int
	indexInSeries: int
	seriesId: str
	parentID: str # IMDB ID of the parent series
	parentTitle: str # Name of the parent series.
