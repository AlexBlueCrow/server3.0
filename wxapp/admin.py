from django.contrib import admin
from .models import AppUser,Item,Order,Comments,Prepay_Order,Varify_failed,Captain,FarmUser,Sell,Adopt,Text,ItemShadow,Question
# Register your models here.

admin.site.register([AppUser,Item,Order,Comments,Prepay_Order,Varify_failed,Captain,FarmUser,Sell,Adopt,Text,ItemShadow,Question])

