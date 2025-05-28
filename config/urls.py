from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path, include

from config.swagger.schema import swagger_urlpatterns


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]   

urlpatterns += [
    path('api/', include('apps.main.urls')),
    path('api/', include('apps.common.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/lang-check/', lambda request: JsonResponse({
        "HTTP_ACCEPT_LANGUAGE": request.META.get("HTTP_ACCEPT_LANGUAGE"),
        "django_language":     request.LANGUAGE_CODE,
    }), name='lang-check'),
]

urlpatterns += swagger_urlpatterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)