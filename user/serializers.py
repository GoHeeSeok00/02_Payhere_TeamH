from rest_framework import serializers

from user.models import User


class UserSignupSerializer(serializers.ModelSerializer):
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
