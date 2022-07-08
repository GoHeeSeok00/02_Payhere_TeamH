from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import AccountBook, AccountBookRecord


class GetDeleteAccountBooksRecordModelSerializer(ModelSerializer):
    """
    Assignee : 희석

    @@@ 가계부 기록이 삭제된 데이터를 보기위한 시리얼라이저입니다. @@@
    """

    class Meta:
        model = AccountBookRecord
        fields = ("date", "amount", "memo", "created_at", "deleted_at", "is_deleted")


class GetDeleteAccountBooksModelSerializer(ModelSerializer):
    """
    Assignee : 희석

    @@@ 해당 가계부의 삭제된 기록만 보여주는 시리얼라이저 입니다. @@@
    """

    accountbook_record = serializers.SerializerMethodField(required=False, read_only=True)

    def get_accountbook_record(self, obj):
        account_book_records = obj.account_book_record.order_by("date", "created_at").filter(is_deleted=True)
        account_book_records_serializer = GetDeleteAccountBooksRecordModelSerializer(account_book_records, many=True)
        return account_book_records_serializer.data

    class Meta:
        model = AccountBook
        fields = ("user", "title", "accountbook_record")


class AccountBooksRecordModelSerializer(ModelSerializer):
    """
    Assignee : 상백
    Refactoring : 희석

    참조 및 역참조를 통해 AccountBookRecord 모델 객체들의 금액을 for문을 이용하여
    AccountBookRecord 모델 데이터가 생성된 시점까지의 잔액을 계산

    내부에 정의된 create 메소드 override로 AccountBookRecord 모델 객체 생성
    """

    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        balance = obj.account_book.balance
        for record in obj.account_book.account_book_record.order_by("date", "created_at").filter(is_deleted=False):
            if obj.date >= record.date:
                balance += record.amount
        return balance

    def create(self, validated_data):
        account_book = self.context["account_book"]
        account_book_record = AccountBookRecord(account_book=account_book, **validated_data)
        account_book_record.save()
        return account_book_record

    class Meta:
        model = AccountBookRecord
        fields = ("date", "amount", "memo", "balance", "created_at", "is_deleted")
        extra_kwargs = {
            "is_deleted": {"write_only": True},
        }


class AccountBooksModelSerializer(ModelSerializer):
    """
    Assignee : 상백
    Refactoring : 희석

    View단에서 AccountBook 모델의 객체가 주어졌을 때,
    역참조를 통해 AccountBookRecord 모델의 쿼리셋을 가져오기

    AccountBookRecord 모델 쿼리셋에서 for문을 이용해
    현재까지의 잔액을 계산하는 로직 구성

    내부에 정의된 create 메소드 override로 로그인된 user로 AccountBook 모델 객체 생성
    """

    가계부_고유번호 = serializers.IntegerField(source="id", required=False, read_only=True)
    total_balance = serializers.SerializerMethodField(required=False, read_only=True)
    accountbook_record = serializers.SerializerMethodField(required=False, read_only=True)

    def get_total_balance(self, obj):
        account_book_records = obj.account_book_record.order_by("created_at").filter(is_deleted=False)
        total_balance = obj.balance
        for record in account_book_records:
            total_balance += record.amount
        return total_balance

    def get_accountbook_record(self, obj):
        account_book_records = obj.account_book_record.order_by("date", "created_at").filter(is_deleted=False)
        account_book_records_serializer = AccountBooksRecordModelSerializer(account_book_records, many=True)
        return account_book_records_serializer.data

    def create(self, validated_data):
        user = self.context["user"]
        account_book = AccountBook(user=user, **validated_data)
        account_book.save()
        return account_book

    class Meta:
        model = AccountBook
        fields = ("user", "title", "balance", "가계부_고유번호", "total_balance", "accountbook_record", "is_deleted")
        extra_kwargs = {
            "is_deleted": {"write_only": True},
        }
        read_only_fields = ["user"]
