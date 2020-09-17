from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse

from administrator.forms import AcademicYearForm
from models import AcademicYear

from .utils import check_admin

# TODO: Implement editing of forms


@login_required
@user_passes_test(check_admin)
def create(request):
    add = AcademicYearForm(prefix="add-year")

    if request.method == "POST":
        add = AcademicYearForm(request.POST, prefix="add-year")
        if add.is_valid():
            add.save()
            return redirect(reverse("academic.year.index"))

    context = {
        "add_year": add,
        "academic_years": AcademicYear.objects.all(),
        "page_title": "Admin | Academic Years",
        "nav_title": "Academic Years",
    }
    return render(request, "administrator/academic_year.html", context)


@login_required
@user_passes_test(check_admin)
def delete(request, *args, **kwargs):
    get_object_or_404(AcademicYear, pk=kwargs["id"]).delete()
    messages.success(request, "Item deleted successfully", extra_tags="alert")
    return redirect(reverse("academic.year.index"))
