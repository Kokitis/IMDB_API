import sys
from pathlib import Path

github_folder = Path.home() / "Documents" / "GitHub"
print(github_folder.exists(), github_folder)
sys.path.append(str(github_folder))
sys.path.append(str(github_folder / "pytools"))

# noinspection PyUnresolvedReferences
import github_data

omdb_api_key = github_data.omdb_api_key
