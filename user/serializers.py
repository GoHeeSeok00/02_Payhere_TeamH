from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Assignee : 정석

    TOKEN 시리얼라이저
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Assignee : 정석

    회원가입 시리얼라이저
    """

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        username = validated_data.get("username")
        mobile = validated_data.get("mobile")
        user = User(email=email, password=password, username=username, mobile=mobile)
        user.set_password(password)
        user.save()
        return user
