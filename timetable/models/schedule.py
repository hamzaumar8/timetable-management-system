from django.contrib.auth.models import User
from django.core import serializers
from django.db import models as db

from models import AcademicYear, Class, Course

from .venue import Venue


class ScheduleManager(db.Manager):
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


class Schedule(db.Model):
    group = db.ForeignKey(Class, on_delete=db.SET_NULL, null=True)
    courses = db.ManyToManyField(Course)
    venues = db.ManyToManyField(Venue)
    academic_year = db.ForeignKey(AcademicYear, on_delete=db.SET_NULL, null=True)
    lecturer = db.ForeignKey(User, on_delete=db.CASCADE)
    status = db.CharField(
        max_length=150,
        choices=[
            ("uncompleted", "Uncompleted"),
            ("pending", "Pending Approval"),
            ("outgoing", "Outgoing"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="uncompleted",
    )

    objects = ScheduleManager()

    class Meta(object):
        db_table = "schedule"
        app_label = "staff"

    def courses_json(self):
        data = self.courses.all()
        return serializers.serialize("json", data)

    def venues_json(self):
        data = self.venues.all()
        return serializers.serialize("json", data)
