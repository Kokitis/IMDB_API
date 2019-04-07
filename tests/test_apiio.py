
from omdbapi.api import apiio
def test_get_search_parameters():


	result = apiio._get_search_parameters('teststring', 'series')

	expected = {
		's': 'teststring',
		'Type': 'series'
	}

	assert result == expected

def test_get_season_parameters():
	result = apiio._get_season_parameters('seriesABC', 12)

	expected = {
		'i': 'seriesABC',
		'Season': 12
	}

	assert result == expected

def test_get_request_parameters():

	expected = {
		't': 'string'
	}
	assert apiio._get_request_parameters('string') == expected

	expected = {
		'i': 'tt1234567'
	}
	assert apiio._get_request_parameters('tt1234567') == expected