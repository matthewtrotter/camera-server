from django.shortcuts import render
from django.utils import timezone

from pics.models import Snapshot

import boto3
from uuid import uuid1

def index(request):
    print(request)
    requested_snapshot = None
    snapshot = None
    if request.method == 'POST':
        requested_snapshot = take_snapshot()

    all_snapshots = Snapshot.objects.order_by('-datetime_taken')[:10]


    context = {
        'requested_snapshot': requested_snapshot,
        'snapshot': snapshot,
        'all_snapshots': all_snapshots
    }
    return render(request, 'pics/index.html', context)

def take_snapshot():
    # Request a new snapshot from the IoT Camera

    # Reserve a picture url
    request_uuid = uuid1()
    url, key = reserve_new_picture(key=str(request_uuid))

    # Request a new snapshot from the IoT Camera
    request_picture(key)
    
    ss = Snapshot(
        picture_url=url,
        request_uuid=request_uuid,
        datetime_taken=timezone.now()
    )
    ss.save()

    return ss

def reserve_new_picture(key: str):
    """Reserve a new picture on AWS S3 and return the url and key
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('remotecamerapics')
    body = open('iot_camera_server/pics/refresh.jpg', 'rb')
    bucket.put_object(
        ACL='public-read',
        Body=body,
        ContentType='jpg',
        Key=key
        )
    url = f'https://remotecamerapics.s3.amazonaws.com/{key}'
    return url, key


def request_picture(key: str):
    """Send a message to the SQS to request the camera upload a new picture to S3

    Parameters
    ----------
    key : str
        AWS S3 key to upload to
    """
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/205509648215/RemoteCameraPictures',
        MessageBody=key
    )