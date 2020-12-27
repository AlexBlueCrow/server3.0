
import hashlib
import datetime
import xml.etree.ElementTree as ET
from homepage.models import Key
from homepage.tools import getKeys


# key = getKeys()
# appid = key['appid']
# secret = key['secret']
# mch_id = key['mch_id']
# mch_key = key['mch_key']




#生成签名的函数
def paysign(appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee):
    key = getKeys()
    mch_key=key['mch_key']
    ret= {
        "appid": appid,
        "body": body,
        "mch_id":mch_id,
        "nonce_str": nonce_str,
        "notify_url":notify_url,
        "openid":openid,
        "out_trade_no":out_trade_no,
        "spbill_create_ip":spbill_create_ip,
        "total_fee":total_fee,
        "trade_type": 'JSAPI'
    }

    #处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k))for k in sorted(ret)])
    print('stringA:',stringA)
    stringSignTemp = '{0}&key={1}'.format(stringA,mch_key)
    print('Temp:',stringSignTemp)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    print('sign:',sign)
    return sign.upper()


#生成随机字符串
def getNonceStr():
    import random
    data="119911213201911118zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
    nonce_str  = ''.join(random.sample(data , 30))
    return nonce_str

#生成商品订单号
def getWxPayOrdrID():
    date=datetime.datetime.now()
    #根据当前系统时间来生成商品订单号。时间精确到微秒
    payOrdrID=date.strftime("%Y%m%d%H%M%S%f")

    return payOrdrID

#获取全部参数信息，封装成xml
def get_bodyData(openid,client_ip,price):
    key = getKeys()
    body = 'qingjiaofarm_rent'#商品描述
    notify_url = 'https://qingjiao.shop:8000/payOrder/' #支付成功的回调地址  可访问 不带参数
    nonce_str =getNonceStr()#随机字符串
    out_trade_no =getWxPayOrdrID()#商户订单号
    total_fee = int(price) #订单价格 单位是 分
    
   
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
    mch_id = key['mch_id']
    mch_key = key['mch_key']
	#获取签名
    sign=paysign(appid,body,Mch_id,nonce_str,notify_url,openid,out_trade_no,client_ip,total_fee)
    print("sign",sign)

    bodyData = '<xml>'
    bodyData += '<appid>' + appid + '</appid>'             # 小程序ID
    bodyData += '<body>' + body + '</body>'                         #商品描述
    bodyData += '<mch_id>' + Mch_id + '</mch_id>'          #商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'         #随机字符串
    bodyData += '<notify_url>' + notify_url + '</notify_url>'      #支付成功的回调地址
    bodyData += '<openid>' + openid + '</openid>'                   #用户标识
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'#商户订单号
    bodyData += '<spbill_create_ip>' + client_ip + '</spbill_create_ip>'#客户端终端IP
    bodyData += '<total_fee type="int">'+ str(total_fee) +'</total_fee>'         #总金额 单位为分
    bodyData += '<trade_type>'+'JSAPI'+'</trade_type>'                   #交易类型 小程序取值如下：JSAPI
    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'

    return bodyData


def xml_to_dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict


def dict_to_xml(dict_data):
    '''
    dict to xml
    :param dict_data:
    :return:
    '''
    xml = ["<xml>"]
    for k, v in dict_data.iteritems():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


#获取返回给小程序的paySign
def get_paysign(prepay_id,timeStamp,nonceStr):
    key = getKeys()
    mch_key=key['mch_key']
    pay_data={
                'appId': appid,
                'nonceStr': nonceStr,
                'package': "prepay_id="+prepay_id,
                'signType': 'MD5',
                'timeStamp':timeStamp
    }
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA,mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()
