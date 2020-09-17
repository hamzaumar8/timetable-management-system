from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=False, null=False)
    title = models.CharField(max_length=150, blank=False, null=False)
    credit_hours = models.IntegerField(blank=False)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta(object):
        db_table = "course"
        app_label = "administrator"
