import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
	"input",
	help = "The name or id of the tv series to look up.",
	action = "store"
)
if __name__ == "__main__":
	from omdbapi.api import omdb_api

	args = parser.parse_args(['tt7569592'])
	print("Input: ", args.input)
	result = omdb_api.find(args.input)
	from pprint import pprint
	pprint(result)
