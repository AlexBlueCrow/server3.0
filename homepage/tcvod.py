import time
import random
import hmac
import hashlib
import base64
import json
from wxapp.views import JSONResponse
from .models import TcVideo,Key,Code
from .serializers import TcVideoSerializer
from wxapp.models import Item,FarmUser
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect


def TcVSign(request):
   

    SecretId = Code.objects.get(name = 'tcSecretId').key
    SecretKey = Code.objects.get(name = 'tcSecretKey').key
    
    TimeStamp = int(time.time())
    ExpireTime = TimeStamp + 86400 * 90 * 10
    Random = random.randint(0, 999999)

    Original = "secretId=" + SecretId + "&currentTimeStamp=" + str(TimeStamp) + "&expireTime=" + str(ExpireTime) + "&random=" + str(Random) + "&procedure=" + "standard-1080"
    Hmac = hmac.new(bytes(SecretKey, 'utf-8'), bytes(Original, 'utf-8'), hashlib.sha1)
    Sha1 = Hmac.digest()
    Signature = bytes(Sha1) + bytes(Original, 'utf-8')
    Signature2 = base64.b64encode(Signature)

    #return str(signature2, 'UTF-8')


    return JSONResponse(str(Signature2, 'UTF-8'))

def tcVideo_api(request):
    if request.method == 'GET':
        farmname = request.GET.get('farmname')
        farm_obj = FarmUser.objects.get(name=farmname)
        try:
            videos = TcVideo.objects.all()
            videos_serializer = TcVideoSerializer(videos, many=True)
            return JSONResponse({'code': 20000, 'msg': '请求成功', 'data': videos_serializer.data})
        except:
            return JSONResponse({'code': 20000, 'msg': '无视频', 'data': ''})


@csrf_exempt
def createTcVideo(request):
    
    farmname = request.POST.get('farmname')
    fileid = request.POST.get('fileId')
    video_url = request.POST.get('video_url')
    cover_url = request.POST.get('cover_url')
    video_name = request.POST.get('video_name')
    farm_obj = FarmUser.objects.get(name = farmname)

    try:
        new = TcVideo.objects.create(
            fileid = fileid,
            video_url=video_url,
            video_name = video_name,
            cover_url = cover_url,
            farmuser  = farm_obj,
        )
        return JSONResponse({'code': 20000, 'data': {'msg': '视频登录成功'}, })
    except:
        print('createfailed')
        return JSONResponse({'code': 20000, 'data': {'msg': '视频记录失败',}, })
    
def videolist(request):
    role = request.GET.get('role')
    farmname = request.GET.get('farmname')
    video_list = TcVideo.objects.all()
    serialized = TcVideoSerializer(video_list,many = True)
    print(serialized.data)

    return JSONResponse({'code': 20000, 'data':serialized.data ,'msg':'获取视频列表成功'})

@csrf_exempt
def callback(request):
    print(request.body)
    json_str = request.body
    json_str = json_str.decode()
    json_data = json.loads(json_str)
    print(json_data)
    fielid = json_data['ProcedureStateChangeEvent']['FileId']
    for item in json_data:
        print(item)
    
    newUrl = json_data["ProcedureStateChangeEvent"]['MediaProcessResultSet']["TranscodeTask"]['Output']['Url']
    try:
        tcvideo_obj = TcVideo.objects.get(fileid = fielid)
    except:
        new = TcVideo.objects.create(
            fileid = fielid
        )
        tcvideo_obj = TcVideo.objects.get(fileid = fielid)
    tcvideo_obj.video_url = newUrl
            
    return JSONResponse({'code': 20000,'msg':'success'})




    