from django.db import models


class BaseModel(models.Model):
    def __repr__(self, **kwargs):
        cls_name = self.__class__.__name__
        short_id = str(self.id).split("-")[0]
        return f"<{cls_name} id=({short_id})>"

    class Meta:
        abstract = True
