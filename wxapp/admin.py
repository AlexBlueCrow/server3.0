from django.contrib import admin
from .models import User,Item,Order,Comments,Prepay_Order,Varify_failed,Captain,CapManager,FarmUser
# Register your models here.

admin.site.register([User,Item,Order,Comments,Prepay_Order,Varify_failed,Captain,CapManager,FarmUser])

