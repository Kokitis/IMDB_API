import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
	"input",
	help = "The name or id of the tv series to look up.",
	action = "store"
)
if __name__ == "__main__":
	import omdbapi
	import matplotlib.pyplot as plt

	args = parser.parse_args(['tt7569592'])
	print("Input: ", args.input)
	result = omdbapi.api.find(args.input)
	omdbapi.plot_series(result.toTable())
	plt.show()


