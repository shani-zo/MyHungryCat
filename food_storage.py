import datetime
import logging
import uuid
import os

import boto3
from botocore.exceptions import ClientError

from exceptions import InvalidFood, ServiceProviderException
from tools import is_image_file
import imageClassification

logger = logging.getLogger(__name__)


BUCKET_NAME = 'cat-food-bucket'
DOWNLOAD_FOLDER = 'temp_image_cache'


if not os.path.exists(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)


class Food:
    def __init__(self, food, timestamp):
        if not is_image_file(food):
            raise InvalidFood("Food must be image file")
        self.image = food
        self.timestamp = timestamp


class CatFood(Food):
    ALLOWED_FOOD_TYPES = ['fish']

    def __init__(self, food, timestamp):
        labels = imageClassification.classify_image(self.image)
        if not set(labels).issubset(self.ALLOWED_FOOD_TYPES):
            raise InvalidFood("This food is not good for cats!")
        super(CatFood, self).__init__(food, timestamp)

    @staticmethod
    def get_last_added_cat_food():
        last_added_food_key, last_added_food_modified_date = get_last_added_food()
        s3.download_file(BUCKET_NAME, last_added_food_key, os.path.join(DOWNLOAD_FOLDER, last_added_food_key))
        return CatFood(last_added_food_key, last_added_food_modified_date)


s3 = None
try:
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = s3.Bucket(BUCKET_NAME)
except ClientError as e:
    logger.error(str(e))
    raise ServiceProviderException(str(e))


def feed(img_path):
    """Upload potential food to food bucket"""
    # Create a format name to upload the new file with
    now = datetime.datetime.now()
    uid_for_upload = '{}-{}-{} {}:{}:{} {}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second,
                                                   uuid.uuid4())

    # Upload the file
    try:
        s3_client.upload_file(img_path, BUCKET_NAME, uid_for_upload)
    except ClientError as e:
        logger.error(str(e))
        raise ServiceProviderException(str(e))


def get_last_added_food():
    """Get the last object that was added to the bucket. Will require going over all the objects"""
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%Y-%m-%d-%H-%M-%S'))
    try:
        objs = s3_client.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
    except ClientError as e:
        logger.error(str(e))
        raise ServiceProviderException(str(e))
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][0]
    return last_added['Key'], last_added['LastModified']


def get_food_by_datetime(date: datetime.datetime, search_by_hour: bool = True):
    """
    Gets the objects uploaded in the date given by the user.

    Args:
        date: The date to search by
        search_by_hour: if True then the results will include only food images from the hour specified

    Returns:
        list of all the files that matched the input upload date.
    """
    # Create a name pattern for searching in the bucket
    search_object_name = '{}-{}-{} '.format(date.year, date.month, date.day) + str(date.hour) if search_by_hour else ''
    try:
        input_date_results = bucket.objects.filter(search_object_name)
    except ClientError as e:
        logger.error(str(e))
        raise ServiceProviderException(str(e))
    files = [obj.key for obj in sorted(input_date_results, key=lambda x: x.last_modified)]
    return files


