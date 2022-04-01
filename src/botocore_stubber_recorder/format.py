import os
import sys
import logging
import subprocess
import shutil
from typing import Optional


def is_black_on_path() -> Optional[str]:
    return shutil.which("black")


def format_source_code(directory: str):
    black = is_black_on_path()
    if black:
        process = subprocess.Popen(
            [
                black,
                "--quiet",
                os.path.abspath(directory),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        out, err = process.communicate()
        if process.returncode != 0:
            logging.error("failed to format code in %s", directory)
            logging.error("%s", out)
            logging.error("%s", err)
    else:
        logging.debug("black not found on path, not formatting")
