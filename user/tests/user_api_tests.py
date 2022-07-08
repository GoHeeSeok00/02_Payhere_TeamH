import json

from rest_framework.test import APITestCase

from user.models import User


class SignUpViewTestCase(APITestCase):
    """
    Assignee : 훈희

    회원가입 테스트
    """

    url = "/api/v1/users/signup"

    def test_user_registration(self):
        """유저 등록 테스트"""
        user_data = {
            "email": "test1@testuser.com",
            "username": "testuser1",
            "mobile": "12341111",
            "password": "12312311",
        }
        response = self.client.post(self.url, user_data, format="json")
        print(response)
        self.assertEqual(201, response.status_code)

    def test_unique_email_validation(self):
        """이메일이 한개만 있는지 테스트"""
        user_data_1 = {
            "username": "testuser1",
            "email": "test@testuser.com",
            "password": "123123",
            "mobile": "12341111",
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser2",
            "email": "test@testuser.com",
            "password": "123123",
            "mobile": "12341111",
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class SignInViewTestCase(APITestCase):
    """
    Assignee : 훈희

    회원 로그인 테스트
    """

    url = "/api/v1/users/signin"

    def setUp(self):
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.email, self.password)

    def test_authentication_without_password(self):
        """패스워드 없을 때 에러 확인"""
        response = self.client.post(self.url, {"email": "john@snow.com"})
        self.assertEqual(404, response.status_code)

    def test_authentication_with_wrong_password(self):
        """패스워드가 잘못 들어왔을 때 에러 확인"""
        response = self.client.post(self.url, {"email": self.email, "password": "I_know"})
        self.assertEqual(404, response.status_code)

    def test_authentication_with_valid_data(self):
        """유효한 데이터가 들어왔을 때 동작 확인"""
        response = self.client.post(self.url, {"email": self.email, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))
        self.assertTrue("message" in json.loads(response.content))
