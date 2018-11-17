import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from rest_framework import serializers


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="records", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super(Record, self).save(*args, **kwargs)

    def __str__(self, **kwargs):
        cls_name = self.__class__.__name__
        short_id = str(self.id).split("-")[0]
        return f"<{cls_name} id=({short_id})>"

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ["created_on"]


class RecordSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = Record
        fields = ("id", "created_on", "data")

    def create(self, validated_data):
        """ Override create to ensure received data is stored in data field """
        # user_id injected by view:perform_create
        user_id = validated_data.pop("user_id")
        return Record.objects.create(user_id=user_id, data=validated_data)

    def to_internal_value(self, request_data):
        """ Pass through to pass data as is and ignore model fields """
        # www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data
        return request_data


ALL_MODELS = [Record]
