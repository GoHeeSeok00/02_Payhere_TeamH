from django.test import Client, TestCase
from django.urls import resolve

from account_book.models import AccountBook, AccountBookRecord
from account_book.views import AccountBooksAPIView, AccountBooksDetailAPIView, AccountBooksRecordAPIView
from user.models import User


class ViewTestCase(TestCase):
    """
    Assignee : 훈희

    view와 view의 method를 테스트 합니다.
    총 3개의 view와 6개의 method가 있습니다.
    """

    def setUp(self):
        self.client = Client()

        """샘플 User 데이터 생성"""
        self.user_01 = User.objects.create(id=7, email="test1@gmail.com", password="pAssWord")
        self.user_02 = User.objects.create(id=8, email="test2@gmail.com", password="pAssWord")

        """샘플 AccountBook 데이터 생성"""
        self.account_book_01 = AccountBook.objects.create(title="서가앤쿡매탄점", balance=10000, user_id=self.user_01.id)
        self.account_book_02 = AccountBook.objects.create(title="서가앤쿡권선점", balance=30000, user_id=self.user_02.id)

        """샘플 AccountBookRecord 데이터 생성"""
        self.account_book_record_01 = AccountBookRecord.objects.create(
            account_book_id=self.account_book_01.id, amount=-10000, memo="재료비", is_deleted=0
        )
        self.account_book_record_01 = AccountBookRecord.objects.create(
            account_book_id=self.account_book_02.id, amount=-30000, memo="매장 자재구매비", is_deleted=1
        )

    def test_url_resolves_to_account_books_api_view(self):
        """accountbooks url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks/")

        self.assertEqual(found.func.__name__, AccountBooksAPIView.as_view().__name__)

    def test_url_resolves_to_account_books_detail_api_view(self):
        """accountbooks_detail url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks/<obj_id>/")

        self.assertEqual(found.func.__name__, AccountBooksDetailAPIView.as_view().__name__)

    def test_url_resolves_to_account_books_record_api_view(self):
        """accountbooks_record url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks/<obj_id>/records/")

        self.assertEqual(found.func.__name__, AccountBooksRecordAPIView.as_view().__name__)
