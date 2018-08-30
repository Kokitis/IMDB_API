from pathlib import Path
from dataclasses import asdict
from pprint import pprint
import re
from package.api import OmdbApi

api = OmdbApi()


class Rename:
	def __init__(self, folder: Path, series_name: str, confirm = False, files = None, pattern: str = None):
		rename_files = confirm

		if pattern is None:
			pattern = 's(?P<season>[0-9]+)e(?P<episode>[0-9]+)'
		if series_name is None:
			series_name = folder.name
		if files is None:
			files = list(folder.iterdir())

		self.series_info = api.get(series_name)
		#self.series_info.summary()

		if rename_files:
			self.series_info.save(folder / "series_info.yaml")

		self.log = list()
		for source in files:
			match = re.search(pattern, source.name.lower())
			if match is None:
				print("Cannot find the episode index for ", source)
				continue
			else:
				match = match.groupdict()
			season_index = match['season']
			episode_index = match['episode']

			try:
				newname = self.format_name(season_index, episode_index)
			except TypeError:
				continue
			destination = source.with_name(newname + source.suffix)

			if source.name == destination.name:
				continue
			self.log.append((source, destination))
			if rename_files:
				if not destination.exists():
					source.rename(destination)
				else:
					print("Already exists: ", destination)
			print(f"{source.name} -> {destination.name}")
		if rename_files:
			self.save_log(folder)

	def format_name(self, season_index, episode_index) -> str:
		episode_key = "S{:>02}E{:>02}".format(int(season_index), int(episode_index))
		series_name = self.series_info.title

		episode = self.series_info.get_episode(episode_key)

		string = "{} {}".format(series_name, episode_key)
		if episode:
			string += " - " + episode.title
		else:
			print("Unable to find the episode for ", episode_key)
		# remove illegal characters

		string = re.sub('[<>:"/|?*]', "", string)
		# print(season_index, episode_index, episode)

		return string

	def save_log(self, folder: Path):
		log_file = folder / "rename_log.txt"
		self.log = [' -> '.join(map(str, i)) for i in self.log]
		log_file.write_text('\n'.join(self.log))


def unpack(folder: Path):
	for f in folder.glob("**/*"):
		destination = folder / f.name
		#print(destination)
		if not destination.exists():
			f.rename(destination)


if __name__ == "__main__":
	debug = False
	folder = Path(r"Z:\Video\TV Shows\Mr. Robot")
	if debug:
		unpack(folder)
	else:
		folder = Path(r"Z:\Video\TV Shows\Veronica Mars\Veronica Mars Season 1")
		fn = Path(folder)

		series_name = "Veronica Mars" #folder.name
		pattern = "s?(?P<season>[\d])[xe](?P<episode>[\d]+)"
		#pattern = None
		unpack(folder)
		files = list(fn.glob("**/*"))
		Rename(folder, series_name, False, files, pattern)
