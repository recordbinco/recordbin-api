# https://jet.readthedocs.io/en/latest/config_file.html
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#inlinemodeladmin-objects
from django.contrib import admin

# from django.utils.html import format_html
# from django.urls import reverse

from .models import Record


# def linkify(field_name):
#     """
#     Converts a foreign key value into clickable links.

#     If field_name is 'parent', link text will be str(obj.parent)
#     Link will be admin url for the admin url for obj.parent.id:change
#     """
#     # docs.djangoproject.com/en/2.1/ref/contrib/admin/#reversing-admin-urls
#     def _linkify(obj):
#         app_label = obj._meta.app_label
#         linked_obj = getattr(obj, field_name)
#         model_name = linked_obj._meta.model_name
#         view_name = f"admin:{app_label}_{model_name}_change"
#         link_url = reverse(view_name, args=[str(linked_obj.id)])
#         return format_html('<a href="{}">{}</a>', link_url, linked_obj)

#     _linkify.short_description = field_name
#     return _linkify


class BaseModel(admin.ModelAdmin):
    view_on_site = False

    def short_id(self, obj):
        return f"{str(obj.id).split('-')[0]}"


# class SpaceTypeSkuInstanceInline(admin.TabularInline):
#     model = SpaceTypeSkuInstance


@admin.register(Record)
class RecordAdmin(BaseModel):
    list_display = ["short_id", "created_on"]
    # list_filter = ["program_type__name"]
