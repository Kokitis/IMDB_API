import unittest

from omdbapi.api.widgets import _is_imdb_id


class TestWidgets(unittest.TestCase):
	def test_is_imdb_id(self):
		self.assertTrue(_is_imdb_id('tt1234567'))
		self.assertFalse(_is_imdb_id('tt12345'))
		self.assertFalse(_is_imdb_id('tt123456g'))

		self.assertFalse(_is_imdb_id('Legion'))
		self.assertFalse(_is_imdb_id('asdwevwfejnew'))
