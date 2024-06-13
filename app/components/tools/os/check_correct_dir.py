# python lib
import os

# my lib
from app.components.config import (
    API_STATIC_FILES_DIRS,
)


def check_exists_dirs() -> None:  # function to check the existence of directories
    # check exists dirs from 'API_STATIC_FILES_DIRS'
    for path in API_STATIC_FILES_DIRS.values():
        if not os.path.exists(path):
            os.mkdir(path)
