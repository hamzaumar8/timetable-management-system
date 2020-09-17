from django.template.response import TemplateResponse as render


def index(request):
    return render(request, "administrator/layout.html", {"nav_title": "Dashboard"})
