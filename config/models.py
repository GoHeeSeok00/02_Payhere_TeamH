from django.db import models


class BaseTimeStamp(models.Model):
    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    class Meta:
        abstract = True
