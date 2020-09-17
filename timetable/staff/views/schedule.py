import json

import arrow
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from models import (
    AcademicYear,
    Class,
    Course,
    LectureSchedule,
    Schedule,
    ScheduleTemplate,
    Venue,
)


@login_required
def approved(request):
    context = {
        "nav_title": "Approved Schedules",
        "courses": Course.objects.all(),
        "classes": Class.objects.all(),
        "venues": Venue.objects.all(),
        "academic_years": AcademicYear.objects.all(),
        "schedules": Schedule.objects.filter(
            status="approved", lecturer=request.user.id
        ),
    }
    return render(request, "staff/schedule/approved.html", context)


@login_required
def outgoing(request):
    context = {
        "nav_title": "Outgoing Schedules",
        "schedules": Schedule.objects.filter(
            status="outgoing",
            lecturer=request.user.id,
            academic_year=AcademicYear.objects.current().id,
        ),
    }
    return render(request, "staff/schedule/outgoing.html", context)


@login_required
def rejected(request):
    context = {
        "nav_title": "Rejected Schedules",
        "schedules": Schedule.objects.filter(
            status="rejected",
            lecturer=request.user.id,
            academic_year=AcademicYear.objects.current().id,
        ),
    }
    return render(request, "staff/schedule/rejected.html", context)


@login_required
def await_approval(request, *args, **kwargs):
    Schedule.objects.filter(id=kwargs["id"]).update(status="outgoing")
    messages.success(
        request, "Schedule submitted for approval successfully", extra_tags="alert"
    )
    return redirect(reverse("staff.schedule.index"))


@login_required
def index(request):
    context = {
        "courses": Course.objects.all(),
        "classes": Class.objects.all(),
        "venues": Venue.objects.all(),
        "academic_years": AcademicYear.objects.all(),
        "schedules": Schedule.objects.all(),
        "nav_title": "Schedules Setup",
        "page_title": "Schedules | Setup",
    }
    if request.method == "POST":
        template = Schedule(
            group=Class.objects.get(pk=request.POST.get("class", "")),
            academic_year=AcademicYear.objects.current(),
            lecturer=request.user,
        )
        template.save()

        for c in request.POST.get("courses[]", []):
            course = Course.objects.get(pk=int(c))
            template.courses.add(course)

        for c in request.POST.get("venues[]", []):
            venue = Venue.objects.get(pk=int(c))
            template.venues.add(venue)

        template.save()
        return redirect(reverse("staff.schedule.index"))

    return render(request, "staff/schedule/index.html", context)


@login_required
def view(request, *args, **kwargs):
    schedules = get_object_or_404(Schedule, pk=kwargs["id"])
    context = {
        "next": request.GET.get("next"),
        "lectures": LectureSchedule.objects.schedules(schedules.id, request.user.id),
    }
    return render(request, "staff/schedule/view.html", context)


@login_required
def template_courses(request, *args, **kwargs):
    data = ScheduleTemplate.objects.courses(kwargs["class_id"])
    output = [{"id": c.id, "text": f"{c.code} {c.title}"} for c in data]

    return JsonResponse({"results": output})


@login_required
def template_venues(request, *args, **kwargs):
    data = ScheduleTemplate.objects.venues(kwargs["class_id"])
    output = [{"id": v.id, "text": v.name} for v in data]

    return JsonResponse({"results": output})


@csrf_exempt
def setup(request, *args, **kwargs):
    schedules = get_object_or_404(Schedule, pk=kwargs["id"])

    if request.method == "POST":
        data = json.loads(request.body)
        # TODO: handle request processing errors
        for event in data:
            user_data = event["userData"]
            if not event["disabled"] and len(user_data) > 0:
                LectureSchedule.objects.update_or_create(
                    schedule_template=get_object_or_404(Schedule, pk=kwargs["id"]),
                    day=event["location"],
                    course=Course.objects.get(pk=int(user_data["course_id"])),
                    group=schedules.group,
                    venue=Venue.objects.get(pk=int(user_data["venue_id"])),
                    start_time=str(arrow.get(event["start"]).time()),
                    end_time=str(arrow.get(event["end"]).time()),
                    lecturer=request.user,
                    academic_year=AcademicYear.objects.current(),
                )

        return JsonResponse(
            {"status": "success", "message": "Timetable data saved successfully"}
        )

    context = {
        "courses": Schedule.objects.courses(schedules.group.id),
        "venues": Schedule.objects.venues(schedules.group.id),
        "schedules": schedules,
        "lectures": LectureSchedule.objects.schedules(schedules.id, request.user.id),
    }
    return render(request, "staff/schedule/new.html", context)


@login_required
def delete(request, *args, **kwargs):
    get_object_or_404(Schedule, pk=kwargs["id"]).delete()
    messages.success(request, "Schedule deleted successfully", extra_tags="alert")
    return redirect(reverse("staff.schedule.index"))
