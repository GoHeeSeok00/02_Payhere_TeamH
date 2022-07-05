from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwner

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
        accountbooks = AccountBook.objects.all().filter(user=request.user, is_deleted=False)
        serializer = AccountBooksModelSerializer(accountbooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountBookRecordCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# url : GET, PUT api/v1/accountbooks/<obj_id>/
class AccountBooksDetailAPIView(APIView):
    """
    Assignee : 희석
    Http method = GET, PUT

    permission = 본인만 조회, 수정

    GET : 가계부 단일조회
    PUT : 가계부 수정, 삭제
    """

    permission_classes = [IsOwner]

    def get_object_and_check_permission(self, obj_id):
        """
        Assignee : 희석

        obj_id : int

        input 인자로 단일 오브젝트를 가져오고, 퍼미션 검사를 하는 메서드입니다.
        DoesNotExist 에러 발생 시 None을 리턴합니다.
        """
        try:
            object = AccountBook.objects.get(id=obj_id, is_deleted=False)
        except AccountBook.DoesNotExist:
            return

        self.check_object_permissions(self.request, object)
        return object

    def get(self, request, obj_id):
        """
        Assignee : 희석

        obj_id : int

        가계부 단일 조회를 하기 위한 메서드입니다.
        """
        account_book = self.get_object_and_check_permission(obj_id)
        if not account_book:
            return Response({"error": "가계부가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(AccountBooksModelSerializer(account_book).data, status=status.HTTP_200_OK)
