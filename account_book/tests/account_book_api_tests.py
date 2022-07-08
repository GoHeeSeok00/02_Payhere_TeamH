from rest_framework.test import APIClient, APITestCase

from user.models import User


class AccountBooksAPIViewTestCase(APITestCase):
    """
    Assignee : 훈희

    accountbook api 작동에 대한 테스트를 합니다.

    """

    def setUp(self):
        """로그인한 상태 설정"""
        payload = {
            "email": "tett1234@test.com",
            "password": "password",
        }
        self.user = User.objects.create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_account_books_api_view_get(self):
        """가계부 목록 조회"""
        url_accountbooks = "/api/v1/accountbooks"

        response = self.client.get(url_accountbooks)
        self.assertEqual(response.status_code, 200)

    def test_account_books_api_view_get_permission_check(self):
        """가계부 단건 조회 권한 확인( 권한 없음 )"""
        url_accountbooks_record = "/api/v1/accountbooks/1"

        response = self.client.get(url_accountbooks_record, format="json")
        self.assertEqual(response.status_code, 404)

    def test_account_books_api_view_get_valid_data(self):
        """가계부 단건 조회"""
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbooks_record = f"/api/v1/accountbooks/{account_book_id}"

        response = self.client.get(url_accountbooks_record)
        self.assertEqual(response.status_code, 200)

    def test_account_books_api_view_post(self):
        """가계부 생성"""
        url_accountbooks = "/api/v1/accountbooks"

        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}
        response = self.client.post(url_accountbooks, account_book_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_account_books_api_view_put(self):
        """
        가계부 단건 수정

        삭제는 is_deleted": "True"
        를 사용해서 soft delete 방식으로 삭제하여 한가지 테스트에 표현

        """
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_modify_url = f"/api/v1/accountbooks/{account_book_id}"

        account_book_data = {
            "title": "서가앤쿡 대구점",
            "balance": "1000000",
        }

        response = self.client.put(url_accountbook_modify_url, account_book_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_account_books_api_view_patch(self):
        """
        가계부 단건 삭제/복구

        삭제는 is_deleted": "True"
        를 사용해서 soft delete 방식으로 삭제하여 한가지 테스트에 표현

        """
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_modify_url = f"/api/v1/accountbooks/{account_book_id}/recovery"

        account_book_data = {"is_deleted": False}

        response = self.client.patch(url_accountbook_modify_url, account_book_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_account_books_record_api_view_post(self):
        """가계부 기록 생성"""
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_records = f"/api/v1/accountbooks/{account_book_id}/records"

        account_book_records_data = {"amount": -30000, "memo": "접대비", "date": "2022-07-16"}

        response = self.client.post(url_accountbook_records, account_book_records_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_account_books_record_api_view_get(self):
        """가계부 기록 단건 상세 조회"""
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {"title": "이디야커피 여의도점", "balance": "1000000"}

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_records = f"/api/v1/accountbooks/{account_book_id}/records"

        account_book_records_data = {"amount": -30000, "memo": "접대비", "date": "2022-07-16"}

        self.client.post(url_accountbook_records, account_book_records_data, format="json")
        account_book_record_id = 1

        url_accountbook_records = f"/api/v1/accountbooks/records/{account_book_record_id}"

        response = self.client.get(url_accountbook_records, format="json")
        self.assertEqual(response.status_code, 200)

    def test_account_books_record_api_view_put(self):
        """가계부 기록 수정"""
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {
            "title": "이디야커피 여의도점",
            "balance": "1000000",
        }

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_records = f"/api/v1/accountbooks/{account_book_id}/records"

        account_book_records_data = {"amount": -30000, "memo": "접대비", "date": "2022-07-16"}

        response_create_first = self.client.post(url_accountbook_records, account_book_records_data, format="json")

        self.assertEqual(response_create_first.status_code, 201)
        record_id = 1
        url_accountbook_modify_records = f"/api/v1/accountbooks/records/{record_id}"
        account_book_modify_records_data = {"amount": 10000, "memo": "로또 당첨", "date": "2022-07-16"}

        response_modify_data = self.client.put(
            url_accountbook_modify_records, account_book_modify_records_data, format="json"
        )

        self.assertEqual(response_modify_data.status_code, 404)

    def test_account_books_record_api_view_patch(self):
        """가계부 기록 삭제/복구"""
        url_accountbooks = "/api/v1/accountbooks"
        account_book_data = {
            "title": "이디야커피 여의도점",
            "balance": "1000000",
        }

        response = self.client.post(url_accountbooks, account_book_data, format="json")
        account_book_id = response.data["가계부_고유번호"]

        url_accountbook_records = f"/api/v1/accountbooks/{account_book_id}/records"

        account_book_records_data = {"amount": -30000, "memo": "접대비", "date": "2022-07-16"}

        response_create_first = self.client.post(url_accountbook_records, account_book_records_data, format="json")

        self.assertEqual(response_create_first.status_code, 201)
        record_id = 1
        url_accountbook_modify_records = f"/api/v1/accountbooks/records/{record_id}/recovery"
        account_book_modify_records_data = {"is_deleted": "False"}

        response_modify_data = self.client.patch(
            url_accountbook_modify_records, account_book_modify_records_data, format="json"
        )

        self.assertEqual(response_modify_data.status_code, 404)
