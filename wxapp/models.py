from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your models here.


class AppUser(models.Model):
    openid = models.CharField(
        max_length=50, blank=False, default='', unique=True)
    gender = models.CharField(max_length=10, choices=[(
        'female', 'female'), ('male', 'male'), ('null', 'null')], default='null')
    avatar = models.CharField(max_length=150, blank=True, default='')  # 头像地址
    nickname = models.CharField(max_length=50, blank=False, default='')
    address = models.CharField(max_length=100, blank=True, default='')
    phonenumber = models.BigIntegerField(blank=True, default=0)
    addressee = models.CharField(max_length=50, blank=False, default='')
    membership = models.IntegerField(default=0)
    region = models.CharField(max_length=50, default='')
    current_captain_id = models.IntegerField(blank=True, default=-1)

    def __str__(self):
        if self.nickname == '':
            return '未授权:'+self.openid[0:3]
        return self.nickname


class FarmUser(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    logo = models.CharField(max_length=100)
    phonenumber = models.BigIntegerField(blank=True, default=0)
    contact = models.CharField(max_length=20)
    rank = models.IntegerField(default=0)
    short = models.CharField(max_length=20, default='', blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    def __str__(self):
        return self.name


class Item(models.Model):
    # id ++
    states = [(0, 'inactive'), (1, 'active'), (2, 'expire')]
    modes = [(0, 'all'), (1, 'foster'), (2, 'selling')]
    name = models.CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey(FarmUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=False, default='')
    video_address = models.CharField(max_length=200)  # video filename
    pic_address = models.CharField(max_length=200)  # pic filename
    description = models.CharField(max_length=600, blank=True)
    status = models.IntegerField(choices=states, default=0)
    mode = models.IntegerField(choices=modes, default=0)
    effect_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)+'.'+self.name


class Sell(models.Model):
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, related_name='Sell')
    price = price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=15, default='', blank=False)

    def __str__(self):
        return 'selling info of %s' % self.item.name


class Adopt(models.Model):
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, related_name='Adopt')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    guaranteed = models.FloatField(default=0)
    benefit = models.CharField(max_length=200,default='')
    period = models.IntegerField(blank=True, default=1)
    unit = models.CharField(max_length=5, default='', blank=False)

    def __str__(self):
        return 'adopting info of %s' % self.item.name


class Captain(models.Model):
  
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    address = models.CharField(max_length=40)
    phonenumber = models.BigIntegerField(blank=False, default=0)
    name = models.CharField(max_length=20, default='', blank=True)
    active = models.BooleanField(default=False)
    dis_name = models.CharField(max_length=20, default='', blank=True)
    time_of_join = models.DateTimeField(default=timezone.now)
    
    deliver = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
    commission_m = models.DecimalField(
        max_digits=2, decimal_places=2, default=0)
    commission_d = models.DecimalField(
        max_digits=2, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)+self.name+'/'+self.dis_name


class Order(models.Model):
    
    num = models.CharField(primary_key=True, unique=True, max_length=25)
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT, default='')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True)
    farm_name = models.CharField(max_length=30, default='', blank=True)
    price_paid = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    phone_num = models.CharField(max_length=30, default='')
    name_rec = models.CharField(max_length=20, default='', blank=True)
    deliver_address = models.CharField(max_length=50, default='', blank=False)
    imageUrl = models.CharField(max_length=50, default='', blank=True,null=True)
    effect_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    captain_id = models.IntegerField(blank=True, default=-1)
    num_delivered = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    message = models.CharField(max_length=400,null=True,blank=True)
    genre = models.CharField(max_length=10, choices=[
                             ('adopt', 'adopt'), ('sell', 'sell')])
    nickname = models.CharField(max_length=20, default='',null=True,blank=True)
    post_sign = models.CharField(max_length=40, default='',null=True,blank=True)
    cap = models.ForeignKey(Captain,on_delete=models.PROTECT,default='',null=True)
    def __str__(self):
        return self.user.nickname+'--'+str(self.price_paid)+'--'+self.item.name+'--'+str(self.captain_id)

    def farm(self):
        return self.item.owner



class Prepay_Order(models.Model):
    out_trade_no = models.CharField(
        primary_key=True, unique=True, max_length=20)
    sign = models.CharField(max_length=50)
    noncestr = models.CharField(max_length=50)
    openid = models.CharField(max_length=40)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    item_id = models.IntegerField(blank=False)
    deliver_address = models.CharField(max_length=50, default='', blank=False)
    quantity = models.IntegerField(default=1)
    varified = models.BooleanField(default=False)
    phone_num = models.CharField(max_length=30, default='')
    name_rec = models.CharField(max_length=20, default='', blank=True)
    captain_id = models.IntegerField(blank=True, default=-1)
    
    message = models.CharField(max_length=400,null=True)
    nickname = models.CharField(max_length=20, default='',null=True)
    post_sign = models.CharField(max_length=40, default='',null=True)
    genre = models.CharField(max_length=10, choices=[
        ('adopt', 'adopt'), ('sell', 'sell')],default='sell')

    def __str__(self):
        return self.name_rec+'----'+str(self.fee)


class Varify_failed(models.Model):
    out_trade_no = models.CharField(
        primary_key=True, unique=True, max_length=20)
    sign = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.out_trade_no+'--'+str(self.fee)


class Comments(models.Model):
    genres = [(1, 'comments'), (2, 'purches')]

    comment_id = models.AutoField(primary_key=True)
    item_id = models.IntegerField(default=0)
    comment_text = models.CharField(max_length=100)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now)
    user_avatar = models.CharField(
        max_length=150, blank=True, default='')  # 头像地址
    user_nickname = models.CharField(max_length=50, blank=False, default='')
    active = models.BooleanField(default=True)
    genre = models.IntegerField(choices=genres, default=1)

    def __str__(self):
        return self.user_nickname+'-'+self.comment_text

class Text(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.title