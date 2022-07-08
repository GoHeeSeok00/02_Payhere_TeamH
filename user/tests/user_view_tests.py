from django.test import TestCase
from django.urls import resolve

from user.views import SignInView, SignUpView


class UserViewTestCase(TestCase):
    """
    Assignee : 훈희

    user view와 url 연결에 대한 테스트를 합니다.

    """

    def test_url_resolves_to_sign_up_view(self):
        """sign_up url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/users/signup")

        self.assertEqual(found.func.__name__, SignUpView.as_view().__name__)

    def test_url_resolves_to_sign_in_view(self):
        """sign_in url과 view가 잘 매치되었는지 Test"""

        found = resolve("/api/v1/users/signin")

        self.assertEqual(found.func.__name__, SignInView.as_view().__name__)
