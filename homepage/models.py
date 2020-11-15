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
      return str(self.id)+'.'+self.username

class Role(models.Model):
    name = models.CharField(max_length = 32)


class Permission(models.Model):
    name = models.CharField(max_length = 32)
    url = models.CharField(max_length = 128)

class Action(models.Model):
    name = models.CharField(max_length = 32)
    code = models.CharField(max_length = 32)

class Menu(models.Model):
    title = models.CharField(max_length =32)
    parent = models.ForeignKey('self',blank=True,on_delete=models.CASCADE)


class Permission2Action(models.Model):
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE)
    action = models.ForeignKey(Action,on_delete=models.CASCADE)
    parent = models.ForeignKey(Menu,on_delete=models.CASCADE)

class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)


class TcVideo(models.Model):
    fileid = models.CharField(max_length=32,unique =True, primary_key=True)
    video_name = models.CharField(max_length = 32)
    video_url = models.CharField(max_length = 256)
    cover_url = models.CharField(max_length = 256)
    farmuser = models.ForeignKey(FarmUser,on_delete=models.CASCADE)
    time_created = models.DateTimeField(default= timezone.now)
    def __str__(self):
        return self.video_name+'.'+self.farmuser.name


    

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

class tcVideo2Item(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    video = models.ForeignKey(TcVideo,on_delete=models.CASCADE)
    

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

class Code(models.Model):
    name = models.CharField(max_length = 48)
    key = models.CharField(max_length = 256)
        

