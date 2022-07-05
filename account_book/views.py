from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccountBook
from .serializers import AccountBookRecordCreateSerializer, AccountBooksModelSerializer


# url : GET api/v1/accountbooks/, POST api/v1/accountbooks/
class AccountBooksAPIView(APIView):
    """
    Assignee : 상백
    Http method = GET, POST

    클라이언트의 요청으로 이제까지 기록한 가계부 리스트 정보를
    response 하는 API

    POST 요청 시, 가계부 데이터를 생성
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 쿼리 파라미터가 들어왔을 때, 삭제된 내역만 볼 수 있게끔 구현해야 함
        accountbooks = AccountBook.objects.all().filter(user=request.user, is_delete=False)
        serializer = AccountBooksModelSerializer(accountbooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountBookRecordCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBooksDetailAPIView(APIView):
    """
    Assignee : 희석
    Http method = GET, PUT

    permission = 본인만 조회, 수정

    GET : 가계부 단일조회
    PUT : 가계부 수정, 삭제
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, obj_id):
        return
