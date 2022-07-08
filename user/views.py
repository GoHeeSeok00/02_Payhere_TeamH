from django.contrib.auth import authenticate, get_user_model, login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwner
from user.serializers import MyTokenObtainPairSerializer, SignInSerializer, SignUpSerializer, UserSerializer

User = get_user_model()


class SignUpView(APIView):
    """
    Assignee : 정석

    회원가입
    """

    permission_classes = [AllowAny]
    serializer = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = Response(
                {
                    "message": "회원가입에 성공했습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """
    Assignee : 정석

    로그인

    로그인 성공시 access token과 refresh token 리턴
    """

    permission_classes = [AllowAny]
    serializer = SignInSerializer

    @swagger_auto_schema(request_body=SignInSerializer)
    def post(self, request):
        user = authenticate(
            request,
            email=request.data.get("email"),
            password=request.data.get("password"),
        )
        if not user:
            return Response({"error": "이메일 또는 비밀번호를 잘못 입력했습니다."}, status=status.HTTP_404_NOT_FOUND)
        login(request, user)
        token = MyTokenObtainPairSerializer.get_token(user)
        res = Response(
            {
                "message": f"{user.username}님 반갑습니다!",
                "token": {
                    "access": str(token.access_token),
                    "refresh": str(token),
                },
            },
            status=status.HTTP_200_OK,
        )
        return res


class UserView(APIView):
    """
    Assignee : 정석

    회원정보 수정

    User의 is_active값을 참조해 해당 값 변경시에 soft delete 진행
    """

    permission_classes = [IsOwner]

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        try:
            if request.data["is_active"] == False:
                return Response(
                    {
                        "message": "회원탈퇴가 정상적으로 진행되었습니다.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            elif request.data["is_active"] == True:
                return Response(
                    {
                        "message": "회원정보가 수정되었습니다.",
                    },
                    status=status.HTTP_200_OK,
                )
        except KeyError:
            return Response(
                {
                    "message": "잘못된 입력입니다.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
