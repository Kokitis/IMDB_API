import sys
from pathlib import Path

github_folder = Path.home() / "Documents" / "GitHub"
print(github_folder.exists(), github_folder)
sys.path.append(str(github_folder))
sys.path.append(str(github_folder / "pytools"))

# noinspection PyUnresolvedReferences
import github_data

omdb_api_key = github_data.omdb_api_key

# noinspection PyUnresolvedReferences
try:
	from pytools import timetools, tabletools, numbertools, datatools
except:
	import pytools

	timetools = pytools.timetools
	tabletools = pytools.tabletools
	numbertools = pytools.numbertools
	datatools = pytools.datatools
