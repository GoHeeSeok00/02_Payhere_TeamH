from django.db import models

from config.models import BaseTimeStamp as BaseTimeStampModel
from user.models import User as UserModel

"""Create your models here."""


class AccountBook(BaseTimeStampModel):
    """
    Assignee : 희석

    사업장 별 가계부를 만들 수 있는 가계부 모델입니다.
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=UserModel, verbose_name="사용자", on_delete=models.CASCADE, related_name="account_book")
    title = models.CharField("가계부 제목", max_length=20)
    balance = models.IntegerField("가계부 시작 금액", default=0)
    is_deleted = models.BooleanField("삭제 여부", default=False)

    def __str__(self):
        return f"id : {self.id} / {self.title}의 가계부"


class AccountBookRecord(BaseTimeStampModel):
    """
    Assignee : 희석

    가계부별 수입 or 지출 기록을 남길 수 있는 모델입니다.
    수입은 양수 지출을 음수를 받습니다.
    """

    id = models.BigAutoField(primary_key=True)
    account_book = models.ForeignKey(
        to=AccountBook, verbose_name="가계부", on_delete=models.CASCADE, related_name="account_book_record"
    )
    amount = models.IntegerField("금액")
    memo = models.CharField("메모", max_length=100)
    is_deleted = models.BooleanField("삭제 여부", default=False)

    def __str__(self):
        return f"id : {self.id} / {self.amount} : {self.memo}"
