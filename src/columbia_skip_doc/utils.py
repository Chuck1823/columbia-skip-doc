import logging
import sys

from pathlib import Path


_logger = logging.getLogger(__name__)


def setup_logging(loglevel, class_name):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages

    Returns:
        str: Logger object with desired loglevel and class_name 
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger(class_name)

    return logger


def get_project_root_str(path_obj=False):
    """Gets root of repo

    Args:
        path_obj (bool, optional): bool indicating if we want to return a Path object or a string. Defaults to False.

    Returns:
        str: string 
    """
    if path_obj:
        return Path(__file__).parent.parent.parent
    else:
        return str(Path(__file__).parent.parent.parent)


def show_df_describe_and_head(df):
    """Prints out the describe and head of a DataFrame

    Args:
        df (DataFrame): DataFrame to describe and head
    """
    _logger.info(f"df.describe():\n {df.describe()}")
    _logger.info(f"df.head():\n {df.head()}")
