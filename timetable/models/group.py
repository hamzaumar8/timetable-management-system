from django.db import models
from django.utils.timezone import now


class Group(models.Model):
    program = models.CharField(max_length=200, blank=False, null=False)
    size = models.IntegerField(null=False, blank=False)
    admission_year = models.DateField(blank=False, null=False, default=now)
    completion_year = models.DateField(blank=False, null=False)

    class Meta(object):
        db_table = "class"
        app_label = "administrator"

    def level(self):
        return (now().year - self.admission_year.year + 1) * 100
