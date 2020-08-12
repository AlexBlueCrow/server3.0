from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views,login
from django.views.static import serve
from server.settings  import MEDIA_ROOT

urlpatterns = [
    url(r'order_inquire/$',views.order),
    
]

