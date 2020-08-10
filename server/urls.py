
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'server/',include('server.urls')),
    url(r'homepage/',include('homepage.urls')),

]
