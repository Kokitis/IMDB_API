import pytest
from omdbapi.api import resources
import pendulum

@pytest.fixture
def episode()->resources.MiniEpisodeResource:
	data = resources.MiniEpisodeResource(
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

def test_episode_rating(episode):
	assert episode['imdbRating'] == 9.0

def test_series_to_table():
	pass