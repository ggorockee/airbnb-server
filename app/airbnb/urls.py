from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import HelathCheck


schema_view = get_schema_view(
    openapi.Info(
        title="Airbnb API by ggorockee",
        default_version="v1.0.0",
        description="Airbnb API by ggorockee",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/ready", HelathCheck.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        # other user API end-point URL
        re_path(
            r"^docs(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^docs/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
