from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import SignupView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
