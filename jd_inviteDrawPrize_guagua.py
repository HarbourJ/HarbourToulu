#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDrawPrize_guagua.py(夺金刮刮乐抽奖提现)
Author: HarbourJ
Date: 2024/7/26 10:00
TG: https://t.me/HarbourToulu
cron: 30 0 0,12,21 * * *
new Env('夺金刮刮乐抽奖提现');
ActivityEntry: https://pro.m.jd.com/mall/active/3pdfN7oPzb6if7pB8N8dMr4dV2ys/index.html
变量：export inviteDrawPin="车头pin"
     export apCashPageSize="提现的最大页数"
"""

import time, requests, sys, re, os, json, random
from urllib.parse import quote_plus, unquote_plus, quote
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    from jd_sign import *
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")
    sys.exit()
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

apCashPageSize = int(os.environ.get("apCashPageSize")) if os.environ.get("apCashPageSize") else 5 # 提现的最大页数，可根据实际情况修改
linkIds = ['1v8ROyHv8LXPs559oaclNA']
baseJdUrl = "https://api.m.jd.com/api"
activityUrl = "https://pro.m.jd.com/mall/active/3pdfN7oPzb6if7pB8N8dMr4dV2ys/index.html"

def getJdTime ():#line:1
    O0O0O0O000OOO0O00 =int (round (time .time ()*1000 ))#line:2
    return O0O0O0O000OOO0O00 #line:3
def printf (OOO0000O0OO0OOOOO ,OOOO0O000O0O000OO ):#line:5
    try :#line:6
        O0OOO000O00000OOO =re .compile (r'pt_pin=(.*?);').findall (OOO0000O0OO0OOOOO )[0 ]#line:7
        O0OOO000O00000OOO =unquote_plus (O0OOO000O00000OOO )#line:8
    except IndexError :#line:9
        O0OOO000O00000OOO =re .compile (r'pin=(.*?);').findall (OOO0000O0OO0OOOOO )[0 ]#line:10
        O0OOO000O00000OOO =unquote_plus (O0OOO000O00000OOO )#line:11
    print (f"{str(datetime.now())[0:22]}->{O0OOO000O00000OOO}->{OOOO0O000O0O000OO}")#line:12
def base64Encode (O00O000O0O00OO000 ):#line:14
    O0OO0OOO000OOO0OO =""#line:15
    O0OOOOOO0OO00OO0O =[]#line:16
    O0O0O0000OO00O000 =""#line:17
    OOO000OOO0OOO0OOO ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:18
    for O000O0000OOOO000O in O00O000O0O00OO000 :#line:19
        O0OO0OOO000OOO0OO +="{:08}".format (int (str (bin (ord (O000O0000OOOO000O ))).replace ("0b","")))#line:20
    for OOOO0O00000O00O00 in range (0 ,len (O0OO0OOO000OOO0OO ),6 ):#line:21
        O0OOOOOO0OO00OO0O .append ("{:<06}".format (O0OO0OOO000OOO0OO [OOOO0O00000O00O00 :OOOO0O00000O00O00 +6 ]))#line:22
    for O0O00OO00O000OOO0 in O0OOOOOO0OO00OO0O :#line:23
        O0O0O0000OO00O000 =O0O0O0000OO00O000 +OOO000OOO0OOO0OOO [int (O0O00OO00O000OOO0 ,2 )]#line:24
    if len (O0O0O0000OO00O000 )%4 ==2 :#line:25
        O0O0O0000OO00O000 +="=="#line:26
    elif len (O0O0O0000OO00O000 )%4 ==3 :#line:27
        O0O0O0000OO00O000 +="="#line:28
    return O0O0O0000OO00O000 #line:29
def userAgent ():#line:31
    import uuid #line:32
    OOOO00OOOO000O000 ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:47
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(OOOO00OOOO000O000).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:48
def get_h5st_body (O000O0O00O0OO00O0 ,O0OO0000OO0O0OO00 ,OOOO00OOOOOOOO0O0 ,OOO0O0O0OOOO0OOO0 ,OOO0O0O00OO0O0O00 ,O0O0O0OOO0O0000O0 ):#line:50
    try :#line:51
        O0O00O000OOO00OO0 =re .compile (r'pt_pin=(.*?);').findall (O0OO0000OO0O0OO00 )[0 ]#line:52
        O0O00O000OOO00OO0 =unquote_plus (O0O00O000OOO00OO0 )#line:53
    except IndexError :#line:54
        O0O00O000OOO00OO0 =re .compile (r'pin=(.*?);').findall (O0OO0000OO0O0OO00 )[0 ]#line:55
        O0O00O000OOO00OO0 =unquote_plus (O0O00O000OOO00OO0 )#line:56
    OOO0O0O0O00000000 =O000O0O00O0OO00O0 .split (";")[2 ]#line:57
    OOO0O0O00OO0O0O00 ={"t":True,"appId":OOO0O0O0OOOO0OOO0,"appid":"activities_platform","ua":O000O0O00O0OO00O0,"pin":O0O00O000OOO00OO0,"functionId":OOOO00OOOOOOOO0O0,"body":OOO0O0O00OO0O0O00,"clientVersion":OOO0O0O0O00000000,"client":"ios","version":O0O0O0OOO0O0000O0}#line:69
    try :#line:70
        import base64 #line:71
        OO00OO0OO0O00000O =["aHR0cDovLzEuMTQuMjA4LjE3ODozMDAzL2FwaS9oNXN0"]#line:72
        OOOO00O0OO000000O =random .choice (OO00OO0OO0O00000O )#line:73
        O00O0OOOO0O0000O0 =json .dumps (OOO0O0O00OO0O0O00 )#line:74
        OOOOOOOO0OOO0OO00 ={'Content-Type':'application/json'}#line:77
        OOOO000OOO00000OO =requests .request ("POST",base64 .b64decode (OOOO00O0OO000000O .encode ('utf-8')).decode ('utf-8'),headers =OOOOOOOO0OOO0OO00 ,timeout =10 ,data =O00O0OOOO0O0000O0 ).json ()#line:78
        if OOOO000OOO00000OO ['code']==200 :#line:79
            return OOOO000OOO00000OO ['data']#line:80
        else :#line:81
            printf (O0OO0000OO0O0OO00 ,f"调用远程h5st接口失败1")#line:82
            return #line:83
    except Exception as O00OOOOOOO000OOO0 :#line:84
        printf (O0OO0000OO0O0OO00 ,f"调用远程h5st接口失败2:{O00OOOOOOO000OOO0}")#line:85
        get_h5st_body (O000O0O00O0OO00O0 ,O0OO0000OO0O0OO00 ,OOOO00OOOOOOOO0O0 ,OOO0O0O0OOOO0OOO0 ,OOO0O0O00OO0O0O00 ,O0O0O0OOO0O0000O0 )#line:86
        return #line:87
def inviteFissionDrawPrize (O0O0OOO0OOOOO0O0O ,O0O00OO0O0000OO00 ,O0OOO000000OO00O0 ,OOOO00OO0O0OO0O00 ,OOO0O00000OOOO0OO ):#line:89
    O000OOOO000O00O00 =get_h5st_body (O0O0OOO0OOOOO0O0O ,O0O00OO0O0000OO00 ,O0OOO000000OO00O0 ,OOOO00OO0O0OO0O00 ,OOO0O00000OOOO0OO ,"4.7")#line:90
    if not O000OOOO000O00O00 :#line:91
        return #line:92
    O000O0O0O0OO0O0O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0O0OOO0OOOOO0O0O ,'Cookie':O0O00OO0O0000OO00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://pro.m.jd.com','X-Referer-Page':activityUrl ,'X-Rp-Client':'h5_1.0.0','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:106
    O00OO000OO00OOO0O =requests .request ("POST",baseJdUrl ,headers =O000O0O0O0OO0O0O0 ,data =O000OOOO000O00O00 )#line:107
    if O00OO000OO00OOO0O .status_code ==200 :#line:108
        try :#line:109
            O000000O0OOO00OO0 =O00OO000OO00OOO0O .json ()#line:110
            if O000000O0OOO00OO0 ['data']:#line:111
                return O00OO000OO00OOO0O .status_code ,O000000O0OOO00OO0 ['data']['prizeValue'],O000000O0OOO00OO0 ['data']['rewardType']#line:112
            else :#line:113
                return O00OO000OO00OOO0O .status_code ,O00OO000OO00OOO0O .text #line:114
        except Exception as O0O00O00OO000O0O0 :#line:115
            printf (O0O00OO0O0000OO00 ,f"{O00OO000OO00OOO0O.text}")#line:116
            exit ()#line:117
    else :#line:118
        printf (O0O00OO0O0000OO00 ,f"{O00OO000OO00OOO0O.status_code}")#line:119
        return O00OO000OO00OOO0O .status_code ,O00OO000OO00OOO0O .text #line:120
def inviteFissionReceive (O000OOOO00O0OOOO0 ,O0OO0000OOOOOO00O ,OOO0O0O0O0OO000O0 ,OO0OOO00O0O0000O0 ,O0O00O0OOO000O00O ):#line:122
    OOOO0OOOOO0O00O0O =get_h5st_body (O000OOOO00O0OOOO0 ,O0OO0000OOOOOO00O ,OOO0O0O0O0OO000O0 ,OO0OOO00O0O0000O0 ,O0O00O0OOO000O00O ,"4.7")#line:123
    if not OOOO0OOOOO0O00O0O :#line:124
        return #line:125
    OOOO0OOOOO0O00O0O =OOOO0OOOOO0O00O0O +"&loginType=2&loginWQBiz=wegame&screen=1512*982&x-api-eid-token=&uuid=-1"#line:126
    O0OOO000OOO00OO00 ={'Host':'api.m.jd.com','Accept':'application/json, text/plain, */*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','User-Agent':O000OOOO00O0OOOO0 ,'Cookie':O0OO0000OOOOOO00O ,'Origin':'https://pro.m.jd.com','x-referer-page':activityUrl ,'Referer':activityUrl }#line:139
    OO00OOO000O0O00OO =requests .request ("POST",baseJdUrl ,headers =O0OOO000OOO00OO00 ,data =OOOO0OOOOO0O00O0O )#line:140
    if OO00OOO000O0O00OO .status_code ==200 :#line:141
        O0OO0O0OOOO00OO0O =OO00OOO000O0O00OO .json ()#line:142
        if O0OO0O0OOOO00OO0O ['data']:#line:143
            return O0OO0O0OOOO00OO0O ['data']#line:145
        else :#line:146
            printf (O0OO0000OOOOOO00O ,f"{OO00OOO000O0O00OO.status_code} {O0OO0O0OOOO00OO0O}")#line:147
            return O0OO0O0OOOO00OO0O #line:148
def superRedBagList (O0OOOOOO00O0O0000 ,O0OOO00OO0OO0O0OO ,O0O00O00OO00O0O00 ,OO0O0OOOO0OO0OO0O ,O0O000O0000O0O000 ):#line:150
    OO0OOO000OOOO0O00 =get_h5st_body (O0OOOOOO00O0O0000 ,O0OOO00OO0OO0O0OO ,O0O00O00OO00O0O00 ,OO0O0OOOO0OO0OO0O ,O0O000O0000O0O000 ,"4.7")#line:151
    if not OO0OOO000OOOO0O00 :#line:152
        return #line:153
    OO0OOO000OOOO0O00 =OO0OOO000OOOO0O00 +"&loginType=2&loginWQBiz=wegame&&x-api-eid-token=&uuid=-1"#line:154
    O0OOOO0OOO0000O0O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0OOOOOO00O0O0000 ,'Cookie':O0OOO00OO0OO0O0OO ,'Host':'api.m.jd.com','Referer':activityUrl ,'X-Referer-Page':activityUrl ,'X-Rp-Client':'h5_1.0.0','Origin':'https://pro.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:168
    try :#line:169
        from curl_cffi import requests #line:170
    except ImportError as O0O0OOO0O000OOO00 :#line:171
        if "No module"in str (O0O0OOO0O000OOO00 ):#line:172
            os .system ("pip install curl_cffi")#line:173
        from curl_cffi import requests #line:174
    O0O00O0000000O00O =requests .request ("POST",baseJdUrl ,impersonate ="chrome124",headers =O0OOOO0OOO0000O0O ,data =OO0OOO000OOOO0O00 )#line:175
    if O0O00O0000000O00O .status_code ==200 :#line:177
        O0000OOO0O00O0000 =O0O00O0000000O00O .json ()#line:178
        try :#line:179
            if O0000OOO0O00O0000 ['data']:#line:180
                return O0000OOO0O00O0000 ['data']#line:181
            else :#line:182
                printf (O0OOO00OO0OO0O0OO ,f"{O0O00O0000000O00O.status_code} {O0000OOO0O00O0000}")#line:183
                return O0O00O0000000O00O .text #line:184
        except Exception as O0O0OOO0O000OOO00 :#line:185
            printf (O0OOO00OO0OO0O0OO ,f"{O0O00O0000000O00O.text}")#line:186
            exit ()#line:187
    else :#line:188
        printf (O0OOO00OO0OO0O0OO ,f"{O0O00O0000000O00O.status_code}")#line:189
        if O0O00O0000000O00O .status_code ==403 :#line:190
            printf (O0OOO00OO0OO0O0OO ,"提现接口403 退出！")#line:191
            exit ()#line:192
def apCashWithDraw (OO00O00OO0O0OOO00 ,O00OO0O0000OOOOOO ,OOO00OOO00OO0O00O ,O000O000OOOOOOOO0 ,O0O0OOOOOOOO0000O ,O000OOO0000OO0O0O ):#line:194
    OOOOO000OOOOOOO00 ="https://api.m.jd.com/"#line:196
    O00OOO000OOO0O0OO ={"linkId":linkId,"channel":"1","businessSource":"NONE","base":{"id":O00OO0O0000OOOOOO,"business":"fission","poolBaseId":OOO00OOO00OO0O00O,"prizeGroupId":O000O000OOOOOOOO0,"prizeBaseId":O0O0OOOOOOOO0000O,"prizeType":4,"activityId":O000OOO0000OO0O0O }}#line:210
    OO0OO0O0O00OOOOOO =get_h5st_body (ua ,OO00O00OO0O0OOO00 ,"apCashWithDraw","8c6ae",O00OOO000OOO0O0OO ,"4.7")#line:211
    if not OO0OO0O0O00OOOOOO :#line:212
        return #line:213
    OO0O0000000OO00O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OO00O00OO0O0OOO00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:225
    O0O000000000OOO0O =requests .request ("POST",OOOOO000OOOOOOO00 ,headers =OO0O0000000OO00O0 ,data =OO0OO0O0O00OOOOOO )#line:226
    if O0O000000000OOO0O .status_code ==200 :#line:227
        O00000O00O0O00O00 =O0O000000000OOO0O .json ()#line:228
        if O00000O00O0O00O00 ['data']:#line:229
            return O00000O00O0O00O00 ['data']['message']#line:230
        else :#line:231
            printf (OO00O00OO0O0OOO00 ,f"{O0O000000000OOO0O.status_code} {O00000O00O0O00O00}")#line:232
def apRecompenseDrawPrize (O0O0O0OOO0000O00O ,OO0OO0OOOOOO0O000 ,O00O0O0O00OO00O00 ,OO00OOO0O00O0O0O0 ,O0OO0O0OOOOOO00O0 ):#line:234
    O0O000OOO000OO0O0 ="https://api.m.jd.com/"#line:235
    O0OOOO00000OOO0OO ={"linkId":linkId,"drawRecordId":OO0OO0OOOOOO0O000,"business":"fission","poolId":O00O0O0O00OO00O00,"prizeGroupId":OO00OOO0O00O0O0O0,"prizeId":O0OO0O0OOOOOO00O0 ,}#line:242
    OO0OOO000O0000OO0 =get_h5st_body (ua ,O0O0O0OOO0000O00O ,"apRecompenseDrawPrize","8c6ae",O0OOOO00000OOO0OO ,"4.7")#line:243
    if not OO0OOO000O0000OO0 :#line:244
        return #line:245
    OO00OO0O0O0O0O0O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O0O0O0OOO0000O00O ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:257
    O0OO0OOOO0OO0OOOO =requests .request ("POST",O0O000OOO000OO0O0 ,headers =OO00OO0O0O0O0O0O0 ,data =OO0OOO000O0000OO0 )#line:258
    if O0OO0OOOO0OO0OOOO .status_code ==200 :#line:259
        OO00O0O00OOOO0OO0 =O0OO0OOOO0OO0OOOO .json ()#line:260
        if OO00O0O00OOOO0OO0 ['data']:#line:261
            return "兑换红包成功"#line:263
        else :#line:264
            printf (O0O0O0OOO0000O00O ,f"{O0OO0OOOO0OO0OOOO.status_code} {OO00O0O00OOOO0OO0}")#line:265
if __name__ =='__main__':#line:268
    try :#line:269
        cks =getCk #line:270
        if not cks :#line:271
            sys .exit ()#line:272
    except :#line:273
        print ("未获取到有效COOKIE,退出程序！")#line:274
        sys .exit ()#line:275
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:276
    if inviteDrawPin :#line:277
        cookie_ =[OOOOO00O0O0OO000O for OOOOO00O0O0OO000O in cks if inviteDrawPin in OOOOO00O0O0OO000O ]#line:278
        if cookie_ :#line:279
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:280
            cookie =cookie_ [0 ]#line:281
        else :#line:282
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:283
            sys .exit ()#line:284
    else :#line:285
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:286
        cookie =cks [0 ]#line:287
    ua =userAgent ()#line:288
    cash =[]#line:289
    successful =[]#line:290
    total =0 #line:291
    i =0 #line:292
    redpacket =[]#line:293
    for index ,linkId in enumerate (linkIds ,1 ):#line:295
        while True :#line:296
            try :#line:297
                info =inviteFissionDrawPrize (ua ,cookie ,"inviteFissionDrawPrize","c02c6",{"linkId":linkId,"area":""})#line:298
                if "活动太火爆"in str (info ):#line:299
                    printf (cookie ,info )#line:300
                    time .sleep (3 )#line:301
                    continue #line:302
            except Exception as e :#line:303
                printf (cookie ,e )#line:304
                time .sleep (3 )#line:305
                continue #line:306
            if not info :#line:307
                time .sleep (3 )#line:308
                continue #line:309
            if not info [1 ]:#line:310
                time .sleep (10 )#line:311
                continue #line:312
            elif "抽奖次数已用完"in info [1 ]:#line:313
                printf (cookie ,f"{info[0]} ⚠️抽奖次数已用完")#line:314
                break #line:315
            elif "本场活动已结束"in info [1 ]:#line:316
                printf (cookie ,f"{info[0]} ⏰本场活动已结束了,快去重新开始吧")#line:317
                break #line:318
            else :#line:319
                if info :#line:320
                    total +=1 #line:321
                    if info [2 ]==1 :#line:322
                        printf (cookie ,f"{info[0]} 🎫获得{info[1]}优惠券")#line:323
                    elif info [2 ]==2 :#line:324
                        printf (cookie ,f"{info[0]} 🧧获得{info[1]}红包")#line:325
                        redpacket .append (info [1 ])#line:326
                    else :#line:327
                        printf (cookie ,f"{info[0]} 💵获得{info[1]}现金")#line:328
                        cash .append (info [1 ])#line:329
            time .sleep (0.5 )#line:330
            info =inviteFissionReceive (ua ,cookie ,"inviteFissionReceive","b8469",{"linkId":linkId})#line:332
            if "火爆"in str (info ):#line:333
                printf (cookie ,f"{info['errMsg']}")#line:334
                time .sleep (3 )#line:335
                continue #line:336
            amount_all =info ['amount']#line:337
            totalAmount =info ['totalAmount']#line:338
            leftAmount =info ['leftAmount']#line:339
            if info ['receiveList']:#line:340
                msg ='💰领现金'#line:341
                amount =info ['receiveList'][0 ]['amount']#line:342
                printf (cookie ,f"{msg}{amount}, 进度{amount_all}/{totalAmount}")#line:343
                if str (leftAmount )=="0.00":#line:344
                    break #line:345
            else :#line:346
                msg ='❌提现金失败'#line:347
                printf (cookie ,f"{msg}")#line:348
            time .sleep (3 )#line:350
    print (f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(OOO0OO0O000OOO0OO) for OOO0OO0O000OOO0OO in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(OO0OOOO00O000O0O0) for OO0OOOO00O000O0O0 in redpacket]))}元红包,开始提现****************\n")#line:352
    print (f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置****************")#line:354
    cashSuccess =0 #line:355
    cashFail =0 #line:356
    for index ,linkId in enumerate (linkIds ,1 ):#line:357
        i =0 #line:358
        while True :#line:359
            print (f"\n开始获取第{i + 1}页奖励列表\n")#line:360
            body ={"pageNum":i,"pageSize":400,"linkId":linkId,"associateLinkId":"","business":"fission","prizeTypeLists":[7 ]}#line:361
            info =superRedBagList (ua ,cookie ,"superRedBagList","f2b1d",body )#line:362
            if not info :#line:363
                print ("等待10s重新获取")#line:364
                time .sleep (10 )#line:365
                continue #line:366
            i +=1 #line:367
            items =info ['items']#line:368
            if not items :#line:369
                printf (cookie ,"全部提现完成！")#line:370
                break #line:371
            for item in items :#line:372
                id =item ['id']#line:374
                amount =item ['amount']#line:375
                prizeType =item ['prizeType']#line:376
                state =item ['state']#line:377
                prizeConfigName =item ['prizeConfigName']#line:378
                prizeGroupId =item ['prizeGroupId']#line:379
                poolBaseId =item ['poolBaseId']#line:380
                prizeBaseId =item ['prizeBaseId']#line:381
                activityId =item ['activityId']#line:382
                if prizeType ==4 and state !=3 and state !=4 and state !=-1 :#line:383
                    cashInfo =apCashWithDraw (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId ,activityId )#line:384
                    if cashInfo :#line:385
                        printf (cookie ,f"{amount}现金 {cashInfo}")#line:386
                        if cashInfo =="提现中":#line:387
                            cashSuccess +=float (amount )#line:388
                        else :#line:389
                            cashFail +=float (amount )#line:390
                        if "上限"in cashInfo or "其他pin"in cashInfo or "其它pin"in cashInfo :#line:391
                            cashInfo =apRecompenseDrawPrize (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:392
                            printf (cookie ,f"{amount}现金 {cashInfo}")#line:393
                    time .sleep (10 )#line:394
                else :#line:395
                    continue #line:396
            time .sleep (3 )#line:398
            if i >=apCashPageSize :#line:400
                break #line:401
    print (f"\n****************提现结束,成功提现💵{round(cashSuccess, 2)}元现金,剩余待提现💵{round(cashFail, 2)}元现金****************")