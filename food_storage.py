import datetime
import logging
import uuid
import os
from typing import Tuple

import boto3
from botocore.exceptions import ClientError

from exceptions import ServiceProviderException

logger = logging.getLogger(__name__)


BUCKET_NAME = 'cat-food-bucket'
DOWNLOAD_FOLDER = 'temp_image_cache'


if not os.path.exists(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)


s3 = None
try:
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = s3.Bucket(BUCKET_NAME)
except ClientError as e:
    logger.error(str(e))
    raise ServiceProviderException(str(e))


def upload(img_path):
    """Upload potential food to food bucket
    Raises
        ServiceProviderException for any error"""
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


def get_last_added_food() -> Tuple[str, datetime.datetime]:
    """Get the last object that was added to the bucket. Will require going over all the objects
    Raises
        ServiceProviderException for any error"""
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%Y-%m-%d-%H-%M-%S'))
    try:
        objs = s3_client.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
    except ClientError as e:
        logger.error(str(e))
        raise ServiceProviderException(str(e))
    last_added = [obj for obj in sorted(objs, key=get_last_modified)][0]
    return last_added['Key'], last_added['LastModified']


def download(key) -> str:
    """
    Download an object by it's key

    Args:
        key: The key of the object to download

    Returns:
        The path the file was downloaded to.

    Raises
        ServiceProviderException for any error with the download or saving process
    """
    save_path = os.path.join(DOWNLOAD_FOLDER, key)
    try:
        s3.download_file(BUCKET_NAME, key, save_path)
    except ClientError as e:
        logger.error(str(e))
        raise ServiceProviderException(str(e))
    return save_path
