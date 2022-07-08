import json

from django.test import Client
from rest_framework.test import APITestCase

from account_book.models import AccountBook, AccountBookRecord
from user.models import User


class AccountBooksAPIViewTestCase(APITestCase):
    url = "/api/v1/accountbooks"
    login_url = "/api/v1/users/signin"

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

        # self.email = "hoonhee@gmail.com"
        # self.password = "you_know_nothing"
        # self.user = User.objects.create_user(self.email, self.password)

    def test_get_access_token(self):
        response = self.client.post(self.login_url, {"email": self.email, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))
        # self.assertTrue("access" in json.loads(response.content))

        access_token = response.json()["token"]["access"]
        return access_token

    def test_account_books_api_view_post(self):
        header = {"HTTP_Authorization": self.test_get_access_token()}
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}
        response = self.client.post(self.url, account_book_data, content_type="application/json", **header)
        self.assertEqual(response.status_code, 201)

    def test_account_books_api_view_get(self):
        header = {"HTTP_Authorization": self.test_get_access_token()}
        response = self.client.get(self.url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
