
try:
	from . import omdb_api
	from .resources import EpisodeResource, SeasonResource, MediaResource, table_columns
except ModuleNotFoundError:
	import omdb_api
	from resources import EpisodeResource, SeasonResource, MediaResource, table_columns