# Sample Command-Line Usage
```
python omdbapi --id tt0491738
```

# Sample API Usage
```
from omdbapi import OmdbApi, graphics
api = OmdbApi(omdb_api_key)
show_id = 'tt4254242'
response = api.find(test_string)
response.summary()
```

# Available Objects


##### MediaResource:
- `actors`: str
- `awards`: str
- `country`: str
- `director`: str
- `duration`: timetools.Duration
- `genre`: str
- `imdbId`: str
- `imdbRating`: float
- `imdbVotes`: int
- `language`: str
- `metascore`: float
- `plot`: str
- `rating`: str
- `ratings`: List[Dict[str, str]]
- `releaseDate`: timetools.Timestamp
- `responseStatus`: bool
- `title`: str
- `type`: str
- `writer`: str
- `year`: str
