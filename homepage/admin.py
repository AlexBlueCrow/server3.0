from django.contrib  import admin
from .models import StaticFiles,AdminUser,VideoFiles,PicFiles,VIMap,Key
# Register your models here.

admin.site.register([StaticFiles,AdminUser,VideoFiles,PicFiles,VIMap,Key])
