from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import ListView
from itsdangerous import TimedSerializer, URLSafeSerializer
from models import Registration


# @login_required
# @user_passes_test(check_admin)
def delete_email(request, *args, **kwargs):
    get_object_or_404(Registration, pk=kwargs["id"]).delete()
    messages.success(request, "Email deleted successfully", extra_tags="alert")
    return redirect(reverse("staff-management"))


class RegistrationEmail(UserPassesTestMixin, ListView):
    model = Registration
    template_name = "administrator/new_staff.html"

    def test_func(self):
        return self.request.user.is_superuser

    def generate_signup_token(self, email):
        serializer = TimedSerializer(
            settings.ITSDANGEROUS_KEY,
            serializer=URLSafeSerializer(settings.ITSDANGEROUS_KEY),
        )
        return serializer.dumps(email, salt="signup")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", None)
        if email is not None:
            url = request.build_absolute_uri(
                reverse("signup", kwargs={"token": self.generate_signup_token(email)})
            )
            html = get_template("registration/email.html")
            content = html.render({"url": url})
            msg = "Kindly visit %s to create an account" % url
            send_mail(
                "Computer Science & I.T Department Timetable Registration",
                msg,
                "admin@citsatimetable.com",
                [email],
                fail_silently=False,
                html_message=content,
            )
            Registration(email=email).save()
            messages.success(
                request, "Registration email sent successfully", extra_tags="alert"
            )
            return super().get(request)
        else:
            messages.warning(request, "An error occured while sending email")
        return render(request, self.template_name, {})
