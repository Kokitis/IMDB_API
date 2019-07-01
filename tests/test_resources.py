import pytest
from omdbapi.api import MiniEpisodeResource, SeriesResource, FilmResource
import pendulum

@pytest.fixture
def episode()->MiniEpisodeResource:
	data = MiniEpisodeResource(
		title = 'Chapter 1',
		imdbId = 'tt6143054',
		imdbRating = 9.0,
		releaseDate = pendulum.DateTime(2017, 2, 8, 0, 0, 0),
		episodeId = 'S01E01',
		seasonIndex = 1,
		indexInSeries = 1,
		indexInSeason = 1
	)
	return data

def test_episode_string(episode):
	assert str(episode) == 'EpisodeResource(S01E01 - Chapter 1)'

def test_episode_rating(episode):
	assert episode.imdb_rating == 9.0

def test_series_to_table():
	pass