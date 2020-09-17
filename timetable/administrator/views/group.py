from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse

from administrator.forms import NewClassForm
from models import Class

from .utils import check_admin


@login_required
@user_passes_test(check_admin)
def create(request, *args, **kwargs):
    form = NewClassForm()
    if request.method == "POST":
        form = NewClassForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "administrator/class.html",
                {"form": NewClassForm(request.POST), "query": Class.objects.all()},
            )

    return render(
        request,
        "administrator/class.html",
        {
            "form": form,
            "query": Class.objects.all(),
            "page_title": "Admin | Classes",
            "nav_title": "Classes",
        },
    )


@login_required
@user_passes_test(check_admin)
def delete(request, *args, **kwargs):
    get_object_or_404(Class, pk=kwargs["id"]).delete()
    messages.success(request, "Class deleted successfully", extra_tags="alert")
    return redirect(reverse("admin.class.index"))
