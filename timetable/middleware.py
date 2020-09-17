from django.utils.deprecation import MiddlewareMixin

from models import AcademicYear, Schedule


class SchedulesTemplateMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            # TODO: Replace this with permissions instead
            if request.user.is_superuser:
                context = {
                    "total_approved": Schedule.objects.filter(
                        status="approved", academic_year=AcademicYear.objects.current()
                    ).count(),
                    "total_outgoing": Schedule.objects.filter(
                        status="outgoing", academic_year=AcademicYear.objects.current()
                    ).count(),
                    "total_rejected": Schedule.objects.filter(
                        status="rejected", academic_year=AcademicYear.objects.current()
                    ).count(),
                }
            else:
                context = {
                    "total_approved": Schedule.objects.filter(
                        status="approved",
                        academic_year=AcademicYear.objects.current(),
                        lecturer=request.user.id,
                    ).count(),
                    "total_outgoing": Schedule.objects.filter(
                        status="outgoing",
                        academic_year=AcademicYear.objects.current(),
                        lecturer=request.user.id,
                    ).count(),
                    "total_rejected": Schedule.objects.filter(
                        status="rejected",
                        academic_year=AcademicYear.objects.current(),
                        lecturer=request.user.id,
                    ).count(),
                }
            response.context_data.update(context)
        return response
