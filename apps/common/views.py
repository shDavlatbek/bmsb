from django.contrib import admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from urllib.parse import urljoin
from drf_yasg.utils import swagger_auto_schema
from .models import TinyMCEImage
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


@csrf_exempt
@login_required
@swagger_auto_schema(schema=None, auto_schema=None)
def upload_image(request):
    """Handle image uploads from TinyMCE editor."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    if not uploaded_file.content_type.startswith('image/'):
        return JsonResponse({'error': 'File is not an image'}, status=400)
    
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


@method_decorator(csrf_exempt, name='dispatch')
class APIDocumentationView(TemplateView):
    template_name = 'api_documentation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current host for API testing
        context['api_base_url'] = f"{self.request.scheme}://{self.request.get_host()}/api"
        
        # API sections with endpoints
        context['api_sections'] = [
            {
                'id': 'maktab',
                'title': 'Maktab',
                'description': 'Maktab haqida umumiy ma\'lumotlar',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/school/',
                        'description': 'Maktab ma\'lumotlarini olish',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/menus/',
                        'description': 'Maktab menyularini olish',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/banners/',
                        'description': 'Banner rasmlarini olish',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/school-lifes/',
                        'description': 'Maktab hayoti rasmlarini olish',
                        'params': []
                    }
                ]
            },
            {
                'id': 'yonalishlar',
                'title': 'Yo\'nalishlar',
                'description': 'Ta\'lim yo\'nalishlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/directions/',
                        'description': 'Barcha yo\'nalishlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/directions/{slug}/',
                        'description': 'Yo\'nalish tafsilotlari',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'oqituvchilar',
                'title': 'O\'qituvchilar',
                'description': 'O\'qituvchilar ro\'yxati va ma\'lumotlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/teachers/',
                        'description': 'Barcha o\'qituvchilar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/teachers/{slug}/',
                        'description': 'O\'qituvchi tafsilotlari',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'xodimlar',
                'title': 'Xodimlar va Rahbarlar',
                'description': 'Maktab xodimlari va rahbarlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/staffs/',
                        'description': 'Barcha xodimlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/leaders/',
                        'description': 'Rahbarlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/leaders/{slug}/',
                        'description': 'Rahbar tafsilotlari',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'faxrlarimiz',
                'title': 'Faxrlarimiz',
                'description': 'Maktab faxrlari va yutuqlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/honors/',
                        'description': 'Barcha faxrlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/honors/{slug}/',
                        'description': 'Faxr tafsilotlari va yutuqlari',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'yangiliklar',
                'title': 'Yangiliklar',
                'description': 'Maktab yangiliklari va e\'lonlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/news/categories/',
                        'description': 'Yangilik kategoriyalari',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/news/',
                        'description': 'Barcha yangiliklar',
                        'params': [
                            {'name': 'category', 'type': 'number', 'required': False},
                            {'name': 'page', 'type': 'number', 'required': False}
                        ]
                    },
                    {
                        'method': 'GET',
                        'path': '/news/{slug}/',
                        'description': 'Yangilik tafsilotlari',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'media',
                'title': 'Media',
                'description': 'Rasm va video to\'plamlar',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/media/collections/',
                        'description': 'Rasm to\'plamlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/media/collections/{slug}/',
                        'description': 'To\'plamdagi barcha rasmlar',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    },
                    {
                        'method': 'GET',
                        'path': '/media/images/',
                        'description': 'Rasmlar, bosh sahifa uchun',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/media/videos/',
                        'description': 'Videolar ro\'yxati',
                        'params': []
                    }
                ]
            },
            {
                'id': 'hujjatlar',
                'title': 'Hujjatlar',
                'description': 'Rasmiy hujjatlar va o\'quv rejalari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/documents/categories/',
                        'description': 'Hujjat kategoriyalari',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/documents/',
                        'description': 'Barcha hujjatlar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/timetables/',
                        'description': 'O\'quv rejalari',
                        'params': []
                    }
                ]
            },
            {
                'id': 'resurslar',
                'title': 'Resurslar',
                'description': 'Ta\'lim resurslari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/resources/videos/',
                        'description': 'Video resurslar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/resources/files/',
                        'description': 'Fayl resurslar',
                        'params': []
                    }
                ]
            },
            {
                'id': 'boshqa',
                'title': 'Boshqa',
                'description': 'Qo\'shimcha ma\'lumotlar',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/faqs/',
                        'description': 'Ko\'p so\'raladigan savollar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/vacancies/',
                        'description': 'Bo\'sh ish o\'rinlari',
                        'params': []
                    }
                ]
            }
        ]
        
        return context