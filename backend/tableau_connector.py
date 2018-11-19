from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

connector = never_cache(
    xframe_options_exempt(TemplateView.as_view(template_name="connector.html"))
)


@xframe_options_exempt
def connection_data(request):
    data = {
        "connections": [
            {
                "alias": "Record Bin",
                "tables": [{"id": "records", "alias": "Records"}],
                "joins": [],
            }
        ]
    }
    return JsonResponse(data)


@xframe_options_exempt
def table_info(request):
    data = {
        "tables": [
            {
                "id": "records",
                "alias": "Records",
                "columns": [
                    {
                        "id": "id",
                        "alias": "id",
                        "dataType": "string",
                        "description": "Record Id",
                    },
                    {
                        "id": "created_on",
                        "alias": "Created On",
                        "dataType": "string",
                        "description": "Record Timestamp",
                    },
                    {
                        "id": "data",
                        "alias": "Data",
                        "dataType": "string",
                        "description": "Record Data",
                    },
                    {"id": "user", "alias": "Username", "dataType": "string"},
                ],
            }
        ]
    }
    return JsonResponse(data)


tablea_urlpatterns = [
    path("connector/", connector),
    path("connector/tableinfo.json", table_info),
    path("connector/connectiondata.json", connection_data),
]
