import os
from progressbar import ProgressBar
from ..github import tabletools
filename = os.path.join(os.getenv('USERPROFILE'), 'Google Drive', "Media List.xlsx")


def parseTable(api, filename, **kwargs):
	"""
		Attempts to lookup imformation from the api using information saved in a table.
		Keyword Arguments
		-----------------

	"""

	table = tabletools.Table(filename, sheetname = "TV Shows")

	# title, status, totalSeasons, totalEpisodes, imdbRating, myRating, synopsis, haveWatched, imdbId, yearAired
	new_table = list()
	pbar = ProgressBar(max_value = len(table))
	for index, row in table.iterrows():
		pbar.update(index)
		media_title = row.get('title')
		media_id = row.get('imdbId')
		media_title = str(media_title)

		if media_title == 'nan': media_title = None
		if not isinstance(media_id, str): media_id = None

		try:
			if media_id:
				response = api.get(media_id, True)
			else:
				response = api.find(media_title)
			error = False
			message = ""
		except Exception as exception:
			error = True
			message = "Could not retrieve data for '{}' ('{}')".format(media_title, str(exception))

		if response is None:
			error = True
			message = "Could not retrieve the seasons for '{}'".format(media_title)

		if error:
			print()
			print(message)
			continue
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