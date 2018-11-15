import django_filters
from .models import Record


class RecordFilterSet(django_filters.FilterSet):
    class Meta:
        model = Record
        fields = dict(id=["exact"], created_on=["exact", "gt", "lt"], data=[])
