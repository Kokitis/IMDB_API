import sys
from pathlib import Path

github_folder = Path.home() / "Documents" / "GitHub"

sys.path.append(str(github_folder))


# noinspection PyUnresolvedReferences
import github_data

omdb_api_key = github_data.omdb_api_key
