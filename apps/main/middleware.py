# apps/core/middleware.py
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from apps.main.models import School

class SubdomainMiddleware(MiddlewareMixin):
    
    # List of URL patterns that should be excluded from school checking
    EXCLUDED_PATHS = [
        '/admin/',
        '/api/check-school/',
    ]
    
    def process_request(self, request):
        # Initialize request attributes
        request.subdomain = None
        request.school = None
        
        # Check if current path should be excluded from school checking
        current_path = request.path
        for excluded_path in self.EXCLUDED_PATHS:
            if current_path.startswith(excluded_path):
                # Skip school checking for excluded paths
                return
        
        # Check for School header from frontend
        school_header = request.META.get('HTTP_SCHOOL', None)
        
        # If header exists and not empty
        if school_header and school_header.strip():
            # Use the header value as subdomain
            subdomain = school_header.lower().strip()
            request.subdomain = subdomain
            
            try:
                school = School.objects.get(domain=subdomain)
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
        
        # If no header or empty, subdomain and school remain None
