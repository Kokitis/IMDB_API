from ._base_api import OmdbApi, Season
from .graphics import GraphTv

if __name__ == "__main__":
	API = OmdbApi()
	test_show = "tt1898069" # American Gods
	test_movie= "tt0848228" # The Avengers
	vd = "tt1405406" # The Vampire Diaries

	result = API.request(vd, True)
	pprint(result)
	graph = GraphTv(result)
	plt.show()