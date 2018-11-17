import pytest

from backend.recordbin.models import ALL_MODELS


@pytest.mark.django_db
@pytest.mark.parametrize("model", ALL_MODELS)
def test_models_repr(model):
    assert model.objects.first()
    assert repr(model.objects.first())
