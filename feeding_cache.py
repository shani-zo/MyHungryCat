import logging
import os

logger = logging.getLogger(__name__)

FEEDING_CACHE_FILE_PATH = 'feeding.cache'


def get_feeding_data() -> str:
    """Gets the data saved in the cache file."""
    try:
        with open(FEEDING_CACHE_FILE_PATH) as feeding_cache:
            return feeding_cache.read()
    except (IOError, OSError) as e:
        logger.error("Error reading from cache file")
        raise e


def update_feeding_data(data: str):
    """Update the cache with the data provided. Old data will be deleted."""
    try:
        with open(FEEDING_CACHE_FILE_PATH, 'w+') as feeding_cache:
            return feeding_cache.write(data)
    except (IOError, OSError) as e:
        logger.error("Error reading from cache file")
        raise e
