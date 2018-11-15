# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest

# from django.db.utils import IntegrityError
from backend.distribution.models import ALL_MODELS


@pytest.mark.django_db
@pytest.mark.parametrize("model", ALL_MODELS)
def test_models_repr(model):
    assert model.objects.first()
    assert repr(model.objects.first())


# @pytest.mark.django_db
# def test_unique_docs():
#     version = Version.objects.first()
#     doc = Document(version=version, filename='xxx', html='123')
#     doc.save()
#     with pytest.raises(IntegrityError):
#         doc = Document(version=version, filename='xxx', html='123')
#         doc.save()
