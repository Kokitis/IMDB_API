from typing import *

class SearchItem(TypedDict):
	Poster: str
	Title: str
	Type: Literal['series', 'movie']
	Year: str
	imdbID: str

class SearchResponse(TypedDict):
	Response: Literal['True', 'False']
	Search: List[SearchItem]
	totalResults: str


class SeasonItem(TypedDict):
	"""
	   example = {
            "Episode": "2",
            "Released": "2012-05-17",
            "Title": "Welcome to Me",
            "imdbID": "tt2761482",
            "imdbRating": "8.1"
        }
	"""
	Episode: str
	Released: str
	Title: str
	imdbID: str
	imdbRating: str

class SeasonResponse(TypedDict):
	"""
	example = {
    "Episodes": [
        {
            "Episode": "2",
            "Released": "2012-05-17",
            "Title": "Welcome to Me",
            "imdbID": "tt2761482",
            "imdbRating": "8.1"
        }
    ],
    "Response": "True",
    "Season": "1",
    "Title": "Video Game High School",
    "totalSeasons": "3"
}
	"""
	Response: Literal['True', 'False']
	Season: str
	Title: str
	totalSeasons: str
	Episodes: List[SeasonItem]

class MediaResponse(TypedDict):
	Actors: str
	Awards: str
	Country: str
	Director: str
	Genre: str
	Language: str
	Metascore: str
	Plot: str
	Poster: str
	Rated: str
	Ratings: List[Dict[str,str]]
	Released: str
	Response: Literal['True', 'False']
	Runtime: str
	Title: str
	Type: Literal['series', 'movie']
	Writer: str
	Year: str
	imdbID: str
	imdbRating: str
	imdbVotes: str
	totalSeasons: str