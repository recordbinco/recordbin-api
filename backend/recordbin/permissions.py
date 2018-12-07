from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token as UserToken
from .models import AppToken


class AppTokenReadWritePermission(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.auth, AppToken):
            permissions = request.auth.permissions
            if request.method == "GET":
                return "R" in permissions
            if request.method == "POST":
                return "W" in permissions
        if isinstance(request.auth, UserToken):
            return request.method == "GET"
        return True
