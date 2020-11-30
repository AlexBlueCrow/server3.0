from django.shortcuts import render
from wxapp.models import Order, Item, Captain, User, Order, Comments, FarmUser, User, Sell, Adopt
from wxapp.serializers import OrderSerializer, ItemSerializer, FarmUserSerializer
from django.http import HttpResponse, HttpResponseNotFound
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
from server.settings import MEDIA_ROOT, MEDIA_URL
from .models import AdminUser, VideoFiles, PicFiles, VIMap, Key,TcVideo,tcVideo2Item,Transact,Account,CashingRequest,PlatformAccount
import jwt
from rest_framework_jwt.settings import api_settings
import csv as csvreader
from rest_framework.authtoken.models import Token
from wxapp.views import JSONResponse
from .serializers import AdminUserSerializer, VideoFilesSerializer, PicFilesSerializer, VIMapSerializer, KeySerializer,AccountSerializer,TransactSerializer,CashingRequestSerializer,PlatformAccountSerializer
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, authentication_classes
import decimal
# from .financetools import creCasReq,comCasReq
# Create your views here.

def creCasReq(user,amount,msg):
    account = Account.objects.get(owner = user)##

    if account.extractable < amount:
        
        return False
    else:
        try:
            new_req = CashingRequest.objects.create(
                account=account,
                amount = amount,
                msg = msg,
                status = 0,
            )
           
            account.extractable -=amount
            account.save()
            return new_req
        except:
            
            return False

def comCasReq(casReq):
    account = casReq.account
    trans = Transact.objects.create(
        account = account,
        amount = casReq.amount,
        genre = -1,
    )
    trans.save()
    account.amount = account.amount-trans.amount
    account.save()
    return

def createTrans(account,msg,amount,genre):
    trans =  Transact.objects.create(
        account = account,
        amount = amount,
        genre = -1,
        msg= msg
    )
    trans.save()
    account.amount = account.amount-trans.amount
    account.save()
    return 
    
def refuseReq(casReq):
    account = casReq.account
    account.amount = account.extractable+trans.amount
    account.save()

@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
def financeInfo(request):
    
    username = request.GET.get('username')
    user_obj = AdminUser.objects.get(username = username)
    account_obj = Account.objects.get(owner = user_obj)
    acc_data = AccountSerializer(account_obj,many = False).data
    transactions = Transact.objects.filter(account=account_obj)
    trans_data = TransactSerializer(transactions,many=True).data
    return JSONResponse({'code': 20000, 'data':{'accountInfo':acc_data,'transInfo':trans_data} ,'msg':'获取列表成功'})

@csrf_exempt
def cashingRequest_API(request):
    
    if request.method=='GET':
        username = request.GET.get('username')
        user = AdminUser.objects.get(username=username)
        
        if user.role == 'farmuser':
            account = Account.objects.get(owner = user)
            acc_data = AccountSerializer(account ,many = False).data
            cashings = CashingRequest.objects.filter(account = account)
            cas_ser = CashingRequestSerializer(cashings,many = True).data
            return JSONResponse({'code': 20000, 'data':{ 'accountInfo':acc_data, 'reqInfo':cas_ser } ,'msg':'获取列表成功'})
        elif user.role == 'manager':
            account = Account.objects.get(owner = user)
            acc_data = AccountSerializer(account ,many = False).data
            cas_req = CashingRequest.objects.filter(status__in = [0,1,2] )
            cas_req_data = CashingRequestSerializer(cas_req,many=True).data
            cas_done = CashingRequest.objects.filter(status__in = [3,4] )
            cas_done_data = CashingRequestSerializer(cas_done,many=True).data
            return JSONResponse({'code': 20000, 'data':{ 'accountInfo':acc_data, 'reqInfo':cas_req_data ,'reqDone': cas_done_data } ,'msg':'获取列表成功'})


    if request.method=='POST':
        username = request.POST.get('username')
        amount = decimal.Decimal(request.POST.get('amount'))
        
        msg = request.POST.get('msg')
        
        user = AdminUser.objects.get(username=username)
        account = Account.objects.get(owner = user)
        new_req = creCasReq(user,amount,msg)
        

        if new_req:
            new_req_ser = CashingRequestSerializer(new_req,many=False).data
            return JSONResponse({'code': 20000, 'data':{'reqInfo':new_req_ser } ,'msg':'success'})
        else:
            return JSONResponse({'code': 20000, 'data':{ } ,'msg':'fail'})
    
 
@csrf_exempt
def casReqUpdate(request):
    reqId = request.POST.get('reqId')
    new_status = request.POST.get('newstatus')
    
    req_obj = CashingRequest.objects.get(id = reqId)
   
    if new_status =='3':
        comCasReq(req_obj)  
    if new_status =='4':
        refuseReq(req_obj)
    req_obj.status = int(new_status)
    req_obj.save()
    return JSONResponse({'code': 20000, 'data':{'new_status':new_status } ,'msg':'success'})


@csrf_exempt
def summary(request):
    account = PlatformAccount.objects.get()
    Acc_data = PlatformAccountSerializer(account,many = False).data
    req_todo = CashingRequest.objects.filter(status__in =[1,2,3]).count()

    latest = Transact.objects.filter(account = account,genre=1).order_by('-time')[:30]
    lat_data = TransactSerializer(latest,many=True).data

    return JSONResponse({'code': 20000, 'data':{'AccountInfo':Acc_data, 'todo':str(req_todo), 'latest':lat_data } ,'msg':'success'})




        

@csrf_exempt
def expense(request):
    placcount = PlatformAccount.objects.get()

    if request.method=='POST':
        msg  = request.POST.get('msg')
        amount = decimal.Decimal(request.POST.get('amount'))
        new = Transact.objects.create(
            account = placcount,
            msg = msg,
            amount = amount,
            genre = -1,
        )
        new.save()
        placcount.amount -= amount
        placcount.save()
        
        return JSONResponse({'code': 20000, 'data':{ } ,'msg':'success'})
    
    
    
    