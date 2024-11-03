#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDrawPrize_XDLY.py(东东心动乐园抽奖提现)
Author: HarbourJ
Date: 2024/10/17 10:00
TG: https://t.me/HarbourToulu
cron: 5 0 1,12,21 * * *
new Env('东东心动乐园抽奖提现');
ActivityEntry: https://pro.m.jd.com/mall/active/2kxGJF9NdMDjyCfvVXMVZrwfXdpT/index.html
变量：export inviteDrawPin="车头pin"
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
linkIds = ['BDhyBiZZFd5l3BkNVMqzZg']
baseJdUrl = "https://api.m.jd.com/api"
activityUrl = "https://pro.m.jd.com/mall/active/2kxGJF9NdMDjyCfvVXMVZrwfXdpT/index.html"
apCashPageSize = 1

def getJdTime ():#line:1
    OOOO00OOOOOOOO00O =int (round (time .time ()*1000 ))#line:2
    return OOOO00OOOOOOOO00O #line:3
def printf (OOO0000000OOO0000 ,OO0O0OO0O0OOO000O ):#line:5
    try :#line:6
        O00OOO00OOO0O000O =re .compile (r'pt_pin=(.*?);').findall (OOO0000000OOO0000 )[0 ]#line:7
        O00OOO00OOO0O000O =unquote_plus (O00OOO00OOO0O000O )#line:8
    except IndexError :#line:9
        O00OOO00OOO0O000O =re .compile (r'pin=(.*?);').findall (OOO0000000OOO0000 )[0 ]#line:10
        O00OOO00OOO0O000O =unquote_plus (O00OOO00OOO0O000O )#line:11
    print (f"{str(datetime.now())[0:22]}->{O00OOO00OOO0O000O}->{OO0O0OO0O0OOO000O}")#line:12
def base64Encode (OOOO00O000OOO0O00 ):#line:14
    OOOOO000OO00OOO0O =""#line:15
    OO00O0OOO0O000000 =[]#line:16
    O0O0OO00OO00OO000 =""#line:17
    OO0OO000O000O00OO ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:18
    for O00O0OO0O0OO0O00O in OOOO00O000OOO0O00 :#line:19
        OOOOO000OO00OOO0O +="{:08}".format (int (str (bin (ord (O00O0OO0O0OO0O00O ))).replace ("0b","")))#line:20
    for OOOO0O000OO00000O in range (0 ,len (OOOOO000OO00OOO0O ),6 ):#line:21
        OO00O0OOO0O000000 .append ("{:<06}".format (OOOOO000OO00OOO0O [OOOO0O000OO00000O :OOOO0O000OO00000O +6 ]))#line:22
    for OOOOOO00O00O00OOO in OO00O0OOO0O000000 :#line:23
        O0O0OO00OO00OO000 =O0O0OO00OO00OO000 +OO0OO000O000O00OO [int (OOOOOO00O00O00OOO ,2 )]#line:24
    if len (O0O0OO00OO00OO000 )%4 ==2 :#line:25
        O0O0OO00OO00OO000 +="=="#line:26
    elif len (O0O0OO00OO00OO000 )%4 ==3 :#line:27
        O0O0OO00OO00OO000 +="="#line:28
    return O0O0OO00OO00OO000 #line:29
def userAgent ():#line:31
    import uuid #line:32
    O0OOO0O0O00000000 ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:47
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(O0OOO0O0O00000000).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:48
def get_h5st_body (O0OOOOO000OO0O0OO ,OOOO000O000O0OOOO ,OOOOOOO0O0OOOOOO0 ,OO000O000OO0OOO00 ,O0O0000O0OOO0OOOO ,OOOO00OOO00OO0O0O ):#line:50
    try :#line:51
        O00OOO0O0O0000OOO =re .compile (r'pt_pin=(.*?);').findall (OOOO000O000O0OOOO )[0 ]#line:52
        O00OOO0O0O0000OOO =unquote_plus (O00OOO0O0O0000OOO )#line:53
    except IndexError :#line:54
        O00OOO0O0O0000OOO =re .compile (r'pin=(.*?);').findall (OOOO000O000O0OOOO )[0 ]#line:55
        O00OOO0O0O0000OOO =unquote_plus (O00OOO0O0O0000OOO )#line:56
    O00OO00O00000OO0O =O0OOOOO000OO0O0OO .split (";")[2 ]#line:57
    O0O0000O0OOO0OOOO ={"t":True ,"appId":OO000O000OO0OOO00 ,"appid":"activities_platform","ua":O0OOOOO000OO0O0OO ,"pin":O00OOO0O0O0000OOO ,"functionId":OOOOOOO0O0OOOOOO0 ,"body":O0O0000O0OOO0OOOO ,"clientVersion":O00OO00O00000OO0O ,"client":"ios","version":OOOO00OOO00OO0O0O }#line:69
    try :#line:70
        import base64 #line:71
        O00OO00O0OOOO0O00 =["aHR0cDovLzEuOTQuMTY4Ljg0OjMwMDkvYXBpL2g1c3Q="]#line:72
        OO00O000O0OO0000O =random .choice (O00OO00O0OOOO0O00 )#line:73
        O0OOO0O00O0OO0000 =json .dumps (O0O0000O0OOO0OOOO )#line:74
        O00OOOO0000O00O00 ={'Content-Type':'application/json'}#line:77
        O0OOO00OO0O0O00OO =requests .request ("POST",base64 .b64decode (OO00O000O0OO0000O .encode ('utf-8')).decode ('utf-8'),headers =O00OOOO0000O00O00 ,timeout =10 ,data =O0OOO0O00O0OO0000 ).json ()#line:78
        if O0OOO00OO0O0O00OO ['code']==200 :#line:79
            return O0OOO00OO0O0O00OO ['data']#line:81
        else :#line:82
            printf (OOOO000O000O0OOOO ,f"调用远程h5st接口失败1")#line:83
            return #line:84
    except Exception as O00000OO0OO00000O :#line:85
        printf (OOOO000O000O0OOOO ,f"调用远程h5st接口失败2:{O00000OO0OO00000O}")#line:86
        get_h5st_body (O0OOOOO000OO0O0OO ,OOOO000O000O0OOOO ,OOOOOOO0O0OOOOOO0 ,OO000O000OO0OOO00 ,O0O0000O0OOO0OOOO ,OOOO00OOO00OO0O0O )#line:87
        return #line:88
def inviteFissionDrawPrize (O00OOOO0OOOOO0OOO ,OOOO00000OOO00000 ,O0OOOOO0O0OOO000O ,OOO0OOO00OO00OOO0 ,OOO0O0O00OOOO000O ):#line:90
    O00O00O00OOOO000O =get_h5st_body (O00OOOO0OOOOO0OOO ,OOOO00000OOO00000 ,O0OOOOO0O0OOO000O ,OOO0OOO00OO00OOO0 ,OOO0O0O00OOOO000O ,"4.8")#line:91
    if not O00O00O00OOOO000O :#line:92
        return #line:93
    OOO00O0OO0OOO0000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O00OOOO0OOOOO0OOO ,'Cookie':OOOO00000OOO00000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://pro.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'application/json, text/plain, */*','Sec-Fetch-Site':'same-site','Sec-Fetch-Mode':'cors','x-rp-client':'h5_1.0.0',}#line:108
    OOOOO0O000O00O0OO =requests .request ("POST",baseJdUrl ,headers =OOO00O0OO0OOO0000 ,data =O00O00O00OOOO000O )#line:109
    if OOOOO0O000O00O0OO .status_code ==200 :#line:110
        try :#line:111
            O0000OO0O00O00O0O =OOOOO0O000O00O0OO .json ()#line:112
            if O0000OO0O00O00O0O ['data']:#line:113
                return OOOOO0O000O00O0OO .status_code ,O0000OO0O00O00O0O ['data']['prizeValue'],O0000OO0O00O00O0O ['data']['rewardType']#line:114
            else :#line:115
                return OOOOO0O000O00O0OO .status_code ,O0000OO0O00O00O0O #line:116
        except Exception as O00OO000O0OO0OOO0 :#line:117
            printf (OOOO00000OOO00000 ,f"{OOOOO0O000O00O0OO.text}")#line:118
            exit ()#line:119
    else :#line:120
        printf (OOOO00000OOO00000 ,f"{OOOOO0O000O00O0OO.status_code}")#line:121
        return OOOOO0O000O00O0OO .status_code ,OOOOO0O000O00O0OO .text #line:122
def inviteFissionReceive (O000OOO00OO00O0O0 ,O00O00O000O00OO00 ,O00OOO0OO000OOO0O ,OOO0000O0O0OO0OOO ,OOO0OOO0O000O00O0 ):#line:124
    OOOO0000O00OO0OOO =get_h5st_body (O000OOO00OO00O0O0 ,O00O00O000O00OO00 ,O00OOO0OO000OOO0O ,OOO0000O0O0OO0OOO ,OOO0OOO0O000O00O0 ,"4.8")#line:125
    if not OOOO0000O00OO0OOO :#line:126
        return #line:127
    OOOO0000O00OO0OOO =OOOO0000O00OO0OOO +"&loginType=2&loginWQBiz=wegame&&x-api-eid-token=&uuid=-1"#line:128
    OOOO000OOO00OO00O ={'accept':'application/json, text/plain, */*','accept-encoding':'gzip, deflate, br, zstd','accept-language':'zh-CN,zh;q=0.9','cache-control':'no-cache','content-type':'application/x-www-form-urlencoded','cookie':O00O00O000O00OO00 ,'origin':'https://pro.m.jd.com','referer':activityUrl ,'sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-site','user-agent':O000OOO00OO00O0O0 ,'x-referer-page':activityUrl ,'x-rp-client':'h5_1.0.0'}#line:144
    O000OOOO0000O00OO =requests .request ("POST",baseJdUrl +"?functionId=drawFissionReceive",headers =OOOO000OOO00OO00O ,data =OOOO0000O00OO0OOO )#line:145
    if O000OOOO0000O00OO .status_code ==200 :#line:147
        O0OOO00OOO000OO0O =O000OOOO0000O00OO .json ()#line:148
        if O0OOO00OOO000OO0O ['data']:#line:149
            return O0OOO00OOO000OO0O ['data']#line:151
        else :#line:152
            printf (O00O00O000O00OO00 ,f"{O000OOOO0000O00OO.status_code} {O0OOO00OOO000OO0O}")#line:153
            return O0OOO00OOO000OO0O #line:154
    else :#line:155
        printf (O00O00O000O00OO00 ,f"{O000OOOO0000O00OO.status_code} {O000OOOO0000O00OO.text}")#line:156
def superRedBagList (O0O00O000O00O0000 ,OO0000O0OO00O0O00 ,OOOO000OOOO0OO00O ,OO000O0OOO0O0OO00 ,O00000OOO0O00OOOO ):#line:158
    O0OO0OO0O00000O0O =get_h5st_body (O0O00O000O00O0000 ,OO0000O0OO00O0O00 ,OOOO000OOOO0OO00O ,OO000O0OOO0O0OO00 ,O00000OOO0O00OOOO ,"4.8")#line:159
    if not O0OO0OO0O00000O0O :#line:160
        return #line:161
    O0OO0OO0O00000O0O =O0OO0OO0O00000O0O +"&loginType=2&loginWQBiz=wegame&&x-api-eid-token=&uuid=-1"#line:162
    O00OOO00OOOOO0O00 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0O00O000O00O0000 ,'Cookie':OO0000O0OO00O0O00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'X-Referer-Page':activityUrl ,'X-Rp-Client':'h5_1.0.0','Origin':'https://pro.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:176
    try :#line:177
        from curl_cffi import requests #line:178
    except ImportError as O00OO00OO0O0O0OOO :#line:179
        if "No module"in str (O00OO00OO0O0O0OOO ):#line:180
            os .system ("pip install curl_cffi")#line:181
        from curl_cffi import requests #line:182
    OO00OO00O0000O0OO =requests .request ("POST",baseJdUrl ,impersonate ="chrome124",headers =O00OOO00OOOOO0O00 ,data =O0OO0OO0O00000O0O )#line:183
    if OO00OO00O0000O0OO .status_code ==200 :#line:185
        O0000OOO0O00OOOOO =OO00OO00O0000O0OO .json ()#line:186
        try :#line:187
            if O0000OOO0O00OOOOO ['data']:#line:188
                return O0000OOO0O00OOOOO ['data']#line:189
            else :#line:190
                printf (OO0000O0OO00O0O00 ,f"{OO00OO00O0000O0OO.status_code} {O0000OOO0O00OOOOO}")#line:191
                return OO00OO00O0000O0OO .text #line:192
        except Exception as O00OO00OO0O0O0OOO :#line:193
            printf (OO0000O0OO00O0O00 ,f"{OO00OO00O0000O0OO.text}")#line:194
            exit ()#line:195
    else :#line:196
        printf (OO0000O0OO00O0O00 ,f"{OO00OO00O0000O0OO.status_code}")#line:197
        if OO00OO00O0000O0OO .status_code ==403 :#line:198
            printf (OO0000O0OO00O0O00 ,"提现接口403 退出！")#line:199
            exit ()#line:200
def apCashWithDraw (O00000O0O0000OOOO ,OOOO00O0O0000O0O0 ,OOOO000OO00OO0OOO ,O00O00000OO000OOO ,OOO00OOOOO0OOO000 ,OOO0OO00OOO0O0O00 ):#line:202
    O0000O000O000O000 ="https://api.m.jd.com/"#line:204
    OOO00O0OO0OO000OO ={"linkId":linkId ,"channel":"1","businessSource":"NONE","base":{"id":OOOO00O0O0000O0O0 ,"business":"fission","poolBaseId":OOOO000OO00OO0OOO ,"prizeGroupId":O00O00000OO000OOO ,"prizeBaseId":OOO00OOOOO0OOO000 ,"prizeType":4 ,"activityId":OOO0OO00OOO0O0O00 }}#line:218
    OO000OOO00OO0OOO0 =get_h5st_body (ua ,O00000O0O0000OOOO ,"apCashWithDraw","8c6ae",OOO00O0OO0OO000OO ,"4.8")#line:219
    if not OO000OOO00OO0OOO0 :#line:220
        return #line:221
    OO0O000OO0O000O00 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O00000O0O0000OOOO ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:233
    O00OOO0O0O0O0O0OO =requests .request ("POST",O0000O000O000O000 ,headers =OO0O000OO0O000O00 ,data =OO000OOO00OO0OOO0 )#line:234
    if O00OOO0O0O0O0O0OO .status_code ==200 :#line:235
        OO00O000000O0O0OO =O00OOO0O0O0O0O0OO .json ()#line:236
        if OO00O000000O0O0OO ['data']:#line:237
            return OO00O000000O0O0OO ['data']['message']#line:238
        else :#line:239
            printf (O00000O0O0000OOOO ,f"{O00OOO0O0O0O0O0OO.status_code} {OO00O000000O0O0OO}")#line:240
def apRecompenseDrawPrize (OO0O0OO00OOO0O00O ,OOOOO0OOO0OO0OO00 ,O0OO0OOOOOO00OO0O ,O000000O0O0O00OO0 ,O0O0OO0OOOO0O000O ):#line:242
    O0O0OOO00000O0OO0 ="https://api.m.jd.com/"#line:243
    OOO0O00OOOO0OO00O ={"linkId":linkId ,"drawRecordId":OOOOO0OOO0OO0OO00 ,"business":"fission","poolId":O0OO0OOOOOO00OO0O ,"prizeGroupId":O000000O0O0O00OO0 ,"prizeId":O0O0OO0OOOO0O000O ,}#line:250
    OOOOO000OO0O000O0 =get_h5st_body (ua ,OO0O0OO00OOO0O00O ,"apRecompenseDrawPrize","8c6ae",OOO0O00OOOO0OO00O ,"4.8")#line:251
    if not OOOOO000OO0O000O0 :#line:252
        return #line:253
    OO0OO0OO00O0O0O00 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OO0O0OO00OOO0O00O ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:265
    OO0O0O000O00O0000 =requests .request ("POST",O0O0OOO00000O0OO0 ,headers =OO0OO0OO00O0O0O00 ,data =OOOOO000OO0O000O0 )#line:266
    if OO0O0O000O00O0000 .status_code ==200 :#line:267
        OO00OO0O0O00OO0O0 =OO0O0O000O00O0000 .json ()#line:268
        if OO00OO0O0O00OO0O0 ['data']:#line:269
            return "兑换红包成功"#line:271
        else :#line:272
            printf (OO0O0OO00OOO0O00O ,f"{OO0O0O000O00O0000.status_code} {OO00OO0O0O00OO0O0}")#line:273
if __name__ =='__main__':#line:276
    try :#line:277
        cks =getCk #line:278
        if not cks :#line:279
            sys .exit ()#line:280
    except :#line:281
        print ("未获取到有效COOKIE,退出程序！")#line:282
        sys .exit ()#line:283
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:284
    if inviteDrawPin :#line:285
        cookie_ =[O0OO0O0OO0OOOO0OO for O0OO0O0OO0OOOO0OO in cks if inviteDrawPin in O0OO0O0OO0OOOO0OO ]#line:286
        if cookie_ :#line:287
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:288
            cookie =cookie_ [0 ]#line:289
        else :#line:290
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:291
            sys .exit ()#line:292
    else :#line:293
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:294
        cookie =cks [0 ]#line:295
    ua =userAgent ()#line:296
    cash =[]#line:297
    successful =[]#line:298
    total =0 #line:299
    i =0 #line:300
    redpacket =[]#line:301
    for index ,linkId in enumerate (linkIds ,1 ):#line:303
        while True :#line:304
            info =inviteFissionReceive (ua ,cookie ,"drawFissionReceive","1dd0c",{"envType":1 ,"linkId":linkId })#line:344
            if "火爆"in str (info ):#line:345
                printf (cookie ,f"{info['errMsg']}")#line:346
                break #line:349
            if not info :#line:350
                time .sleep (5 )#line:351
                if not inviteFissionReceive (ua ,cookie ,"drawFissionReceive","1dd0c",{"envType":1 ,"linkId":linkId }):#line:352
                    continue #line:353
            try :#line:354
                amount_all =info ['amount']#line:355
                totalAmount =info ['totalAmount']#line:356
                leftAmount =info ['leftAmount']#line:357
            except Exception as e :#line:358
                time .sleep (10 )#line:359
                printf (cookie ,info )#line:360
                continue #line:361
            if info ['receiveList']:#line:362
                msg ='💰领现金'#line:363
                receiveList =info ['receiveList']#line:364
                for index ,receive_amount in enumerate (receiveList ,1 ):#line:365
                    amount =receiveList [index -1 ]['amount']#line:366
                    printf (cookie ,f"{msg}{amount}, 进度{amount_all}/{totalAmount} | 剩余{leftAmount}")#line:367
                if str (leftAmount )=="0.00":#line:368
                    break #line:369
            else :#line:370
                msg ='❌提现金失败'#line:371
                printf (cookie ,f"{msg}")#line:372
            time .sleep (5 )#line:374
    print (f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(O0O0000O00OO0OO00) for O0O0000O00OO0OO00 in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(O0OOO0O0OOO00O0OO) for O0OOO0O0OOO00O0OO in redpacket]))}元红包,开始提现****************\n")#line:376
    print (f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置****************")#line:378
    cashSuccess =0 #line:379
    cashFail =0 #line:380
    for index ,linkId in enumerate (linkIds ,1 ):#line:381
        i =0 #line:382
        while True :#line:383
            print (f"\n开始获取第{i + 1}页奖励列表\n")#line:384
            body ={"pageNum":i ,"pageSize":400 ,"linkId":linkId ,"associateLinkId":"","business":"fission","prizeTypeLists":[7 ]}#line:385
            info =superRedBagList (ua ,cookie ,"superRedBagList","f2b1d",body )#line:386
            if not info :#line:387
                print ("等待10s重新获取")#line:388
                time .sleep (10 )#line:389
                continue #line:390
            i +=1 #line:391
            items =info ['items']#line:392
            if not items :#line:393
                printf (cookie ,"全部提现完成！")#line:394
                break #line:395
            for item in items :#line:396
                id =item ['id']#line:398
                amount =item ['amount']#line:399
                prizeType =item ['prizeType']#line:400
                state =item ['state']#line:401
                prizeConfigName =item ['prizeConfigName']#line:402
                prizeGroupId =item ['prizeGroupId']#line:403
                poolBaseId =item ['poolBaseId']#line:404
                prizeBaseId =item ['prizeBaseId']#line:405
                activityId =item ['activityId']#line:406
                if prizeType ==4 and state !=3 and state !=4 and state !=-1 :#line:407
                    cashInfo =apCashWithDraw (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId ,activityId )#line:408
                    if cashInfo :#line:409
                        printf (cookie ,f"{amount}现金 {cashInfo}")#line:410
                        if cashInfo =="提现中":#line:411
                            cashSuccess +=float (amount )#line:412
                        else :#line:413
                            cashFail +=float (amount )#line:414
                        if "上限"in cashInfo or "其他pin"in cashInfo or "其它pin"in cashInfo :#line:415
                            cashInfo =apRecompenseDrawPrize (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:416
                            printf (cookie ,f"{amount}现金 {cashInfo}")#line:417
                    time .sleep (10 )#line:418
                else :#line:419
                    continue #line:420
            time .sleep (3 )#line:422
            if i >=apCashPageSize :#line:424
                break #line:425
    print (f"\n****************提现结束,成功提现💵{round(cashSuccess, 2)}元现金,剩余待提现💵{round(cashFail, 2)}元现金****************")