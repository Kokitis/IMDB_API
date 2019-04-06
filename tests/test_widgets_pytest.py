import pytest

from omdbapi.api import widgets


@pytest.mark.parametrize("string,expected_result", [
	('Legion', False),
	("tt2488496", True),
	("tt234jfas", False)
])
def test_is_imdb_id(string, expected_result):
	test_result = widgets._is_imdb_id(string)

	assert test_result == expected_result
