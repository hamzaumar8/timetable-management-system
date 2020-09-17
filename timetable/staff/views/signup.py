import django.http as http
import itsdangerous
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from models import Registration
from staff.forms.signup_form import SignupForm


def create(request, *args, **kwargs):
    serializer = itsdangerous.TimedSerializer(
        settings.ITSDANGEROUS_KEY,
        serializer=itsdangerous.URLSafeSerializer(settings.ITSDANGEROUS_KEY),
    )

    try:
        email = serializer.loads(
            kwargs["token"], max_age=settings.ITSDANGEROUS_EXPIRE_PERIOD, salt="signup"
        )
        Registration.objects.filter(email=email).update(pending=False)
    except itsdangerous.SignatureExpired:
        msg = "Link has expired. Please contact department administrator for new link"
        return http.HttpResponse(msg)
    except itsdangerous.BadSignature:
        return http.HttpResponseNotFound("Page Not Found")

    form = SignupForm(prefix="user_form")
    if request.method == "POST":
        form = SignupForm(request.POST, prefix="user_form")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully. Please login to proceed",
                extra_tags="alert",
            )
            return http.HttpResponseRedirect(reverse("login"))

    context = {"user_form": form, "title": "Registration"}
    return render(request, "staff/signup.html", context)


# # FIXME: check if registration email pending is false
# def registration(request, *args, **kwargs):
#     serializer = itsdangerous.TimedSerializer(
#         settings.ITSDANGEROUS_KEY,
#         serializer=itsdangerous.URLSafeSerializer(settings.ITSDANGEROUS_KEY),
#     )

#     try:
#         email = serializer.loads(
#             kwargs["token"], max_age=settings.ITSDANGEROUS_EXPIRE_PERIOD, salt="signup"
#         )
#         Registration.objects.filter(email=email).update(pending=False)
#     except itsdangerous.SignatureExpired:
#         msg = "Link has expired. Please contact department administrator for new link"
#         return http.HttpResponse(msg)
#     except itsdangerous.BadSignature:
#         return http.HttpResponseNotFound("Page Not Found")

#     form = SignupForm(prefix="user_form")
#     if request.method == "POST":
#         form = SignupForm(request.POST, prefix="user_form")
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request,
#                 "Account created successfully. Please login to proceed",
#                 extra_tags="alert",
#             )
#             return http.HttpResponseRedirect(reverse("login"))

#     context = {"user_form": form, "title": "Registration"}
#     return render(request, "timetable/signup.html", context)
