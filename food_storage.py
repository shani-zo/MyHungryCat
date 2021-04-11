import datetime
import logging
import uuid

import boto3
from botocore.exceptions import ClientError

import exceptions

logger = logging.getLogger(__name__)

BUCKET_NAME = 'cat-food-bucket'

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)


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


def get_last_added_food():
    """Get the last object that was added to the bucket. Will require going over all the objects"""
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    try:
        objs = s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
    except ClientError as e:
        logger.error(str(e))
    else:
        last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][0]
        return last_added


def get_food_by_datetime(date: datetime.datetime, search_by_hour: bool):
    """

    Args:
        date: The date to search by

    Returns:

    """
    search_object_name = '{}-{}-{} '.format(date.year, date.month, date.day) + str(date.hour) if search_by_hour else ''
    input_date_results = bucket.objects.filter(search_object_name)
    files = [obj.key for obj in sorted(input_date_results, key=lambda x: x.last_modified)]
    return files


