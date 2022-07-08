from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwner

from .models import AccountBook, AccountBookRecord
from .serializers import AccountBooksModelSerializer, AccountBooksRecordModelSerializer


# url : GET, POST api/v1/accountbooks
class AccountBooksAPIView(APIView):
    """
    Assignee : 상백
    Http method = GET, POST

    permission = 본인만 조회, 수정

    GET : 가계부 목록 조회
    POST : 가계부 생성
    """

    permission_classes = [IsOwner]

    status = openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        description="delete를 입력하면 삭제된 가계부를 보여줍니다.",
        required=False,
        default=None,
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[status], responses={200: "Success"})
    def get(self, request):
        """
        Assignee : 상백, 희석

        클라이언트의 요청으로 지금까지 기록된 가계부 리스트 정보를 response 하는 메서드입니다.
        로그인된 유저가 생성한 가계부 리스트에서 삭제가 되지 않은 가계부를 의미합니다.

        쿼리 파라미터로 "status" 키의 값이 "delete"가 들어오는 경우 삭제된 데이터를 보여줍니다.
        """

        data_status = request.GET.get("status", None)
        if data_status == "delete":
            account_books = AccountBook.objects.all().filter(user=request.user, is_deleted=True)

        else:
            account_books = AccountBook.objects.all().filter(user=request.user, is_deleted=False)
        serializer = AccountBooksModelSerializer(account_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AccountBooksModelSerializer)
    def post(self, request):
        """
        Assignee : 상백

        클라이언트의 요청 및 JSON 형태 데이터 입력 시, 가계부 데이터를 생성하는 메서드입니다.
        context 딕셔너리로 로그인된 유저 객체를 보내주어 클라이언트가 유저 id를 입력하지 않게 설정했습니다.
        ex) {"title": "서가앤쿡 목동점","balance": "100000"}
        """
        context = {"user": request.user}
        serializer = AccountBooksModelSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# url : POST api/v1/accountbooks/<obj_id>/records | GET,PUT /api/v1/accountbooks/records/<obj_id>
class AccountBooksRecordAPIView(APIView):
    """
    Assignee : 상백, 희석

    Http method = POST, GET, PUT

    permission = 본인만 조회, 수정

    GET : 가계부 단건 상세 조회
    POST : 가계부 기록 생성
    PUT : 가계부 기록 수정

    """

    permission_classes = [IsOwner]

    def get_object_and_check_permission(self, obj_id):
        """
        Assignee : 상백

        obj_id : int

        input 인자로 AccountBookRecord 객체를 가져와 퍼미션 검사를 하는 메서드입니다.
        DoesNotExist 에러 발생 시 None을 리턴합니다.
        APIView 클래스에 정의된 check_object_permissions 메서드를 override해서 검사를 진행합니다.
        """
        try:
            object = AccountBookRecord.objects.get(id=obj_id)
        except AccountBookRecord.DoesNotExist:
            return

        self.check_object_permissions(self.request, object)
        return object

    @swagger_auto_schema(request_body=no_body)
    def get(self, request, obj_id):
        """
        Assignee : 상백

        obj_id : int

        클라이언트의 요청 및 가계부 기록 고유번호 입력 시, 특정 기록에 대한 내용을 응답하는 메서드입니다.
        설정한 permission_classes로 인해 특정 기록의 작성자가 아닐 경우, 접근이 제한됩니다.
        """
        account_book_record = self.get_object_and_check_permission(obj_id)
        if not account_book_record:
            return Response({"error": "해당 가계부 기록이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response(AccountBooksRecordModelSerializer(account_book_record).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AccountBooksRecordModelSerializer)
    def post(self, request, obj_id):
        """
        Assignee : 상백

        obj_id : int

        클라이언트의 요청 및 가계부 고유번호 입력 시, 해당 가계부에 속한 금액과 메모 기록을 생성하는 메서드입니다.
        context 딕셔너리로 AccountBook 객체를 보내주어 클라이언트가 가계부 id를 입력하지 않게 설정했습니다.
        ex) {"amount": "30000","memo": "현금매출"}
        """
        account_book = get_object_or_404(AccountBook, id=obj_id, is_deleted=False)
        context = {"account_book": account_book}
        serializer = AccountBooksRecordModelSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountBooksRecordModelSerializer)
    def put(self, request, obj_id):
        """
        Assignee : 희석

        obj_id : int

        가계부 기록의 단일 객체 수정을 위한 메서드입니다.
        객체 삭제의 경우 is_deleted 필드의 값을 False에서 True로 변경하는 로직으로 구성됩니다.
        """
        record = self.get_object_and_check_permission(obj_id)
        if not record:
            return Response({"error": "기록이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountBooksRecordModelSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            if request.data["is_deleted"] == True:
                return Response({"message": "기록 삭제 성공!!"}, status=status.HTTP_200_OK)
            elif request.data["is_deleted"] == False:
                return Response({"message": "기록 복구 성공!!"}, status=status.HTTP_200_OK)
        except KeyError:
            pass

        return Response({"message": "기록 수정 성공!!"}, status=status.HTTP_200_OK)


# url : GET, PUT api/v1/accountbooks/<obj_id>
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
            object = AccountBook.objects.get(id=obj_id)
        except AccountBook.DoesNotExist:
            return

        self.check_object_permissions(self.request, object)
        return object

    @swagger_auto_schema(request_body=no_body)
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

    @swagger_auto_schema(request_body=AccountBooksModelSerializer)
    def put(self, request, obj_id):
        """
        Assignee : 희석

        obj_id : int

        가계부 단일 객체 수정을 위한 메서드입니다.
        객체 삭제의 경우 is_deleted 필드의 값을 False에서 True로 변경하는 로직으로 구성됩니다.
        """
        account_book = self.get_object_and_check_permission(obj_id)
        if not account_book:
            return Response({"error": "가계부가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountBooksModelSerializer(account_book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            if request.data["is_deleted"] == True:
                return Response({"message": "가계부 삭제 성공!!"}, status=status.HTTP_200_OK)
            elif request.data["is_deleted"] == False:
                return Response({"message": "가계부 복구 성공!!"}, status=status.HTTP_200_OK)
        except KeyError:
            pass

        return Response({"message": "가계부 수정 성공!!"}, status=status.HTTP_200_OK)
