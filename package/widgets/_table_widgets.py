from ..github import tabletools


def parseTable(api, filename, **kwargs):
	"""
		Attempts to lookup imformation from the api using information saved in a table.
		Keyword Arguments
		-----------------

	"""

	table = tabletools.Table(filename)
	# title, status, totalSeasons, totalEpisodes, imdbRating, myRating, synopsis, haveWatched, imdbId, yearAired
	new_table = list()
	for row in table:
		media_title = ""
		media_id = ""

		if media_id:
			response = api.get(media_id, True)
		else:
			response = api.find(media_title)

		total_episodes = 0
		for i in response['seasons']:
			total_episodes += i['length']

		new_row = {
			'title':         response['title'],
			'status':        row['status'],
			'totalSeasons':  response['totalSeasons'],
			'totalEpisodes': total_episodes,
			'imdbRating':    response['imdbRating'],
			'myRating':      row['myRating'],
			'haveWatched':   row['haveWatched'],
			'synopsis':      response['plot'],
			'imdbId':        response['imdbId'],
			'yearAired':     response['year']
		}
		new_table.append(new_row)

	new_table = tabletools.Table(new_table)

	return new_table
