"""
This module provides configuration variables for the git API and other utility functions,
for the time being they are not environment specific but can be further extended if needbe
"""

import os

GH_URL = "https://github.com"
GH_API_URL = "https://api.github.com"
DEFAULT_BRANCH = "main"
TEST_FILE_NAME = "README.md"
GH_USERNAME = os.getenv("GH_USERNAME")
GH_TOKEN = os.getenv("GH_TOKEN")