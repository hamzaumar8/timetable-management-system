from django.urls import path

from .views import dashboard, schedule

# staff urls
urlpatterns = [
    path("dashboard/", dashboard.index, name="staff.dashboard"),
    path("schedule/index", schedule.index, name="staff.schedule.index"),
    path("schedule/<int:id>/view", schedule.view, name="staff.schedule.view"),
    path("schedule/<int:id>/delete", schedule.delete, name="staff.schedule.delete"),
    path("schedule/<int:id>/setup", schedule.setup, name="staff.schedule.setup"),
    path("schedule/<int:id>/setup", schedule.setup, name="staff.schedule.setup.save"),
    path("schedule/outgoing", schedule.outgoing, name="staff.schedule.outgoing"),
    path("schedule/approved", schedule.approved, name="staff.schedule.approved"),
    path("schedule/rejected", schedule.rejected, name="staff.schedule.rejected"),
    path(
        "schedule/<int:id>/await-approval",
        schedule.await_approval,
        name="staff.schedule.await.approval",
    ),
    path(
        "schedule/template/<int:class_id>/courses",
        schedule.template_courses,
        name="staff.template.courses",
    ),
    path(
        "schedule/template/<int:class_id>/venues",
        schedule.template_venues,
        name="staff.template.venues",
    ),
]
