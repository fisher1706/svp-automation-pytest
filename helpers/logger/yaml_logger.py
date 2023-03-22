import logging.config
import os
from pathlib import Path

import yaml

__CONFIG_PATH = Path(__file__).parent.joinpath('logging.yaml')


def setup_logging(default_path=__CONFIG_PATH, default_level=logging.INFO):
    """
    Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt', encoding="utf-8") as file:
            config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    return logging
