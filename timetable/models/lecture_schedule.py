import json

from django.contrib.auth.models import User
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from models import AcademicYear, Class, Course

from .schedule import Schedule
from .venue import Venue


class LectureScheduleManager(models.Manager):
    def schedules(self, templated_id=None, lecturer_id=None):
        results = (
            super()
            .get_queryset()
            .filter(
                academic_year=AcademicYear.objects.current(),
                group=Schedule.objects.get(id=templated_id).group.id,
            )
        )

        output = []
        for item in results:
            output.append(
                {
                    "name": f"{item.course.title} @ {item.venue.name}",
                    "start": str(item.start_time),
                    "end": str(item.end_time),
                    "day": item.day,
                    "disabled": item.lecturer.id != lecturer_id,
                }
            )
        return json.dumps(output)


# TODO: Review foriegn keys on delete rules
class LectureSchedule(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    schedule_template = models.ForeignKey(
        Schedule, null=False, on_delete=models.CASCADE
    )
    day = models.CharField(max_length=50, blank=False, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)

    objects = LectureScheduleManager()

    class Meta(object):
        db_table = "lecture_schedule"
        app_label = "staff"
