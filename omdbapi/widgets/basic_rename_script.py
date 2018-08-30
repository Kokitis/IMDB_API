from pathlib import Path
import re



def rename_folder(folder:Path):
	pattern = "s[\d]+e[\d]+"

	logs = list()
	for source in folder.iterdir():
		match = re.search(pattern, source.name.lower())

		season_number, episode_number = match.group(0)[1:].split('e')
		destination = "1600 Penn S{}E{:>02}{}".format(season_number, episode_number, source.suffix)

		destination = source.with_name(destination)

		print(source, "->", destination)
		source.rename(destination)
		logs.append("{} -> {}".format(source, destination))
	log_file = folder / "rename_log.txt"
	log_file.write_text('\n'.join(logs))

if __name__ == "__main__":
	folder = Path(r"Y:\Video\Series\1600 Penn")
	rename_folder(folder)