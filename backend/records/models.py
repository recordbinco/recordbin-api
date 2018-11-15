import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)

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
        return Record.objects.create(data=validated_data)

    def to_internal_value(self, request_data):
        """ Pass through to pass data as is and ignore model fields """
        # www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data
        return request_data


ALL_MODELS = [Record]
