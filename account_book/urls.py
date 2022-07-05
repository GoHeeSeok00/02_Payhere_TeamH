from django.urls import path

from .views import AccountBooksAPIView

app_name = "account_book"

urlpatterns = [
    path("api/v1/accountbooks/", AccountBooksAPIView.as_view()),
]
