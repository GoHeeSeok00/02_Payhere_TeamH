from django.db import models


class BaseTimeStamp(models.Model):
    """
    Assignee : 희석

    created_at, updated_at(DateTimeField) 필드를
    사용하는 모델을 위한 기본 모델입니다.
    abstract = True 설정을 해서 물리적 테이블이 생성되지 않습니다.
    """

    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    class Meta:
        abstract = True
