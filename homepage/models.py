from django.db import models
from server.settings import MEDIA_ROOT
from wxapp.models import Item,FarmUser
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class AdminUser(AbstractUser):
    phonenumber = models.BigIntegerField(blank=True,default=0,unique=True)
    farm = models.CharField(max_length=30,default='',blank=True)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=20,default='farmuser')
    active = models.BooleanField(default=False)
    def __str__(self):
      return self.id+'.'+self.username

class Account(models.Model):
    owner = models.ForeignKey(AdminUser,on_delete=models.CASCADE)
    num = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    extractable = models.DecimalField(default=0,max_digits=8,decimal_places=2)

class Transact(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    time = models.DateTimeField(default= timezone.now)
    amount = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    genre = models.IntegerField(choices=[(-1,'disburse'),(1,'income')])
    desc = models.CharField(max_length = 200)


class VideoFiles(models.Model):
    name = models.CharField(max_length = 50 , default = '',blank = True)
    farmid = models.CharField(max_length = 50,default = '',unique = False )
    video = models.FileField(upload_to = 'statics/video/',unique = True )
    cover = models.FileField(upload_to='statics/cover/',unique = False, blank= True)
    def __str__(self):
        return str(self.id)+'/'+self.name


class PicFiles(models.Model):
    name = models.CharField(max_length = 50,default = '',blank = True)
    itemname = models.CharField(max_length = 50,default = '',unique = False,blank = True)
    farmid = models.CharField(max_length = 50,default = '',unique = False )
    pic = models.FileField(upload_to = 'statics/pic/', unique = True )

    def __str__(self):
        return str(self.id)+self.itemname

class VIMap(models.Model):
    name = models.CharField(max_length = 50,default='')
    farm = models.ForeignKey(FarmUser, on_delete = models.CASCADE)
    item_id = models.IntegerField(blank=False,default=-1)
    video_id = models.IntegerField(blank=False,default=-1)


    def __str__(self):
        return self.name



class Key(models.Model):
    account = models.CharField(max_length = 50,default='')
    appid = models.CharField(max_length = 50,default='')
    secret = models.CharField(max_length = 50,default='')
    mch_id = models.CharField(max_length = 50,default='')
    mch_key = models.CharField(max_length = 50,default='')

        

