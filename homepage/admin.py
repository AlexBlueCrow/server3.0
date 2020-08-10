from django.contrib  import admin
from .models import AdminUser,VideoFiles,PicFiles,VIMap,Key
# Register your models here.

admin.site.register([AdminUser,VideoFiles,PicFiles,VIMap,Key])
