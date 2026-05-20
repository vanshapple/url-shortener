from django.urls import path
from .views import ShortenURLView, URLRetrieveView, RedirectToOriginalView

app_name = 'shortener'

urlpatterns = [

    # POST /api/shorten/
    path(
        'shorten/',
        ShortenURLView.as_view(),
        name='shorten-url'
    ),

    # GET /api/urls/<short_code>/
    path(
        'urls/<str:short_code>/',
        URLRetrieveView.as_view(),
        name='retrieve-url'
    ),

]

# Redirect route — defined separately (used at project level, not under /api/)
redirect_urlpatterns = [

    # GET /<short_code>/
    path(
        '<str:short_code>/',
        RedirectToOriginalView.as_view(),
        name='redirect-url'
    ),

]