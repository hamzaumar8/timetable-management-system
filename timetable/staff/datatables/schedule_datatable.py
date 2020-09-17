import django_filters
import django_tables2 as tables

from models import Schedule


class ScheduleTable(tables.Table):
    class Meta:
        model = Schedule
        template_name = "django_tables2/bootstrap4.html"
        fields = ("venue", "course")


class ScheduleFilter(django_filters.FilterSet):
    class Meta:
        model = Schedule
        fields = ["venue", "course"]
