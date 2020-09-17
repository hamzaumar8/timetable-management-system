from django.db import models


class Registration(models.Model):
    email = models.EmailField(blank=False, unique=True)
    pending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = "registration"
        app_label = "administrator"
