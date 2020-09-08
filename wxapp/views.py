from rest_framework.response import Response
import hashlib
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import AppUser, Item, Order, Comments, Prepay_Order, Varify_failed, Captain, FarmUser,Text
from .serializers import AppUserSerializer, ItemSerializer, OrderSerializer, CommentsSerializer, Prepay_OrderSerializer, CaptainSerializer, FarmUserSerializer,TextSerializer
from homepage.models import Key, VideoFiles, PicFiles, VIMap
from homepage.serializers import VIMapSerializer
import random
import time
import xml.etree.ElementTree as ET
from wxapp import pay
from rest_framework.decorators import api_view, authentication_classes
from wechatpy.utils import check_signature
from wechatpy.pay.api import WeChatOrder
from wechatpy.pay import WeChatPay
from json import dumps
from math import radians, cos, sin, asin, sqrt
import random
import string
import json
from homepage.tools import getKeys
from django.db.models import Min

# Create your views here.


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def wxlogin(code):
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' + 'appid=' + \
        appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return HttpResponse(res['errcode'])
    openid = res['openid']
    user = AppUser.objects.get_or_create(
        openid=openid,
    )
    user = AppUser.objects.get(openid=openid)
    return user


def get_farms(request):
    farmuser = FarmUser.objects.all()
    farmuser_serializer = FarmUserSerializer(farmuser, many=True)
    return JSONResponse(farmuser_serializer.data)


def get_item(request):
    items = Item.objects.filter(status=1)
    items_serializer = ItemSerializer(items, many=True)
    # Rearrange by distance
    try:
        userlon = float(request.GET.get('lon'))
        userlat = float(request.GET.get('lat'))
    except:
        userlon = 120
        userlat = 30
    Locdic = getFarmLocs()
    for item in items_serializer.data:
        farmid = item['owner']
        for Loc in Locdic:
            if Loc['id'] == farmid:
                farmLon = Loc['loc']['lon']
                farmLat = Loc['loc']['lat']
                break
        item['dis'] = round(getDistance(userlon, userlat, farmLon, farmLat), 2)
    sorteddata = sorted(items_serializer.data, key=lambda x: x['dis'])
    for item in sorteddata:
        item['ex_videos'] = []
        links = VIMap.objects.filter(item_id=item['id'])
        for link in links:
            video = VideoFiles.objects.get(id=link.video_id)
            video_file_name = str(video.video).split("/")[-1]
            cover_file_name = str(video.cover).split("/")[-1]
            item['ex_videos'].append(
                {'video': video_file_name, 'cover': cover_file_name, 'name': video.name})

    return JSONResponse(sorteddata)


def getFarmLocs():
    farms = FarmUser.objects.all()
    dic = []
    for farm in farms:
        LocInfo = {'id': farm.id, 'loc': {
            "lon": farm.longitude, "lat": farm.latitude}}
        dic.append(LocInfo)
    return dic


def getCaptainLocs():
    captains = Captain.objects.filter(active=True)
    dic = []
    for cap in captains:
        Locinfo = {'id': cap.id, 'name': cap.name,
                   'loc': {'lon': cap.longitude, 'lat': cap.latitude}}
        dic.append(Locinfo)
    return dic


def getDistance(userLon, userLat, farmLon, farmLat):
    ##
    lon1, lat1, lon2, lat2 = map(radians, [userLon, userLat, farmLon, farmLat])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    s = c*r
    return s


def get_orderInfo(request):
    code = request.GET.get('code')
    user = wxlogin(code)
    try:
        orders = Order.objects.filter(user=user)
        orders_serializer = OrderSerializer(orders, many=True)

        for order in orders_serializer.data:
            item = Item.objects.get(id=order['item'])
            order['item_name'] = item.name
            order['effect_time'] = order['effect_time'][0:10]
            order['image'] = item.pic_address

        return JSONResponse(orders_serializer.data)
    except:
        return HttpResponse("无有效订单")


def get_farmInfo(request):
    id = request.GET.get('farm')
    farm = FarmUser.objects.filter(id=id)
    farm_serializer = FarmUserSerializer(farm, many=True)
    return JSONResponse(farm_serializer.data)


def get_userInfo(request):
    code = request.GET.get('code')
    user = wxlogin(code)
    user_serializer = AppUserSerializer(user, many=False)
    return JSONResponse(AppUser_serializer.data)


# '''def get_questions(request):
#     category=request.GET.get('cate')
#     try:
#         questions = Question.objects.filter(question_category=category)
#     except Question.DoesNotExist:
#         return HttpResponseNotFound
#     questions_serializer = QuestionSerializer(questions,many=True)
#     return JSONResponse(questions_serializer.data)
# '''


def get_comments(request):
    item_id = request.GET.get('item_id')
    comments = Comments.objects.filter(item_id=item_id, active=True)
    if comments:
        comments_serializer = CommentsSerializer(comments, many=True)
    else:
        return HttpResponse([])
    return JSONResponse(comments_serializer.data)


@api_view(['GET'])
@authentication_classes([])
def comment_post(request):
    code = request.GET.get('code')
    comment_text = request.GET.get('comment')
    item_id = request.GET.get('item_id')
    nickname = request.GET.get('nickname')
    avatarUrl = request.GET.get('avatarUrl')

    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    AccTokUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + \
        appid+'&secret='+secret
    accToken = json.loads(requests.get(AccTokUrl).content)['access_token']
    SensCheckUrl = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token='+accToken
    data = {"content": comment_text}

    # data_json = json.dumps(data,ensure_ascii=True)
    # data = json.loads(data_json,encoding='utf-8')
    r = json.loads(requests.post(
        SensCheckUrl, data=json.dumps(data, ensure_ascii=False).encode()).content)

    if r['errcode'] == 87014:
        return JSONResponse({'code': 'sensitive'})
    user = wxlogin(code)
    avatarUrl = user.avatar
    nickname = user.nickname
    if comment_text:
        created = Comments.objects.create(
            user=user,
            comment_text=comment_text,
            item_id=item_id,
            user_avatar=avatarUrl,
            user_nickname=nickname,
        )
        created.save()
    return Response(data={'code': 'success', 'msg': 'ok'})


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
def payOrder(request):
    import time
    JSCODE = ''
    if request.method == 'GET':
        item_price = request.GET.get('item_price')
        num_buy = int(request.GET.get('num_buy'))
        reward = request.GET.get('reward')
        price = request.GET.get('total_fee')

        # 获取客户端ip
        client_ip, port = request.get_host().split(":")
        # 获取小程序openid
        JSCODE = request.GET.get('code')
        ''' ####print('JSCODE',JSCODE)
        appid= 'wx5aff52c0a3a0f7ac'
        secret='3c6eb61f23aeff10038a74ff10aedd11'
        wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
        res = json.loads(requests.get(wxLoginURL).content)
        if 'errcode' in res:
            return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
        openid=res['openid']
        ##print('openid',openid)
        '''
        user = wxlogin(JSCODE)
        openid = user.openid

        # 请求微信的url
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

        # 拿到封装好的xml数据
        # print('bodtdata_input:',openid,'ip',client_ip,'price:',price)
        body_data = pay.get_bodyData(openid, client_ip, price)
        # print('body_data',body_data)

        # 获取时间戳
        timeStamp = str(int(time.time()))
        # print('timeStamp',timeStamp)

        # 请求微信接口下单
        respone = requests.post(url, body_data.encode(
            "utf-8"), headers={'Content-Type': 'application/xml'})

        # 回复数据为xml,将其转为字典
        content = pay.xml_to_dict(respone.content)

        # print("content:",content)

        if content["return_code"] == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content.get("prepay_id")
            # 获取随机字符串
            nonceStr = content.get("nonce_str")

            # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr)

            # print("paysign",paySign)

            # 封装返回给前端的数据
            data = {"prepay_id": prepay_id, "nonceStr": nonceStr,
                    "paySign": paySign, "timeStamp": timeStamp}

            return HttpResponse(packaging_list(data))

        else:
            # print('支付失败')
            return HttpResponse("请求支付失败")


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
def weChatPay(request):
    ##
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    mch_id = key['mch_id']
    mch_key = key['mch_key']

    code = request.GET.get('code')
    genre = request.GET.get('genre')
    item_id = request.GET.get('item_id')
    item_name = request.GET.get('item_name')
    item_price = request.GET.get('item_price')
    num_buy = int(request.GET.get('num_buy'))
    reward = request.GET.get('reward')

    nickname = request.GET.get('nickname')
    post_sign = request.GET.get('post_sign')

    price = int(float(request.GET.get('total_fee'))*100)
    address = request.GET.get('addRegion')+request.GET.get('addDetail')
    name_rec = request.GET.get('name_rec')
    phone_num = request.GET.get('phone_num')
    captain_id = request.GET.get('captain_id')
    del_time = request.GET.get('del_time')
    # success
    user = wxlogin(code)
    openid = user.openid

    NOTIFY_URL = 'https://qingjiao.shop:8000/server/pay_feedback'
    wepy_order = WeChatPay(appid=appid, sub_appid=appid,
                           api_key=mch_key, mch_id=mch_id)
    out_trade_no = pay.getWxPayOrdrID()
    pay_res = wepy_order.order.create(
        trade_type="JSAPI",
        body=item_name,
        total_fee=price,
        notify_url=NOTIFY_URL,
        user_id=openid,
        out_trade_no=out_trade_no,
    )

    # print("------pay_res",pay_res)
    prepay_id = pay_res.get("prepay_id")
    wepy_sign = wepy_order.order.get_appapi_params(prepay_id=prepay_id)
    # print('------wepy_sign:',wepy_sign)

    timeStamp = str(int(time.time()))
    nonceStr = pay_res['nonce_str']

    paySign = pay.get_paysign(
        prepay_id=prepay_id, timeStamp=timeStamp, nonceStr=nonceStr)
    prepay_order = Prepay_Order.objects.create(
        out_trade_no=out_trade_no,
        sign=paySign,
        noncestr=nonceStr,
        openid=openid,
        fee=int(price)/100,  # cents
        deliver_address=address,
        quantity=num_buy,
        item_id=int(item_id),
        phone_num=str(phone_num),
        name_rec=name_rec,
        captain_id=captain_id,

        nickname=nickname,
        post_sign=post_sign,
        genre=genre
    )

    user.current_captain_id = captain_id
    user.save()

    return Response(data={'wepy_sign': wepy_sign, 'status': 100, 'paySign': paySign, 'timeStamp': timeStamp, 'nonceStr': nonceStr})


@csrf_exempt
def pay_feedback(request):
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    mch_id = key['mch_id']
    mch_key = key['mch_key']

    xml = request.body.decode('utf-8')
    wepy_order = WeChatPay(appid=appid, sub_appid=appid,
                           api_key=mch_key, mch_id=mch_id)
    result = wepy_order.parse_payment_result(xml)

    prepay = Prepay_Order.objects.get(out_trade_no=result['out_trade_no'])
    prepay_serializer = Prepay_OrderSerializer(prepay, many=False)
    # print('prepay_serializer',prepay_serializer.data)
    if prepay_serializer.data['varified'] == True:
        # print('varified==True')
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')

    # print('fee,',float(prepay_serializer.data['fee']),float(result['total_fee']))
    if (float(prepay_serializer.data['fee'])*100 == float(result['total_fee'])):
        # print('sign=sign&fee=fee')
        item = Item.objects.get(id=prepay_serializer.data['item_id'])
        user = AppUser.objects.get(openid=prepay_serializer.data['openid'])
        item_serializer = ItemSerializer(item, many=False)
        try:
            cap = Captain.objects.get(id=prepay_serializer.data['captain_id'])
        except:
            cap = Captain.objects.all().aggregate(Min('id'))
        try:
            new_order = Order.objects.create(
                num=str(prepay_serializer.data['out_trade_no']),
                item=item,
                farm_name=item.owner.name,
                user=user,
                deliver_address=prepay_serializer.data['deliver_address'],
                price_paid=prepay_serializer.data['fee'],
                quantity=prepay_serializer.data['quantity'],
                imageUrl=item_serializer.data['pic_address'],
                phone_num=str(prepay_serializer.data['phone_num']),
                name_rec=prepay_serializer.data['name_rec'],
                captain_id=prepay_serializer.data['captain_id'],
                cap=cap,
                genre=prepay.genre,
                nickname=prepay.nickname,
                post_sign=prepay.post_sign,
            )
            comment = Comments.objects.create(
                user=user,
                comment_text='我刚刚买了'+item.item_name+'!',
                item_id=item.item_id,
                user_avatar=user.avatar,
                user_nickname=user.nickname,
                genre=2,
            )

        #print('order created:',new_order)
            prepay.varified = True
            prepay.save()
        #print('prepay varified')
        except:
            pass
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    else:
        failed = Varify_failed.objects.create(
            fee=prepay_serializer.data['fee'],
            out_trade_no=prepay_serializer.data['out_trade_no'],
        )
        return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[金额错误]]></return_msg></xml>')

    # print("Pay_success",request)


def allorder(request):
    orders = Order.objects.all()
    orders_serializer = OrderSerializer(orders, many=True)
    for order in orders:
        print('商品名称', order.item.item_name, '收件姓名', order.name_rec,)
    return JSONResponse(orders_serializer)


def updateUser(request):

    code = request.GET.get('code')
    nickname = request.GET.get('nickname')
    avatarUrl = request.GET.get('avatarUrl')
    user = wxlogin(code=code)
    user.nickname = nickname
    user.avatar = avatarUrl
    user.save()

    return JSONResponse(user.current_captain_id)


def getCaptains(request):
    userlon = float(request.GET.get('lon'))
    userlat = float(request.GET.get('lat'))
    captains = Captain.objects.filter(active=True)
    captains_serializer = CaptainSerializer(captains, many=True)
    caps_data = []
    for cap in captains:
        item = {}
        item['id'] = cap.id
        item['nickname'] = cap.user.nickname
        item['avatarUrl'] = cap.user.avatar
        caps_data.append(item)
        # Rearrange by distance
    Locdic = getCaptainLocs()
    for index, cap in enumerate(captains_serializer.data):
        cap['dis'] = round(getDistance(userlon, userlat, float(
            cap['longitude']), float(cap['latitude'])), 2)
        cap['nickname'] = caps_data[index]['nickname']
        cap['avatarUrl'] = caps_data[index]['avatarUrl']
    sorteddata = sorted(captains_serializer.data, key=lambda x: x['dis'])
    return JSONResponse(sorteddata)

def get_text(request):
    text = Text.objects.all()
    
    return JSONResponse(TextSerializer(text,many=True).data)
 


def cap_apply(request):
    code = request.GET.get('code')
    name = request.GET.get('name')
    number = request.GET.get('number')
    address = request.GET.get('address')
    longitude = request.GET.get('lng')
    latitude = request.GET.get('lat')
    dis_name = request.GET.get('disName')
    deliver = request.GET.get('deliver')=='true'
    marketing = request.GET.get('marketing')=='true'
    user = wxlogin(code)
    newcap = Captain.objects.create(
        user=user,
        longitude=longitude,
        latitude=latitude,
        address=address,
        phonenumber=number,
        name=name,
        dis_name=dis_name,
        active=False,
        deliver=deliver,
        marketing=marketing
    )
    user.current_captain_id = newcap.id
    user.save()
    return HttpResponse('success')
    # except:
    #     return HttpResponse('fail')


def is_captain(request):
    code = request.GET.get('code')
    user = wxlogin(code)

    try:
        captain = Captain.objects.get(user=user)
        user.current_captain_id = captain.captain_id
        user.save()
        return JSONResponse({'is_captain': True, 'status': captain.active, 'id': captain.captain_id})
    except:
        return JSONResponse({'is_captain': False, 'current_cap': user.current_captain_id})

    
# 用小程序用户code换取openid，返回用户实例


# def get_questions():


# def data_response():

# def get_user(request):
