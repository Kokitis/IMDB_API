
try:
	from ._base_api import OmdbApi, EpisodeResource, SeasonResource, MediaResource
except ModuleNotFoundError:
	from _base_api import OmdbApi, EpisodeResource, SeasonResource, MediaResource