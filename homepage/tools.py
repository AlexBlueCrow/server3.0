from .models import Key
from .serializers import KeySerializer
import json
import requests

def getKeys():
    key = Key.objects.get(account='qj')
    key_ser = KeySerializer(key,many=False)
    return key_ser.data
 
def getAccToken(code):
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    AccTokUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + \
        appid+'&secret='+secret
    accToken = json.loads(requests.get(AccTokUrl).content)['access_token']
    return accToken

def tryprint(content):
    on = False
    if on:
        try:
            print(content)
            return
        except:
            return
    else:
        return

