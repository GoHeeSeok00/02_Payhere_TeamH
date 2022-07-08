from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account_book.urls")),
    path("api/", include("user.urls")),
]

# swagger 화면 Info 설정
schema_view_v1 = get_schema_view(
    openapi.Info(
        title="PAYHERE API",
        default_version="v1",
        description="PAYHERE API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# swagger 관련 url
urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view_v1.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view_v1.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view_v1.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
