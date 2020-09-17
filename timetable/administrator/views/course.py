from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse

from administrator.forms import NewCourseForm
from models import Course

from .utils import check_admin


@login_required
@user_passes_test(check_admin)
def create(request):
    new_course = NewCourseForm(prefix="add-course")
    if request.method == "POST":
        new_course = NewCourseForm(request.POST, prefix="add-course")
        if new_course.is_valid():
            new_course.save()
    context = {
        "new_course": new_course,
        "courses": Course.objects.all(),
        "page_title": " Admin | Courses",
        "nav_title": "Courses",
    }
    return render(request, "administrator/courses.html", context)


@login_required
@user_passes_test(check_admin)
def delete(request, *args, **kwargs):
    get_object_or_404(Course, pk=kwargs["id"]).delete()
    messages.success(request, "Course deleted successfully", extra_tags="alert")
    return redirect(reverse("admin.course.index"))
