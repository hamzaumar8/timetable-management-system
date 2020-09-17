from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse as render
from django.urls import reverse

from administrator.forms import AddVenueForm
from models import Venue

from .utils import check_admin


@login_required
@user_passes_test(check_admin)
def index(request, *args, **kwargs):
    form_data = AddVenueForm()
    if request.method == "POST":
        form_data = AddVenueForm(request.POST)
        if form_data.is_valid():
            form_data.save()

    return render(
        request,
        "administrator/venue.html",
        {
            "form": form_data,
            "venues": Venue.objects.all(),
            "page_title": "Admin | Venues",
            "nav_title": "Venues",
        },
    )


@login_required
@user_passes_test(check_admin)
def delete(request, *args, **kwargs):
    get_object_or_404(Venue, pk=kwargs["id"]).delete()

    messages.success(request, "Venue deleted successfully", extra_tags="alert")
    return redirect(reverse("admin.venue.index"))


# TODO: Add editing of venue
