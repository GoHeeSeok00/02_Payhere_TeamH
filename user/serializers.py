from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Assignee : 정석

    TOKEN 시리얼라이저
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class SignUpSerializer(serializers.ModelSerializer):
    """
    Assignee : 정석

    회원가입 시리얼라이저
    """

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "mobile",
        )

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        username = validated_data.get("username")
        mobile = validated_data.get("mobile")
        user = User(email=email, password=password, username=username, mobile=mobile)
        user.set_password(password)
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    """
    Assignee : 정석

    회원정보수정 시리얼라이저
    """

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = User
        fields = ("email", "password", "mobile", "is_active")
        extra_kwargs = {"password": {"write_only": True}}
