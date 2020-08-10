from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class User(models.Model):
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
        if self.user_nickname == '':
            return '未授权:'+self.user_openid[0:3]
        return self.user_nickname


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


class Item(models.Model):
    # id ++
    states = [(0, 'active'), (1, 'inactive'), (2, 'expire')]
    modes = [(0,'all'),(1,'foster'),(2,'selling')]
    name = models.CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey(FarmUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=False, default='')
    main_video = models.CharField(max_length=200)  # video filename
    main_pic = models.CharField(max_length=200)  # pic filename
    description = models.CharField(max_length=600, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    status = models.IntegerField(choices=states, default=0)
    mode = models.IntegerField(choices=modes, default=0)
    stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=15, default='', blank=False)
    effect_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)+self.item_name+'--'+str(self.item_price)+'/'+self.unit

    def deactivate(self):
        self.status = 1

    def expire(self):
        self.status = 2

    def activate(self):
        self.status = 0


class Captain(models.Model):
    genres = [
        (0, '全部'),
        (1, '销售'),
        (2, '配送')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    address = models.CharField(max_length=40)
    phonenumber = models.BigIntegerField(blank=True, default=0)
    name = models.CharField(max_length=20, default='', blank=True)
    active = models.BooleanField(default=False)
    dis_name = models.CharField(max_length=20, default='', blank=True)
    time_of_join = models.DateTimeField(default=timezone.now)
    genre = models.IntegerField(choices=genres, default=0)
    commission_m = models.DecimalField(max_digits=2, decimal_places=2)
    commission_d = models.DecimalField(max_digits=2, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):

    num = models.CharField(primary_key=True, unique=True, max_length=25)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default='')
    price_paid = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    phone_num = models.CharField(max_length=30, default='')
    name_rec = models.CharField(max_length=20, default='', blank=True)
    deliver_address = models.CharField(max_length=50, default='', blank=False)
    effect_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    price_origin = models.DecimalField(
        default=0, max_digits=8, decimal_places=2)
    captain_id = models.IntegerField(blank=True, default=-1)
    num_delivered = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    message = models.CharField(max_length=400)
    genre = models.CharField(max_length=10, choices=[('认领', '认领'), ()])

    def __str__(self):
        return self.user.user_nickname+'--'+str(self.price_paid)+'--'+self.item.item_name+'/'+str(self.captain_id)

    def farm(self):
        return self.item.owner

    def captain(self):
        return Captain.objects.get(id=self.captain_id)


class Prepay_Order(models.Model):
    out_trade_no = models.CharField(primary_key=True, unique=True, max_length=20)
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
    message = models.CharField(max_length=400)

    def __str__(self):
        return str(self.fee)+str(self.varified)+self.out_trade_no


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now)
    user_avatar = models.CharField(
        max_length=150, blank=True, default='')  # 头像地址
    user_nickname = models.CharField(max_length=50, blank=False, default='')
    active = models.BooleanField(default=True)
    genre = models.IntegerField(choices=genres, default=1)

    def __str__(self):
        return self.user_nickname+'-'+self.comment_text
