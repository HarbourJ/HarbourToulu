#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_lzkjInteract.py(jd_lzkjInteract邀请有礼)
Author: HarbourJ
Date: 2022/11/24 10:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('jd_lzkjInteract邀请有礼');
ActivityEntry: https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType=10070&activityId=1595256546199793665&templateId=20201228083300yqrhyl011&nodeId=101001005&prd=cjwx
变量: jd_lzkjInteractUrl 活动链接
     jd_lzkjInteractNum 指定邀请人数，不填默认活动最高邀请人数

Description: 10070 邀请xx人xx豆,自动助力,自动领奖
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from datetime import datetime #line:2
from urllib .parse import quote_plus ,unquote_plus #line:3
from functools import partial #line:4
from sendNotify import *#line:5
print =partial (print ,flush =True )#line:6
import warnings #line:7
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:8
try :#line:9
    from jd_sign import *#line:10
except ImportError as e :#line:11
    print (e )#line:12
    if "No module"in str (e ):#line:13
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:14
try :#line:15
    from jdCookie import get_cookies #line:16
    getCk =get_cookies ()#line:17
except :#line:18
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:19
    sys .exit (3 )#line:20
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:22
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:23
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:24
jd_lzkjInteractUrl =os .environ .get ("jd_lzkjInteractUrl")if os .environ .get ("jd_lzkjInteractUrl")else ""#line:25
jd_lzkjInteractNum =os .environ .get ("jd_lzkjInteractNum")if os .environ .get ("jd_lzkjInteractNum")else ""#line:26
share_userId =os .environ .get ("jd_lzkjInteractUserId")if os .environ .get ("jd_lzkjInteractUserId")else ""#line:27
if "lzkj-isv.isvjcloud.com/prod/cc/interactsaas"not in jd_lzkjInteractUrl :#line:29
    print ("⛈暂不支持变量设置的活动类型,请检查后重试！仅支持interactsaas类型活动")#line:30
    sys .exit ()#line:31
templateId =re .findall (r"templateId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:32
activityId =re .findall (r"activityId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:33
activityType =re .findall (r"activityType=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:34
activity_url =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&activityId={activityId}&shareUserId={share_userId}&templateId={templateId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:36
print (f"【🛳活动入口】https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}")#line:38
def redis_conn ():#line:40
    try :#line:41
        import redis #line:42
        try :#line:43
            O0O0O00OOO0OOO00O =redis .ConnectionPool (host =redis_url ,port =6379 ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:44
            OO00000O00OOO0O0O =redis .Redis (connection_pool =O0O0O00OOO0OOO00O )#line:45
            OO00000O00OOO0O0O .get ('conn_test')#line:46
            print ('✅redis连接成功')#line:47
            return OO00000O00OOO0O0O #line:48
        except :#line:49
            print ("⚠️redis连接异常")#line:50
    except :#line:51
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:52
        sys .exit ()#line:53
def getToken (O0OOOO0OO00OO0000 ,r =None ):#line:55
    OO0OO0000O00O000O =f'{activityUrl.split("com/")[0]}com'#line:56
    try :#line:57
        OOOO0O0O0000O0O0O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0OOOO0OO00OO0000 )[0 ])#line:58
    except :#line:59
        OOOO0O0O0000O0O0O =O0OOOO0OO00OO0000 [:15 ]#line:60
    try :#line:61
        try :#line:62
            O0000O0OO0O000OO0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO0O0O0000O0O0O}')#line:63
        except Exception as OOOOO000O0000OO0O :#line:64
            O0000O0OO0O000OO0 =None #line:65
        if O0000O0OO0O000OO0 is not None :#line:66
            print (f"♻️获取缓存Token")#line:67
            return O0000O0OO0O000OO0 #line:68
        else :#line:69
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0OOOO0OO00OO0000 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:80
            sign ({"url":f"{OO0OO0000O00O000O}","id":""},'isvObfuscator')#line:81
            OOO0O0OO00O0O0O00 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:82
            if OOO0O0OO00O0O0O00 .status_code !=200 :#line:83
                print (OOO0O0OO00O0O0O00 .status_code )#line:84
                return #line:85
            else :#line:86
                if "参数异常"in OOO0O0OO00O0O0O00 .text :#line:87
                    print (OOO0O0OO00O0O0O00 .text )#line:88
                    return #line:89
            O0000OO0O000OO0OO =OOO0O0OO00O0O0O00 .json ()['token']#line:90
            try :#line:91
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO0O0O0000O0O0O}',O0000OO0O000OO0OO ,ex =1800 ):#line:92
                    print ("✅Token缓存成功")#line:93
                else :#line:94
                    print ("❌Token缓存失败")#line:95
            except Exception as OOOOO000O0000OO0O :#line:96
                print (f"✅获取实时Token")#line:97
            return O0000OO0O000OO0OO #line:98
    except Exception as OOOOO000O0000OO0O :#line:99
        print (f"Token error: {str(OOOOO000O0000OO0O)}")#line:100
        return #line:101
def getJdTime ():#line:103
    OO0OOO00O0OOOO00O =int (round (time .time ()*1000 ))#line:104
    return OO0OOO00O0OOOO00O #line:105
def randomString (OO00OO0OOOOOOO000 ,flag =False ):#line:107
    OO0OO0O0O00OO0OOO ="0123456789abcdef"#line:108
    if flag :OO0OO0O0O00OO0OOO =OO0OO0O0O00OO0OOO .upper ()#line:109
    OO0OOOOOOOO0000O0 =[random .choice (OO0OO0O0O00OO0OOO )for _O00000OOOOO00OOOO in range (OO00OO0OOOOOOO000 )]#line:110
    return ''.join (OO0OOOOOOOO0000O0 )#line:111
def check (OO00OO0O0O00O0O00 ):#line:113
    try :#line:114
        O00O0OOOOO0OOOO0O ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:115
        OOO0OO0000000OOOO ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OO00OO0O0O00O0O00 ,"User-Agent":ua ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:125
        O00O000O0OOO0000O =requests .get (url =O00O0OOOOO0OOOO0O ,headers =OOO0OO0000000OOOO ).text #line:126
        O0O0O00O0O000O000 =json .loads (O00O000O0OOO0000O )#line:127
        if O0O0O00O0O000O000 ['retcode']=='1001':#line:128
            O0OOOO0OO00000OOO ="当前ck已失效，请检查"#line:129
            return {'code':1001 ,'data':O0OOOO0OO00000OOO }#line:130
        elif O0O0O00O0O000O000 ['retcode']=='0'and 'userInfo'in O0O0O00O0O000O000 ['data']:#line:131
            OOO000O00OO00OOOO =O0O0O00O0O000O000 ['data']['userInfo']['baseInfo']['nickname']#line:132
            return {'code':200 ,'name':OOO000O00OO00OOOO ,'ck':cookie }#line:133
    except Exception as O0000O00OOOO0O0O0 :#line:134
        return {'code':0 ,'data':O0000O00OOOO0O0O0 }#line:135
def getActivity ():#line:137
    O0O0O000O00O00O0O =activityUrl #line:138
    OO0OO00OOO0000OOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:146
    O0O000OOO00000O00 =requests .request ("GET",O0O0O000O00O00O0O ,headers =OO0OO00OOO0000OOO )#line:147
    if O0O000OOO00000O00 .status_code !=200 :#line:148
        print (O0O000OOO00000O00 .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:149
        sys .exit ()#line:150
def followShop (OO0OO0OOO000000O0 ):#line:152
    OO0OOOOOO0O0O0OO0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followShop/follow"#line:153
    OOO0000OOO0O00O00 ={}#line:154
    OO0O00OO00000O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO0OO0OOO000000O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:166
    O000O000000000OOO =requests .post (OO0OOOOOO0O0O0OO0 ,headers =OO0O00OO00000O0OO ,data =json .dumps (OOO0000OOO0O00O00 ))#line:167
    try :#line:168
        return O000O000000000OOO .json ()#line:169
    except :#line:170
        return False #line:171
def gen_uuid (e =40 ):#line:173
    from string import hexdigits #line:174
    from random import sample #line:175
    return ((e ==0 )and '0')or (gen_uuid (e -1 ).lstrip ('0')+sample (hexdigits [:-6 ],1 )[0 ])#line:176
def getUserInfo (OOO00O0OOO00000OO ):#line:178
    O000O00O0OOOOO0O0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login"#line:179
    OOO0OO00O0OO00000 ={"status":"0","activityId":activityId ,"source":"01","tokenPin":token ,"shareUserId":OOO00O0OOO00000OO ,"uuid":gen_uuid (),"envInfo":"",}#line:188
    O0OOO000OOOO00OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':'','Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};'}#line:201
    OOO0OOO0O0OO0OO0O =requests .request ("POST",O000O00O0OOOOO0O0 ,headers =O0OOO000OOOO00OO0 ,data =json .dumps (OOO0OO00O0OO00000 ))#line:202
    if OOO0OOO0O0OO0OO0O .status_code ==200 :#line:203
        OOO000OOOOOOO0000 =OOO0OOO0O0OO0OO0O .json ()#line:204
        if OOO000OOOOOOO0000 ['resp_code']==0 :#line:205
            if OOO000OOOOOOO0000 ['data']:#line:206
                return OOO000OOOOOOO0000 ['data']#line:207
            else :#line:208
                print (OOO000OOOOOOO0000 )#line:209
        else :#line:210
            print (OOO000OOOOOOO0000 ['resp_msg'])#line:211
    else :#line:212
        print (OOO0OOO0O0OO0OO0O .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:213
        sys .exit ()#line:214
def guestMyself (O0O00OOOOOO0O0O0O ,O00O0OO0O000O0OO0 ):#line:216
    O00OO00OOO000O00O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/bargain/guest/myself"#line:217
    OO0O00OOO00OOOOO0 ={"shareUserId":O00O0OO0O000O0OO0 }#line:220
    O0OOO000O0OO0000O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0O00OOOOOO0O0O0O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:232
    requests .post (O00OO00OOO000O00O ,headers =O0OOO000O0OO0000O ,data =json .dumps (OO0O00OOO00OOOOO0 ))#line:233
def getMember (O0OO00OO0OO0000OO ,OOOOOOOO000O0OO0O ):#line:235
    OOOOOOOO00O000O0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/getMember"#line:236
    OO00000OO00O000O0 ={"shareUserId":OOOOOOOO000O0OO0O }#line:239
    OOO0000OO0O00OOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0OO00OO0OO0000OO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:251
    OO0O0OOOOO000O0OO =requests .post (OOOOOOOO00O000O0O ,headers =OOO0000OO0O00OOO0 ,data =json .dumps (OO00000OO00O000O0 ))#line:252
    try :#line:253
        O0O0OOO0OO00000OO =OO0O0OOOOO000O0OO .json ()#line:254
        OOO000000O0OOOOO0 =O0O0OOO0OO00000OO ['data']['shareUser']#line:255
        return OOO000000O0OOOOO0 #line:256
    except Exception as O00O000OOOO00O00O :#line:257
        print (str (O00O000OOOO00O00O ))#line:258
        return False #line:259
def prizeList (OO00O00OOO0O0O000 ):#line:261
    OO00OOO0OOOOO0000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/prizeList"#line:262
    O0O0O000OO0O0000O ={}#line:263
    OO00OO00O0000O00O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO00O00OOO0O0O000 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:275
    OO00OO0O0OOO00O00 =requests .post (OO00OOO0OOOOO0000 ,headers =OO00OO00O0000O00O ,data =json .dumps (O0O0O000OO0O0000O ))#line:276
    try :#line:277
        return OO00OO0O0OOO00O00 .json ()#line:278
    except :#line:279
        return False #line:280
def joinCheck (OOOOO0O0OOOOO0000 ):#line:282
    O00O0OOOOO000O0O0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/join/check"#line:283
    O00OO0OO0O00OO0OO ={"status":"0"}#line:286
    O00000OO0OO00OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOOOO0O0OOOOO0000 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:298
    O0OO0OO00O0OOOOO0 =requests .post (O00O0OOOOO000O0O0 ,headers =O00000OO0OO00OO0O ,data =json .dumps (O00OO0OO0O00OO0OO ))#line:299
    try :#line:300
        return O0OO0OO00O0OOOOO0 .json ()#line:301
    except :#line:302
        return False #line:303
def getUserId (O000OO000OOO0OOO0 ):#line:305
    O0000O00OOOO0OOOO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/share/getUserId"#line:306
    O0O00OO0O0O0O0O00 ={}#line:307
    OO00OO00OO0000OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Token':O000OO000OOO0OOO0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:319
    OOOOO0OO0OO0OOO00 =requests .post (O0000O00OOOO0OOOO ,headers =OO00OO00OO0000OO0 ,data =json .dumps (O0O00OO0O0O0O0O00 ))#line:320
    try :#line:321
        if OOOOO0OO0OO0OOO00 .json ()['resp_code']!=0 :#line:322
            print (f"getUserId Error: {OOOOO0OO0OO0OOO00.json()['resp_msg']}")#line:323
            return #line:324
        return OOOOO0OO0OO0OOO00 .json ()['data']['shareUserId']#line:325
    except Exception as OO00O00O00OOO0000 :#line:326
        print (f"getUserId Error: {OO00O00O00OOO0000}")#line:327
def receiveAcquire (OO0O000O00OOO000O ,O000O0OO0OOOOOO0O ):#line:329
    OO0OOO0O0OOOOO0OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/receive/acquire"#line:330
    OOOOO00O00O0000O0 ={"prizeInfoId":O000O0OO0OOOOOO0O ,"status":1 }#line:334
    O000O0O00OO0OOO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO0O000O00OOO000O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:346
    OOO0OO0O00O000OOO =requests .post (OO0OOO0O0OOOOO0OO ,headers =O000O0O00OO0OOO00 ,data =json .dumps (OOOOO00O00O0000O0 ))#line:347
    try :#line:348
        return OOO0OO0O00O000OOO .json ()['resp_code']#line:349
    except :#line:350
        print (OOO0OO0O00O000OOO .text )#line:351
        return False #line:352
def bindWithVender (O0OOO000000OOO0OO ,O00O0OO00O00O000O ,OO0OOOOOO000OO0O0 ):#line:354
    try :#line:355
        O0OOO00OOO00O000O ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':OO0OOOOOO000OO0O0 ,'shopId':O00O0OO00O00O000O ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:364
        O0OOO0000OO0OO0OO ={'Host':'api.m.jd.com','Accept':'*/*','Sec-Fetch-Site':'same-site','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Sec-Fetch-Mode':'cors','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','User-Agent':ua ,'x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','Connection':'keep-alive','Sec-Fetch-Dest':'empty','Cookie':O0OOO000000OOO0OO }#line:381
        OO00OOOOOO000O00O =requests .request ("POST","https://api.m.jd.com/client.action",headers =O0OOO0000OO0OO0OO ,data =O0OOO00OOO00O000O ,verify =False ,timeout =10 ).text #line:382
        O00O00OOO0O0OOOOO =json .loads (OO00OOOOOO000O00O )#line:383
        if O00O00OOO0O0OOOOO ['success']:#line:384
            return O00O00OOO0O0OOOOO ['message']#line:386
    except Exception as OO0OO0OO0O00OO0O0 :#line:387
        print (f"bindWithVender Error: {OO0OOOOOO000OO0O0} {OO0OO0OO0O00OO0O0}")#line:388
def getShopOpenCardInfo (O00000OO0000O00OO ,O00O0O0O0OOO00O0O ):#line:390
    O00OOO0O0OOOO0000 =f"https://shopmember.m.jd.com/shopcard/?venderId={O00O0O0O0OOO00O0O}&channel=401&returnUrl={quote_plus(activityUrl)}"#line:391
    try :#line:392
        OO00OO00O00O00OOO ={"venderId":str (O00O0O0O0OOO00O0O ),"channel":"8019006"}#line:393
        OO00OO0OO000OOO0O =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OO00OO00O00O00OOO)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:394
        O0O0OO0O000OOOOO0 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':O00000OO0000O00OO ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':O00OOO0O0OOOO0000 ,'Accept-Encoding':'gzip, deflate'}#line:404
        O0OOO0OO0O0O00OO0 =requests .get (url =OO00OO0OO000OOO0O ,headers =O0O0OO0O000OOOOO0 ,timeout =5 ).text #line:405
        O0OOOOOO0OO00O0O0 =json .loads (O0OOO0OO0O0O00OO0 )#line:406
        if O0OOOOOO0OO00O0O0 ['success']:#line:407
            OOOO000O0O0OO00OO =O0OOOOOO0OO00O0O0 ['result']['shopMemberCardInfo']['venderCardName']#line:408
            OO000O000000O0O0O =O0OOOOOO0OO00O0O0 ['result']['userInfo']['openCardStatus']#line:409
            return OOOO000O0O0OO00OO ,OO000O000000O0O0O #line:410
        else :#line:411
            return False ,1 #line:412
    except :#line:413
        return False ,1 #line:414
if __name__ =='__main__':#line:417
    r =redis_conn ()#line:418
    try :#line:419
        cks =getCk #line:420
        if not cks :#line:421
            sys .exit ()#line:422
    except :#line:423
        print ("未获取到有效COOKIE,退出程序！")#line:424
        sys .exit ()#line:425
    global shareUserId ,inviteSuccNum ,activityUrl ,firstCk ,MSG #line:426
    inviteSuccNum =0 #line:427
    MSG =''#line:428
    title ="🗣消息提醒：lzkjInteract邀请有礼"#line:429
    if len (cks )==1 :#line:430
        shareUserId =share_userId #line:431
        activityUrl =activity_url #line:432
    else :#line:433
        try :#line:434
            shareUserId =remote_redis (f"lzkj_{activityId}",2 )#line:435
            shareUserId =shareUserId if shareUserId else ""#line:436
        except :#line:437
            shareUserId =""#line:438
        activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:439
    num =0 #line:440
    for cookie in cks [:]:#line:441
        num +=1 #line:442
        if num ==1 :#line:443
            firstCk =cookie #line:444
        if num %10 ==0 :#line:445
            print ("⏰等待5s,休息一下")#line:446
            time .sleep (5 )#line:447
        global ua ,token #line:448
        ua =userAgent ()#line:449
        try :#line:450
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:451
            pt_pin =unquote_plus (pt_pin )#line:452
        except IndexError :#line:453
            pt_pin =f'用户{num}'#line:454
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:455
        print (datetime .now ())#line:456
        result =check (cookie )#line:458
        if result ['code']!=200 :#line:459
            if num ==1 :#line:460
                print ("⚠️车头CK失效,退出程序！")#line:461
                sys .exit ()#line:462
            print (f"⚠️当前CK失效！跳过")#line:463
            time .sleep (2 )#line:464
            continue #line:465
        token =getToken (cookie ,r )#line:466
        if token is None :#line:467
            if num ==1 :#line:468
                print (f"⚠️车头获取Token失败,退出本程序！")#line:469
                sys .exit ()#line:470
            print (f"⚠️获取Token失败！⏰等待3s")#line:471
            time .sleep (3 )#line:472
            continue #line:473
        time .sleep (0.2 )#line:474
        getActivity ()#line:475
        time .sleep (0.2 )#line:476
        userInfo =getUserInfo (shareUserId )#line:477
        if not userInfo :#line:478
            if num ==1 :#line:479
                print ('⚠️无法获取userInfo，退出本程序！')#line:480
                sys .exit ()#line:481
            time .sleep (2 )#line:482
            continue #line:483
        openCardStatus =True #line:484
        followStatus =True #line:485
        shopId =userInfo ['shopId']#line:486
        openCardUrl =userInfo ['joinInfo']['openCardUrl']#line:487
        venderId =re .findall (r"venderId=(\w+)",openCardUrl )#line:488
        venderId =venderId [0 ]if venderId else ""#line:489
        Token =userInfo ['token']#line:490
        shopName =userInfo ['shopName']#line:491
        actName =userInfo ['actName']#line:492
        joinCodeInfo =userInfo ['joinInfo']['joinCodeInfo']#line:493
        joinCode =joinCodeInfo ['joinCode']#line:494
        joinDes =joinCodeInfo ['joinDes']#line:495
        print (f"🤖 {joinDes}")#line:496
        if joinCode =="1002":#line:497
            openCardStatus =False #line:498
        if joinCode =="1004":#line:499
            followStatus =False #line:500
        if joinCode =="1005":#line:501
            openCardStatus =False #line:502
            followStatus =False #line:503
        if joinCode =="1006":#line:504
            openCardStatus =False #line:505
        customerId =userInfo ['customerId']#line:506
        time .sleep (0.1 )#line:507
        if not followStatus :#line:508
            followShop (Token )#line:509
            time .sleep (0.1 )#line:510
        guestMyself (Token ,shareUserId )#line:511
        time .sleep (0.2 )#line:512
        if not followStatus and num ==1 :#line:513
            userInfo =getUserInfo (shareUserId )#line:514
            if not userInfo :#line:515
                print ('⚠️无法获取userInfo，退出本程序！')#line:516
                sys .exit ()#line:517
            Token =userInfo ['token']#line:518
        time .sleep (0.2 )#line:519
        if num ==1 :#line:520
            print (f"✅ 开启【{actName}】活动")#line:521
            print (f"店铺名称：{shopName} {shopId}")#line:522
            MSG +=f'✅账号[{pt_pin}] 开启{actName}活动\n📝活动地址 {activityUrl.split("&shareUserId=")[0]}\n'#line:523
            if shareUserId :#line:524
                print (f"CK1准备助力【{shareUserId}】")#line:525
            else :#line:526
                print (f"未填写助力码,CK1准备助力💨")#line:527
            if "不是会员无法参加"not in joinCodeInfo ['joinDes']and "需加入会员"not in joinCodeInfo ['joinDes']:#line:528
                print ("已经是会员,助力失败！")#line:529
                joinCheck (Token )#line:530
                time .sleep (0.2 )#line:531
                inviteNum =getMember (Token ,shareUserId )#line:532
                time .sleep (0.2 )#line:533
                inviteSuccNum =inviteNum #line:534
                if jd_lzkjInteractNum :#line:535
                    jd_lzkjInteractNum =int (jd_lzkjInteractNum )#line:536
                    print (f"🧑‍🤝‍🧑CK1已邀请{inviteNum}人,当前已设置最大邀请人数{jd_lzkjInteractNum}人")#line:537
                else :#line:538
                    jd_lzkjInteractNum =0 #line:539
                    print (f"🧑‍🤝‍🧑CK1已邀请{inviteNum}人")#line:540
                time .sleep (0.2 )#line:541
                prizeListResponse =prizeList (Token )#line:542
                prizeListRecord =[]#line:543
                prizeNameList =[]#line:544
                try :#line:545
                    for prizeitem in prizeListResponse ['data']['prizeInfo']:#line:546
                        print (f"🎁 奖品: {prizeitem['prizeName']}, 助力人数: {prizeitem['days']}, 最大助力人数: {prizeitem['winNumberDay']}, 总数：{prizeitem['allNum']}, 剩余：{prizeitem['leftNum']}, ID: {prizeitem['id']}")#line:547
                        prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},助力人数:{prizeitem['days']},最大助力人数: {prizeitem['winNumberDay']},总数:{prizeitem['allNum']},剩余:{prizeitem['leftNum']}\n")#line:548
                        if prizeitem ['leftNum']>0 :#line:549
                            prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['days'],prizeitem ['id'],prizeitem ['winNumberDay']))#line:550
                    MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"#line:551
                except :#line:552
                    print ('⚠️无法获取奖品列表, 退出本程序！')#line:553
                    sys .exit ()#line:554
                if prizeListRecord ==[]:#line:555
                    print ('⚠️无奖品可领,退出本程序！')#line:556
                    sys .exit ()#line:557
                for prizeinfo in prizeListRecord :#line:558
                    if inviteSuccNum >=prizeinfo [1 ]:#line:559
                        print (f'已达到领取条件,开始领取 {prizeinfo[0]}')#line:560
                        receive_result =receiveAcquire (Token ,prizeinfo [2 ])#line:561
                        if receive_result ==0 :#line:562
                            print (f'🎉🎉 领取奖励成功')#line:563
                            MSG +=f"🎉成功领取 {prizeinfo[0]}\n"#line:564
                        elif receive_result ==60002 :#line:565
                            print (f'🎉🎉 奖励已经领取过')#line:566
                            MSG +=f"🎉已经领取过 {prizeinfo[0]}\n"#line:567
                        elif receive_result ==60009 :#line:568
                            print (f'🎉🎉 奖励已经领取过其他奖励或未达到领取标准建议手动领取！')#line:569
                            MSG +=f"🎉奖励已经领取过其他奖励或未达到领取标准建议手动领取 {prizeinfo[0]}\n"#line:570
                        else :#line:571
                            print (f'💥💥 领取奖励失败')#line:572
                            MSG +=f"💥💥 领取奖励失败 {prizeinfo[0]}\n"#line:573
                    time .sleep (1.5 )#line:574
                if inviteSuccNum >=prizeListRecord [-1 ][1 ]and inviteSuccNum >=jd_lzkjInteractNum :#line:575
                    print ("奖励已领完")#line:576
                    MSG +=f"🤖奖励已领完\n"#line:577
                    if len (cks )>1 :#line:578
                        send (title ,MSG )#line:579
                    sys .exit ()#line:580
                actorUuid =getUserId (Token )#line:581
                time .sleep (0.1 )#line:582
                if not actorUuid :#line:583
                    if num ==1 :#line:584
                        print (f'⚠️车头无法获取邀请码, 退出本程序！')#line:585
                        sys .exit ()#line:586
                print (f"\n后面账号全部助力 {actorUuid}")#line:587
                shareUserId =actorUuid #line:588
                activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:589
                continue #line:590
            else :#line:591
                inviteSuccNum =0 #line:592
        if "不是会员无法参加"in joinCodeInfo ['joinDes']or "需加入会员"in joinCodeInfo ['joinDes']:#line:594
            print (f"未开卡 现在去开卡")#line:595
            open_result =bindWithVender (cookie ,shopId ,venderId )#line:596
            if open_result is not None :#line:597
                if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:598
                    print (f"\t💥💥 {open_result}\n‼️助力失败")#line:599
                    continue #line:600
                else :#line:601
                    print (f"\t🎉🎉 {open_result}")#line:602
                    if num !=1 :#line:603
                        inviteSuccNum +=1 #line:604
                        print (f"🛳已经邀请{inviteSuccNum}人")#line:605
                    time .sleep (0.1 )#line:606
                    joinCheck (Token )#line:607
                    time .sleep (0.1 )#line:608
                    getMember (Token ,shareUserId )#line:609
                    time .sleep (0.1 )#line:610
                    prizeListResponse =prizeList (Token )#line:611
                    prizeListRecord =[]#line:612
                    prizeNameList =[]#line:613
                    try :#line:614
                        for prizeitem in prizeListResponse ['data']['prizeInfo']:#line:615
                            if num ==1 :#line:616
                                print (f"🎁 奖品: {prizeitem['prizeName']}, 助力人数: {prizeitem['days']}, 最大助力人数: {prizeitem['winNumberDay']}, 总数：{prizeitem['allNum']}, 剩余：{prizeitem['leftNum']}, ID: {prizeitem['id']}")#line:617
                                prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},助力人数:{prizeitem['days']},最大助力人数: {prizeitem['winNumberDay']},总数:{prizeitem['allNum']},剩余:{prizeitem['leftNum']}\n")#line:618
                            if prizeitem ['leftNum']>0 :#line:619
                                prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['days'],prizeitem ['id'],prizeitem ['winNumberDay']))#line:620
                        if prizeNameList :#line:621
                            MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"#line:622
                            print (f"‼️该活动部分有且仅能领取一次奖励,默认自动领最高档豆🎁,或者手动领取\n")#line:623
                    except :#line:624
                        print ('⚠️无法获取奖品列表, 退出本程序！')#line:625
                        sys .exit ()#line:626
                    if prizeListRecord ==[]:#line:627
                        print ('⚠️无奖品可领, 退出本程序！')#line:628
                        sys .exit ()#line:629
                    for prizeinfo in prizeListRecord [:]:#line:630
                        if inviteSuccNum ==prizeinfo [1 ]:#line:631
                            print (f'\nCK1已达到领取条件, 开始领取 {prizeinfo[0]}')#line:632
                            time .sleep (0.2 )#line:633
                            token =getToken (firstCk ,r )#line:634
                            time .sleep (0.2 )#line:635
                            getActivity ()#line:636
                            time .sleep (0.2 )#line:637
                            Token0 =getUserInfo (shareUserId )['token']#line:638
                            receive_result =receiveAcquire (Token0 ,prizeinfo [2 ])#line:639
                            if receive_result ==0 :#line:640
                                print (f'🎉🎉 领取奖励成功')#line:641
                                MSG +=f"🎉成功领取 {prizeinfo[0]}\n"#line:642
                            elif receive_result ==60002 :#line:643
                                print (f'🎉🎉 奖励已经领取过')#line:644
                                MSG +=f"🎉已经领取过 {prizeinfo[0]}\n"#line:645
                            elif receive_result ==60009 :#line:646
                                print (f'🎉🎉 奖励已经领取过其他奖励或未达到领取标准建议手动领取！')#line:647
                                MSG +=f"🎉奖励已经领取过其他奖励或未达到领取标准建议手动领取 {prizeinfo[0]}\n"#line:648
                            else :#line:649
                                print (f'💥💥 领取奖励失败')#line:650
                                MSG +=f"💥💥 领取奖励失败 {prizeinfo[0]}\n"#line:651
                            time .sleep (1.5 )#line:652
                    if inviteSuccNum >=prizeListRecord [-1 ][1 ]and inviteSuccNum >=jd_lzkjInteractNum :#line:653
                        print ("🤖奖励已领完")#line:654
                        MSG +=f"🤖奖励已领完\n"#line:655
                        if len (cks )>1 :#line:656
                            send (title ,MSG )#line:657
                        sys .exit ()#line:658
                    time .sleep (0.1 )#line:659
                    if num ==1 :#line:660
                        actorUuid =getUserId (Token )#line:661
                        if not actorUuid :#line:662
                            print (f'⚠️无法获取车头邀请码, 退出本程序！')#line:663
                            sys .exit ()#line:664
                        print (f"后面账号全部助力 {actorUuid}")#line:665
                        shareUserId =actorUuid #line:666
                        activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:667
        else :#line:668
            print (f"⛈已开卡,无法完成助力")#line:669
        time .sleep (2 )#line:671
