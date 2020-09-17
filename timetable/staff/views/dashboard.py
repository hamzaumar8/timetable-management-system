import json

from django.template.response import TemplateResponse as render

from models import AcademicYear, LectureSchedule


def index(request, *args, **kwargs):
    results = LectureSchedule.objects.filter(
        lecturer=request.user.id,
        academic_year=AcademicYear.objects.current(),
        schedule_template__status="approved",
    )

    data = []
    for item in results:
        data.append(
            {
                "name": f"{item.course.title} @ {item.venue.name}",
                "start": str(item.start_time),
                "end": str(item.end_time),
                "day": item.day,
                "disabled": item.lecturer.id != request.user.id,
            }
        )

    context = {
        "next": request.GET.get("next"),
        "lectures": json.dumps(data),
        "nav_title": "Dashboard",
        "back_button": False,
        "page_title": f"{request.user.get_full_name()} | Dashboard",
    }
    return render(request, "staff/layout.html", context)
