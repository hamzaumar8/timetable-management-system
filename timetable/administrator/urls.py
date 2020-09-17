from django.urls import path

from staff.views import signup

from .views import academic_year, auth, course, dashboard, group, schedule
from .views import staff_manager as staff
from .views import venue

# app_name = "administrator"

# TOOD: add new view for handling index
urlpatterns = [
    path("accounts/auth/", auth.check_user, name="auth"),
    path("dashboard/", dashboard.index, name="admin.dashboard"),
    # lecturers registration
    path(
        "staff/",
        # login_required(admin.StaffManagement.as_view()),
        staff.RegistrationEmail.as_view(),
        name="staff-management",
    ),
    path("signup/<str:token>/", signup.create, name="signup"),
    path("staff/email/<int:id>/", staff.delete_email, name="delete-email"),
    # venue
    path("venue/", venue.index, name="admin.venue.index"),
    path("venue/delete/<int:id>/", venue.delete, name="admin.venue.delete"),
    # course
    path("courses/", course.create, name="admin.course.index"),
    path("courses/delete/<int:id>/", course.delete, name="admin.course.delete"),
    # class
    path("class/", group.create, name="admin.class.index"),
    path("class/delete/<int:id>/", group.delete, name="admin.class.delete"),
    # schedules
    path("schedules/index", schedule.index, name="admin.schedules.index"),
    path(
        "schedules/template/<int:id>/delete",
        schedule.delete_template,
        name="admin.template.delete",
    ),
    path(
        "schedules/delete/<int:id>",
        schedule.delete_schedule,
        name="admin.schedules.delete",
    ),
    path(
        "schedules/<int:id>/approve",
        schedule.approve_schedule,
        name="administrator.schedules.approve",
    ),
    path(
        "schedules/<int:id>/reject",
        schedule.reject_schedule,
        name="administrator.schedules.reject",
    ),
    path(
        "schedules/incoming", schedule.incoming, name="administrator.schedule.incoming"
    ),
    path(
        "schedules/approvals",
        schedule.approved,
        name="administrator.schedule.approvals",
    ),
    path(
        "schedules/rejected", schedule.rejected, name="administrator.schedule.rejected"
    ),
    # academic year
    path("academic-year/index", academic_year.create, name="academic.year.index"),
    path(
        "academic-year/delete/<int:id>/",
        academic_year.delete,
        name="academic.year.delete",
    ),
]
