import uuid
import binascii
import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .base import BaseModel

class App(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="apps", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "App"
        verbose_name_plural = "Apps"


class AppSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = App
        fields = ("id", "created_on", "name", "owner")


class AppToken(models.Model):
    """ DRF authorization token model > Modified: Removes User """

    key = models.CharField("Key", max_length=40, primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App, related_name="tokens", on_delete=models.CASCADE)
    permission_choices = (
        ('R', 'Read'),
        ('W', 'Write'),
        ('RW', 'Read and Write'),
    )
    permissions = models.CharField(max_length=2, choices=permission_choices)

    class Meta:
        verbose_name = "App Token"
        verbose_name_plural = "App Tokens"

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super().save(*args, **kwargs)


class AppTokenSerializer(serializers.ModelSerializer):
    app = serializers.SlugRelatedField(
        many=False, queryset=App.objects.all(), read_only=False, slug_field="name"
    )

    class Meta:
        model = AppToken
        fields = ("key", "created_on", "app")

