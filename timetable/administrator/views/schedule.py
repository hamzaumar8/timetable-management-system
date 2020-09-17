from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse

from models import AcademicYear, Class, Course, Schedule, ScheduleTemplate, Venue

from .utils import check_admin


@login_required
@user_passes_test(check_admin)
def index(request):
    context = {
        "courses": Course.objects.all(),
        "classes": Class.objects.all(),
        "venues": Venue.objects.all(),
        "schedules": ScheduleTemplate.objects.all(),
        "page_title": "Admin | Schedule Template",
        "nav_title": "Schedule Templates",
    }

    if request.method == "POST":
        template = ScheduleTemplate(
            group=Class.objects.get(pk=request.POST.get("class", "")),
            academic_year=AcademicYear.objects.current(),
        )
        template.save()

        for c in request.POST.get("courses[]", []):
            course = Course.objects.get(pk=int(c))
            print(c)
            template.courses.add(course)

        for c in request.POST.get("venues[]", []):
            venue = Venue.objects.get(pk=int(c))
            print(c)
            template.venues.add(venue)

        template.save()

    return render(request, "administrator/schedule/new.html", context)


def approve_schedule(request, *args, **kwargs):
    data = get_object_or_404(Schedule, pk=kwargs["id"])
    data.status = "approved"
    data.save()

    messages.success(request, "Schedule approved successfully", extra_tags="alert")
    return redirect(request.GET.get("next"))


def reject_schedule(request, *args, **kwargs):
    data = get_object_or_404(Schedule, pk=kwargs["id"])
    data.status = "rejected"
    data.save()

    messages.success(request, "Schedule rejected successfully", extra_tags="alert")
    return redirect(request.GET.get("next"))


def approved(request):
    context = {
        "title": "Approved Schedules",
        "schedules": Schedule.objects.filter(
            status="approved", academic_year=AcademicYear.objects.current()
        ),
        "page_title": "Admin | Approved Schedules",
        "nav_title": "Approved Schedules",
    }
    return render(request, "administrator/schedule/approvals.html", context)


def incoming(request):
    context = {
        "title": "Incoming Schedules",
        "schedules": Schedule.objects.filter(
            status="outgoing", academic_year=AcademicYear.objects.current()
        ),
        "page_title": "Admin | Incoming Schedules",
        "nav_title": "Incoming Schedules",
    }
    return render(request, "administrator/schedule/incoming.html", context)


def rejected(request):
    context = {
        "title": "Rejected Schedules",
        "schedules": Schedule.objects.filter(
            status="rejected", academic_year=AcademicYear.objects.current()
        ),
        "page_title": "Admin | Rejected Schedules",
        "nav_title": "Rejected Schedules",
    }
    return render(request, "administrator/schedule/rejected.html", context)


@login_required
@user_passes_test(check_admin)
def delete_template(request, *args, **kwargs):
    get_object_or_404(ScheduleTemplate, pk=kwargs["id"]).delete()
    messages.success(request, "Schedule deleted successfully", extra_tags="alert")

    url = request.GET.get("next", None)
    if url is None:
        return redirect(reverse("admin.schedules.index"))

    return redirect(url)


@login_required
@user_passes_test(check_admin)
def delete_schedule(request, *args, **kwargs):
    get_object_or_404(Schedule, pk=kwargs["id"]).delete()
    messages.success(request, "Schedule deleted successfully", extra_tags="alert")

    url = request.GET.get("next", None)
    if url is None:
        return redirect(reverse("admin.schedules.index"))

    return redirect(url)
