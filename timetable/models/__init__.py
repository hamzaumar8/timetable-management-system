from .academic_year import AcademicYear
from .course import Course
from .group import Group as Class
from .lecture_schedule import LectureSchedule
from .registration import Registration
from .schedule import Schedule
from .schedule_template import ScheduleTemplate
from .venue import Venue

__all__ = [
    "Registration",
    "Course",
    "Class",
    "AcademicYear",
    "ScheduleTemplate",
    "Venue",
    "Schedule",
    "LectureSchedule",
]
