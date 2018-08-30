import package
from pprint import pprint
import dataclasses
if __name__ == "__main__":
	test_id = ""
	test_title = "teen wolf"


	api = package.OmdbApi()

	result = api.get(test_title, include_seasons = True)

	print(result)