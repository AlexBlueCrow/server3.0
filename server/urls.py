
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from homepage import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'zxserver/',include('wxapp.urls')),
    url(r'api/',include(api_urls)), 
]
