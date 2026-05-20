from django.contrib import admin
from django.urls import path, include
from shortener.urls import redirect_urlpatterns
from django.http import JsonResponse



def api_root(request):
    return JsonResponse({
        "message": "URL Shortener API is running.",
        "endpoints": {
            "shorten": "/api/shorten/",
            "retrieve": "/api/urls/<short_code>/",
            "redirect": "/<short_code>/"
        }
    })

urlpatterns = [

    # Django admin panel
    path('admin/', admin.site.urls),

    path('', api_root, name='api-root'),

    # All API routes — prefixed with /api/
    path('api/', include('shortener.urls', namespace='shortener')),

    # Redirect route — sits at root level, e.g. /abc123/
    *redirect_urlpatterns,

]