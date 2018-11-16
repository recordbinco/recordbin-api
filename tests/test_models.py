import pytest

from backend.recordbin.models import ALL_MODELS


@pytest.mark.django_db
@pytest.mark.parametrize("model", ALL_MODELS)
def test_models_repr(model):
    from django.conf import settings

    print(settings.DATABASES)
    assert model.objects.first()
    assert repr(model.objects.first())
