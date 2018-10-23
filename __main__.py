from omdbapi.api import OmdbApi
import argparse
from pprint import pprint
def _generate_parser():


	parser = argparse.ArgumentParser()

	parser.add_argument(
		"-i", "--id",
		help = "The imdb id of a show or tv show.",
		action = 'store',
		dest = 'id'
	)

	parser.add_argument(
		"-s", "--search",
		help = "Searches for a show or movie matching the requested term.",
		action = 'store',
		dest = 'term'
	)

	parser.add_argument(
		"-o", "--output",
		help = "Filename of the output graph."
	)

	return parser.parse_args()



if __name__ == "__main__":
	cmd = _generate_parser()

	omdb_api = OmdbApi()

	if cmd.id:
		response = omdb_api.get(cmd.id)
		print(response.summary())
	elif cmd.term:
		response = omdb_api.find(cmd.term)