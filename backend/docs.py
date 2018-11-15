from pathlib import Path
from rest_framework.decorators import api_view
from django.http.response import HttpResponse

from django.urls import re_path, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# https://drf-yasg.readthedocs.io/en/stable/readme.html#installation
schema_view = get_schema_view(
    openapi.Info(
        title="Record Bin",
        default_version="v1",
        description="Record Bin API",
        contact=openapi.Contact(email="gui.talarico+recordbin@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    validators=["flex", "ssv"],
    public=False,
)


@api_view(["GET"])
def openapi_view(request):
    path = Path("openapi.yaml")
    with open(path) as fp:
        data = fp.read()
    return HttpResponse(data)


doc_urlpatterns = [
    path("openapi.yaml", openapi_view),
    # Auto-generated at /_swagger(.yaml|.json)
    re_path(
        r"^_swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
