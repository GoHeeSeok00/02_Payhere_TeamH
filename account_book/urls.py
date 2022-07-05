from django.urls import path

from .views import AccountBooksAPIView, AccountBooksDetailAPIView

app_name = "account_book"

urlpatterns = [
    path("api/v1/accountbooks/", AccountBooksAPIView.as_view()),
    path("api/v1/accountbooks/<obj_id>/", AccountBooksDetailAPIView.as_view()),
]
