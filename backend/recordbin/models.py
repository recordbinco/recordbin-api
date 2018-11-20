import uuid
import binascii
import os
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers


class BaseModel(models.Model):
    def __str__(self, **kwargs):
        cls_name = self.__class__.__name__
        short_id = str(self.id).split("-")[0]
        return f"<{cls_name} id=({short_id})>"
        # Record.objects.first() # TODO
        # <Record: <Record id=(01baf783)>

    class Meta:
        abstract = True


class Record(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(
        "Source", related_name="records", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super(Record, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ["created_on"]


class RecordSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()  # Needed?
    source = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Record
        fields = ("id", "created_on", "data", "source")

    def create(self, validated_data):
        """ Override create to ensure received data is stored in data field """
        # source_id injected by view:perform_create
        source_id = validated_data.pop("source_id")
        return Record.objects.create(source_id=source_id, data=validated_data)

    def to_internal_value(self, request_data):
        """ Pass through to pass data as is and ignore model fields """
        # www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data
        return request_data


class Source(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sources", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Record Source"
        verbose_name_plural = "Record Sources"


class SourceSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Source
        fields = ("id", "created_on", "name", "owner")


class SourceToken(models.Model):
    """ DRF authorization token model > Modified: Removes User """

    key = models.CharField("Key", max_length=40, primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, related_name="tokens", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Source Token"
        verbose_name_plural = "Source Tokens"

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super().save(*args, **kwargs)


class SourceTokenSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        many=False, queryset=Source.objects.all(), read_only=False, slug_field="name"
    )

    class Meta:
        model = SourceToken
        fields = ("key", "created_on", "source")


ALL_MODELS = [Record, Source, SourceToken]
