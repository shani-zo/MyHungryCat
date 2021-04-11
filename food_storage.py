import datetime
import logging
import uuid

import boto3
from botocore.exceptions import ClientError

import exceptions

logger = logging.getLogger(__name__)


BUCKET_NAME = 'cat-food-bucket'

s3 = None
try:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
except ClientError as e:
    logger.error(str(e))
    raise exceptions.ServiceProviderException(str(e))


def feed(img_path):
    """Upload potential food to food bucket"""
    # Create a format name to upload the new file with
    now = datetime.datetime.now()
    uid_for_upload = '{}-{}-{} {}:{}:{} {}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second,
                                                   uuid.uuid4())

    # Upload the file
    try:
        s3.upload_file(img_path, BUCKET_NAME, uid_for_upload)
    except ClientError as e:
        logger.error(str(e))
        raise exceptions.ServiceProviderException(str(e))


def get_last_added_food():
    """Get the last object that was added to the bucket. Will require going over all the objects"""
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    try:
        objs = s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
    except ClientError as e:
        logger.error(str(e))
        raise exceptions.ServiceProviderException(str(e))
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][0]
    return last_added


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
        raise exceptions.ServiceProviderException(str(e))
    files = [obj.key for obj in sorted(input_date_results, key=lambda x: x.last_modified)]
    return files


