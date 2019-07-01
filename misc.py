
if __name__ == "__main__":
	print("Running notebook...", flush = True)
	from omdbapi import api, graphics

	key = 'Lucifer'  # Legion
	response = api.find(key)


	print(response.toTable().to_string())
