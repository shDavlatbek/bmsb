from django.contrib import admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from urllib.parse import urljoin
from drf_yasg.utils import swagger_auto_schema
from .models import TinyMCEImage


@csrf_exempt  # Note: For production, consider a more secure approach for CSRF
@login_required  # Optional: Restrict uploads to authenticated users
@swagger_auto_schema(schema=None, auto_schema=None)
def upload_image(request):
    """Handle image uploads from TinyMCE editor."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Check if file is an image
    if not uploaded_file.content_type.startswith('image/'):
        return JsonResponse({'error': 'File is not an image'}, status=400)
    
    # Create a new image record
    image = TinyMCEImage(title=uploaded_file.name)
    image.image = uploaded_file
    image.save()
    
    # Get the absolute URL by combining the site URL with the media URL
    site_url = request.build_absolute_uri('/').rstrip('/')
    relative_url = image.image.url
    
    # Ensure we have an absolute URL
    if relative_url.startswith('/'):
        # Already a root-relative URL, just add the site domain
        absolute_url = f"{site_url}{relative_url}"
    else:
        # Combine with the site URL
        absolute_url = urljoin(site_url, relative_url)
    
    # Return the absolute URL to the image
    return JsonResponse({
        'location': absolute_url,  # Absolute URL for TinyMCE
        'success': True
    })