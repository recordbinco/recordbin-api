import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers

from .base import BaseModel


class Record(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(
        "App", related_name="records", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super(Record, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ["created_on"]


class RecordSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()  # Needed?
    app = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Record
        fields = ("id", "created_on", "data", "app")

    def create(self, validated_data):
        """ Override create to ensure received data is stored in data field """
        # app_id injected by view:perform_create
        app_id = validated_data.pop("app_id")
        return Record.objects.create(app_id=app_id, data=validated_data)

    def to_internal_value(self, request_data):
        """ Pass through to pass data as is and ignore model fields """
        # www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data
        return request_data
