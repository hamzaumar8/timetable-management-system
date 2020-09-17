from django.shortcuts import redirect
from django.urls import reverse


def check_user(request):
    if request.user.is_superuser:
        return redirect(reverse("admin.dashboard"), permanent=True)
    else:
        return redirect(reverse("staff.dashboard"), permanent=True)
