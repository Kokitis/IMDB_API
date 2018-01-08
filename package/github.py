import sys
import os

github_folder = os.path.join(os.getenv('USERPROFILE'), 'Documents', 'Github')

sys.path.append(github_folder)

# noinspection PyUnresolvedReferences
from github_data import omdb_api_key

# noinspection PyUnresolvedReferences
from pytools import timetools