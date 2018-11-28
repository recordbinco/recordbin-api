"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import routers


from .docs import doc_urlpatterns
from .tableau_connector import tablea_urlpatterns
from .recordbin.views import RecordViewSet, SourceViewSet, SourceTokenViewSet

# TODO
# from rest_framework.authtoken.views import obtain_auth_token

# path("api/v1/token/", obtain_auth_token),

index_view = never_cache(TemplateView.as_view(template_name="index.html"))

router = routers.DefaultRouter()
router.register("records", RecordViewSet)
router.register("sources", SourceViewSet)
router.register("tokens", SourceTokenViewSet)

urlpatterns = [
    path("api/v1/", include((router.urls, "records"), namespace="v1")),
    path("", admin.site.urls),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    *tablea_urlpatterns,
    *doc_urlpatterns,
]
