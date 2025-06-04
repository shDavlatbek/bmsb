# apps/core/middleware.py
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from apps.main.models import School

class SubdomainMiddleware(MiddlewareMixin):
    MAIN_SITE_SUBDOMAINS = {"www", ""}

    def process_request(self, request):
        host = request.get_host().split(":")[0]
        parts = host.split(".")
        request.subdomain = None
        request.school    = None

        if len(parts) > 2:
            sub = parts[0]
        elif len(parts) == 2:
            sub = ""
        else:
            sub = parts[0]

        if sub not in self.MAIN_SITE_SUBDOMAINS:
            request.subdomain = sub
            try:
                school = School.objects.get(domain=sub)
                if school.is_active:
                    request.school = school
                else:
                    raise Http404("Maktab faol emas")
            except School.DoesNotExist:
                raise Http404("Maktab topilmadi")
            except Http404:
                # Re-raise Http404 exceptions to properly display 404 pages
                raise
            except Exception as e:
                # Only catch other exceptions, not Http404
                print(f"Unexpected error in SubdomainMiddleware: {e}")
                # Don't set request.school, leaving it as None
