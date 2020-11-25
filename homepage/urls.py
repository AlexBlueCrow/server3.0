from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views,login,tcvod,finance
from django.views.static import serve
from server.settings  import MEDIA_ROOT

urlpatterns = [
    url(r'order_inquire/$',views.order),
    url(r'Item/$',views.Item_API),
    url(r'csrf_token/',views.get_csrf_token),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    url(r'login/$',login.login),
    url(r'register',login.register),
    url(r'csv/',views.csv),
    url(r'getUserInfo/',login.userInfo),
    url(r'farm/',views.Farm_API),
    url(r'Item_update',views.Item_update),
    url(r'video/',views.video_api),
    url(r'VIMap/',views.VIMap_update),
    url(r'tcvsign/',tcvod.TcVSign),
    url(r'createTcVideo',tcvod.createTcVideo),
    url(r'tcVideo',tcvod.tcVideo_api),
    url(r'callback',tcvod.callback),            ##dealwith callback form tcVideo
    url(r'financeInfo',finance.financeInfo),     ##GET PUT POST DELETE
    url(r'cashingRequest',finance.cashingRequest_API),
    url(r'casReqUpdate',finance.casReqUpdate),
    url(r'bankInfo',views.bankInfo_API),
    url(r'financeSummary', finance.summary),
    url(r'expense',finance.expense)
]

