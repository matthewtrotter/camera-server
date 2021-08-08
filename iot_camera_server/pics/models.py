from django.db import models


class Snapshot(models.Model):
    picture_url = models.URLField()
    request_uuid = models.UUIDField()
    datetime_taken = models.DateTimeField()
