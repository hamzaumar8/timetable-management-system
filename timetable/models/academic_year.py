from django.db import models
from django.utils.timezone import now


class AcademicYearManager(models.Manager):
    def current(self):
        return super().get_queryset().filter(is_current=True).first()


class AcademicYear(models.Model):
    start_date = models.DateField(blank=False, null=False, default=now)
    end_date = models.DateField(blank=False, null=False)
    semester = models.CharField(
        max_length=150,
        choices=[
            ("first_semester", "First Semester"),
            ("second_semester", "Second Semester"),
        ],
        default="first_semester",
    )
    is_current = models.BooleanField(
        default=False, choices=[(True, "True"), (False, "False")]
    )
    objects = AcademicYearManager()

    class Meta(object):
        db_table = "academic_year"
        app_label = "administrator"

    def full_year(self):
        return "%s/%s - %s" % (
            self.start_date.year,
            self.end_date.year,
            self.semester.title().replace("_", " "),
        )

    def format_semester(self):
        return self.semester.title().replace("_", " ")
