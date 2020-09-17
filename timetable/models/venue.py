from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class Venue(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=150, unique=True, blank=False)
    capacity = models.IntegerField(null=True)

    class Meta(object):
        db_table = "venue"
        app_label = "administrator"
