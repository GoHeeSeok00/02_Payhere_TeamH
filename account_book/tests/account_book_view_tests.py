from django.test import TestCase
from django.urls import resolve

from account_book.views import AccountBooksAPIView, AccountBooksDetailAPIView, AccountBooksRecordAPIView


class AccountBookViewTestCase(TestCase):
    """
    Assignee : 훈희

    accountbook view와 url 연결에 대한 테스트를 합니다.

    """

    def test_url_resolves_to_account_books_api_view(self):
        """accountbooks url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks")

        self.assertEqual(found.func.__name__, AccountBooksAPIView.as_view().__name__)

    def test_url_resolves_to_account_books_api_view_get_method(self):
        """AccountBooksAPIViewdml get method Test - WIP"""

        found = resolve("/api/v1/accountbooks")

        self.assertEqual(found.func.__name__, AccountBooksAPIView.as_view().__name__)

    def test_url_resolves_to_account_books_detail_api_view(self):
        """accountbooks_detail url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks/<obj_id>")

        self.assertEqual(found.func.__name__, AccountBooksDetailAPIView.as_view().__name__)

    def test_url_resolves_to_account_books_record_api_view(self):
        """accountbooks_record url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/accountbooks/<obj_id>/records")

        self.assertEqual(found.func.__name__, AccountBooksRecordAPIView.as_view().__name__)
