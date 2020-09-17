from django.db import models as db

from models import AcademicYear, Class, Course

from .venue import Venue


class ScheduleTemplateManager(db.Manager):
    def courses(self, group_id=None):
        results = (
            super()
            .get_queryset()
            .filter(
                academic_year=AcademicYear.objects.current(),
                group=Class.objects.get(id=group_id),
            )
        ).only("courses")

        data = []
        for item in results:
            data.extend(item.courses.all())

        return data

    def venues(self, group_id=None):
        results = (
            super()
            .get_queryset()
            .filter(
                academic_year=AcademicYear.objects.current(),
                group=Class.objects.get(id=group_id),
            )
        ).only("venues")

        data = []
        for item in results:
            data.extend(item.venues.all())

        return data


class ScheduleTemplate(db.Model):
    group = db.ForeignKey(Class, on_delete=db.CASCADE, null=True)
    academic_year = db.ForeignKey(AcademicYear, on_delete=db.CASCADE, null=True)
    courses = db.ManyToManyField(Course)
    venues = db.ManyToManyField(Venue)

    objects = ScheduleTemplateManager()

    class Meta(object):
        db_table = "schedule_template"
        app_label = "administrator"
