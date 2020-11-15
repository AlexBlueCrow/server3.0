from django.contrib  import admin
from .models import AdminUser,VideoFiles,PicFiles,VIMap,Key,TcVideo,tcVideo2Item,Code
# Register your models here.

admin.site.register([AdminUser,VideoFiles,PicFiles,VIMap,Key,TcVideo,tcVideo2Item,Code])
