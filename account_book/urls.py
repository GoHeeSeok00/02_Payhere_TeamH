from django.urls import path

from .views import (
    AccountBooksAPIView,
    AccountBooksDetailAPIView,
    AccountBooksDetailRecoveryAPIView,
    AccountBooksRecordAPIView,
    AccountBooksRecordDetailAPIView,
    AccountBooksRecordDetailRecoveryAPIView,
)

app_name = "account_book"

urlpatterns = [
    path("api/v1/accountbooks", AccountBooksAPIView.as_view()),
    path("api/v1/accountbooks/<accountbook_id>", AccountBooksDetailAPIView.as_view()),
    path("api/v1/accountbooks/<accountbook_id>/recovery", AccountBooksDetailRecoveryAPIView.as_view()),
    path("api/v1/accountbooks/<accountbook_id>/records", AccountBooksRecordAPIView.as_view()),
    path("api/v1/accountbooks/records/<record_id>", AccountBooksRecordDetailAPIView.as_view()),
    path("api/v1/accountbooks/records/<record_id>/recovery", AccountBooksRecordDetailRecoveryAPIView.as_view()),
]
