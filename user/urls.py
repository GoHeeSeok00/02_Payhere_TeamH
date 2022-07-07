from django.urls import path

from user.views import SignInView, SignUpView

urlpatterns = [
    path("v1/users/signup", SignUpView.as_view()),
    path("v1/users/signin", SignInView.as_view()),
]
