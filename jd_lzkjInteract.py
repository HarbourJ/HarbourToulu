#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_lzkjInteract.py(jd_lzkjInteract邀请有礼)
Author: HarbourJ
Date: 2022/11/24 10:00
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('jd_lzkjInteract邀请有礼');
ActivityEntry: https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType=10006&activityId=1595256546199793665&templateId=20201228083300yqrhyl011&nodeId=101001005&prd=cjwx

Description: 邀请xx人xx豆,自动助力,自动领奖
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
share_userId =os .environ .get ("jd_lzkjInteractUserId")if os .environ .get ("jd_lzkjInteractUserId")else ""#line:26
if "lzkj-isv.isvjcloud.com/prod/cc/interactsaas"not in jd_lzkjInteractUrl :#line:28
    print ("⛈暂不支持变量设置的活动类型,请检查后重试！仅支持interactsaas类型活动")#line:29
    sys .exit ()#line:30
templateId =re .findall (r"templateId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:31
activityId =re .findall (r"activityId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:32
activityType =re .findall (r"activityType=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:33
activity_url =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&activityId={activityId}&shareUserId={share_userId}&templateId={templateId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:35
print (f"【🛳活动入口】https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}")#line:37
def redis_conn ():#line:39
    try :#line:40
        import redis #line:41
        try :#line:42
            O00O000O0O0OO00O0 =redis .ConnectionPool (host =redis_url ,port =6379 ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:43
            O0OOOO0OOO00OO0O0 =redis .Redis (connection_pool =O00O000O0O0OO00O0 )#line:44
            O0OOOO0OOO00OO0O0 .get ('conn_test')#line:45
            print ('✅redis连接成功')#line:46
            return O0OOOO0OOO00OO0O0 #line:47
        except :#line:48
            print ("⚠️redis连接异常")#line:49
    except :#line:50
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:51
        sys .exit ()#line:52
def getToken (OOOOOOOOOOO0O0OOO ,r =None ):#line:54
    O00O00OO00O00O0O0 =f'{activityUrl.split("com/")[0]}com'#line:55
    try :#line:56
        O000O000O0O0O0O00 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OOOOOOOOOOO0O0OOO )[0 ])#line:57
    except :#line:58
        O000O000O0O0O0O00 =OOOOOOOOOOO0O0OOO [:15 ]#line:59
    try :#line:60
        try :#line:61
            OOO000OO0O0000OOO =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{O000O000O0O0O0O00}')#line:62
        except Exception as OOO000OO0O0O0OOOO :#line:63
            OOO000OO0O0000OOO =None #line:64
        if OOO000OO0O0000OOO is not None :#line:65
            print (f"♻️获取缓存Token")#line:66
            return OOO000OO0O0000OOO #line:67
        else :#line:68
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OOOOOOOOOOO0O0OOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:79
            sign ({"url":f"{O00O00OO00O00O0O0}","id":""},'isvObfuscator')#line:80
            OO0O00OOO000OO000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:81
            if OO0O00OOO000OO000 .status_code !=200 :#line:82
                print (OO0O00OOO000OO000 .status_code )#line:83
                return #line:84
            else :#line:85
                if "参数异常"in OO0O00OOO000OO000 .text :#line:86
                    print (OO0O00OOO000OO000 .text )#line:87
                    return #line:88
            O0OOOO0OO0000O0O0 =OO0O00OOO000OO000 .json ()['token']#line:89
            try :#line:90
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{O000O000O0O0O0O00}',O0OOOO0OO0000O0O0 ,ex =1800 ):#line:91
                    print ("✅Token缓存成功")#line:92
                else :#line:93
                    print ("❌Token缓存失败")#line:94
            except Exception as OOO000OO0O0O0OOOO :#line:95
                print (f"✅获取实时Token")#line:96
            return O0OOOO0OO0000O0O0 #line:97
    except Exception as OOO000OO0O0O0OOOO :#line:98
        print (f"Token error: {str(OOO000OO0O0O0OOOO)}")#line:99
        return #line:100
def getJdTime ():#line:102
    OOOO000O0OO00000O =int (round (time .time ()*1000 ))#line:103
    return OOOO000O0OO00000O #line:104
def randomString (O000OO0OOO0O0OOOO ,flag =False ):#line:106
    O000O00OOO000O000 ="0123456789abcdef"#line:107
    if flag :O000O00OOO000O000 =O000O00OOO000O000 .upper ()#line:108
    OOOOO0000O00O0000 =[random .choice (O000O00OOO000O000 )for _OOO00O000000OO000 in range (O000OO0OOO0O0OOOO )]#line:109
    return ''.join (OOOOO0000O00O0000 )#line:110
def check (O0OO00O000OO0O0O0 ):#line:112
    try :#line:113
        OOOO0OO0OO0O000OO ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:114
        OO0O00O00OOO0OO00 ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":O0OO00O000OO0O0O0 ,"User-Agent":ua ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:124
        OO0OO0O0OOOO0O000 =requests .get (url =OOOO0OO0OO0O000OO ,headers =OO0O00O00OOO0OO00 ).text #line:125
        OO0OOOO00O0OOO000 =json .loads (OO0OO0O0OOOO0O000 )#line:126
        if OO0OOOO00O0OOO000 ['retcode']=='1001':#line:127
            OO00OO0000OOO000O ="当前ck已失效，请检查"#line:128
            return {'code':1001 ,'data':OO00OO0000OOO000O }#line:129
        elif OO0OOOO00O0OOO000 ['retcode']=='0'and 'userInfo'in OO0OOOO00O0OOO000 ['data']:#line:130
            O00OO0O0O0OO00O00 =OO0OOOO00O0OOO000 ['data']['userInfo']['baseInfo']['nickname']#line:131
            return {'code':200 ,'name':O00OO0O0O0OO00O00 ,'ck':cookie }#line:132
    except Exception as O00OO0O0OOO0O0O0O :#line:133
        return {'code':0 ,'data':O00OO0O0OOO0O0O0O }#line:134
def getActivity ():#line:136
    OO000OOOOOO0OOOOO =activityUrl #line:137
    O0OO00OOOOOO0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:145
    O000OO00OOO0OO0OO =requests .request ("GET",OO000OOOOOO0OOOOO ,headers =O0OO00OOOOOO0O0OO )#line:146
    if O000OO00OOO0OO0OO .status_code !=200 :#line:147
        print (O000OO00OOO0OO0OO .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:148
        sys .exit ()#line:149
def followShop (O000O000OOOOO0OOO ):#line:151
    O0OO0O000O0OOOOOO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followShop/follow"#line:152
    OO0O00O00O000O0OO ={}#line:153
    O0000O0000000O000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O000O000OOOOO0OOO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:165
    OO00O000OO0OOOOO0 =requests .post (O0OO0O000O0OOOOOO ,headers =O0000O0000000O000 ,data =json .dumps (OO0O00O00O000O0OO ))#line:166
    try :#line:167
        return OO00O000OO0OOOOO0 .json ()#line:168
    except :#line:169
        return False #line:170
def getUserInfo (OO0O0000000O00OO0 ):#line:172
    OOO000O0OOOOOO00O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login"#line:173
    OOO0OOOO0OOOOO00O ={"status":"0","activityId":activityId ,"source":"01","tokenPin":token ,"shareUserId":OO0O0000000O00OO0 }#line:180
    OOOOO00O0000O0OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':'','Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};'}#line:193
    OOOO00O00OOO000O0 =requests .request ("POST",OOO000O0OOOOOO00O ,headers =OOOOO00O0000O0OO0 ,data =json .dumps (OOO0OOOO0OOOOO00O ))#line:194
    if OOOO00O00OOO000O0 .status_code ==200 :#line:195
        OO0OO00OO00OOO00O =OOOO00O00OOO000O0 .json ()#line:196
        if OO0OO00OO00OOO00O ['data']:#line:197
            return OO0OO00OO00OOO00O ['data']#line:198
        else :#line:199
            print (OO0OO00OO00OOO00O )#line:200
    else :#line:201
        print (OOOO00O00OOO000O0 .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:202
        sys .exit ()#line:203
def guestMyself (O0000O0O00O0000O0 ,OOOOOO000OOOO0O00 ):#line:205
    OOO00O0OO0OO00OO0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/bargain/guest/myself"#line:206
    O0OO0000OOOOOO00O ={"shareUserId":OOOOOO000OOOO0O00 }#line:209
    O00OO0OO00OO0O0O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0000O0O00O0000O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:221
    requests .post (OOO00O0OO0OO00OO0 ,headers =O00OO0OO00OO0O0O0 ,data =json .dumps (O0OO0000OOOOOO00O ))#line:222
def getMember (O000OOO0O00O0O0OO ,OO000OO000OOOO0OO ):#line:224
    O0O0O0OOOOO000OOO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/getMember"#line:225
    OOOOOO000OO0OOO00 ={"shareUserId":OO000OO000OOOO0OO }#line:228
    O0000OOOOOO000000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O000OOO0O00O0O0OO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:240
    O000O0O00000OO000 =requests .post (O0O0O0OOOOO000OOO ,headers =O0000OOOOOO000000 ,data =json .dumps (OOOOOO000OO0OOO00 ))#line:241
    try :#line:242
        O00O00000O0O0O00O =O000O0O00000OO000 .json ()#line:243
        O0O0OOO00O0O0O00O =O00O00000O0O0O00O ['data']['shareUser']#line:244
        return O0O0OOO00O0O0O00O #line:245
    except Exception as OOO000OO00O00O000 :#line:246
        print (str (OOO000OO00O00O000 ))#line:247
        return False #line:248
def prizeList (OO0O0O0OOO000OOO0 ):#line:250
    OO00OOOOO0OOOOOO0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/prizeList"#line:251
    O0OO000000O0OOOO0 ={}#line:252
    OOOOO00OO0O0O0OOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO0O0O0OOO000OOO0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:264
    O00000000OOO00000 =requests .post (OO00OOOOO0OOOOOO0 ,headers =OOOOO00OO0O0O0OOO ,data =json .dumps (O0OO000000O0OOOO0 ))#line:265
    try :#line:266
        return O00000000OOO00000 .json ()#line:267
    except :#line:268
        return False #line:269
def joinCheck (O0OOOO0O00O00O000 ):#line:271
    OO00000OOO00000OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/join/check"#line:272
    O0O0O0O00OO0OO00O ={"status":"0"}#line:275
    OO00O000O0OO0O000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0OOOO0O00O00O000 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:287
    O0000OOO00O00O00O =requests .post (OO00000OOO00000OO ,headers =OO00O000O0OO0O000 ,data =json .dumps (O0O0O0O00OO0OO00O ))#line:288
    try :#line:289
        return O0000OOO00O00O00O .json ()#line:290
    except :#line:291
        return False #line:292
def getUserId (O0O0O000OO0O00OOO ):#line:294
    OOOOOO0OOOO0OO0O0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/share/getUserId"#line:295
    O00OOOO000OOO0000 ={}#line:296
    OO0O00000OOOO00OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0O0O000OO0O00OOO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:308
    O00OO000OO0O0OOOO =requests .post (OOOOOO0OOOO0OO0O0 ,headers =OO0O00000OOOO00OO ,data =json .dumps (O00OOOO000OOO0000 ))#line:309
    try :#line:310
        return O00OO000OO0O0OOOO .json ()['data']['shareUserId']#line:311
    except Exception as O0000OO0OOOO000O0 :#line:312
        print (str (O0000OO0OOOO000O0 ))#line:313
def receiveAcquire (OO000O000OOO0OO00 ,O0000000OOO00O000 ):#line:315
    O0OO0O0O0OO00O000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/receive/acquire"#line:316
    OO0000OO00OOO00OO ={"prizeInfoId":O0000000OOO00O000 ,"status":1 }#line:320
    OOO0000OOOOO00000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO000O000OOO0OO00 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:332
    OOOO0OOOOOO000O00 =requests .post (O0OO0O0O0OO00O000 ,headers =OOO0000OOOOO00000 ,data =json .dumps (OO0000OO00OOO00OO ))#line:333
    try :#line:334
        return OOOO0OOOOOO000O00 .json ()['resp_code']#line:335
    except :#line:336
        print (OOOO0OOOOOO000O00 .text )#line:337
        return False #line:338
def bindWithVender (O0OOOO0OO0O0OOOOO ,O0000O0O00000O0OO ,OOO00OO0O00O0OOO0 ):#line:340
    try :#line:341
        O00000000O000OOOO ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':OOO00OO0O00O0OOO0 ,'shopId':O0000O0O00000O0OO ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:350
        O0O000OOOO0O00O00 ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':O0OOOO0OO0O0OOOOO }#line:363
        O0O00O0OOO000OOOO =requests .request ("POST","https://api.m.jd.com/",headers =O0O000OOOO0O00O00 ,data =O00000000O000OOOO ,timeout =10 ).text #line:364
        OOOO0O0OOO0O0OO00 =json .loads (O0O00O0OOO000OOOO )#line:365
        if OOOO0O0OOO0O0OO00 ['success']:#line:366
            return OOOO0O0OOO0O0OO00 ['message']#line:367
    except Exception as OOOO000O000O00OO0 :#line:368
        print (f"bindWithVender Error: {OOO00OO0O00O0OOO0} {OOOO000O000O00OO0}")#line:369
def getShopOpenCardInfo (OO0O000O00OO00OOO ,OO0OO00O0O0O0O0O0 ):#line:371
    OOOO0O00000OO0OO0 =f"https://shopmember.m.jd.com/shopcard/?venderId={OO0OO00O0O0O0O0O0}&channel=401&returnUrl={quote_plus(activityUrl)}"#line:372
    try :#line:373
        OOO0O000OO00O0O0O ={"venderId":str (OO0OO00O0O0O0O0O0 ),"channel":"8019006"}#line:374
        OOO00O000OOO0OO0O =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OOO0O000OO00O0O0O)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:375
        O0OO00OOO00000O00 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OO0O000O00OO00OOO ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':OOOO0O00000OO0OO0 ,'Accept-Encoding':'gzip, deflate'}#line:385
        O0OO00OOO000OOOO0 =requests .get (url =OOO00O000OOO0OO0O ,headers =O0OO00OOO00000O00 ,timeout =5 ).text #line:386
        O0O0000OOOO0OO00O =json .loads (O0OO00OOO000OOOO0 )#line:387
        if O0O0000OOOO0OO00O ['success']:#line:388
            OO00O0O0O0OOOO00O =O0O0000OOOO0OO00O ['result']['shopMemberCardInfo']['venderCardName']#line:389
            OOOO00OO0OO000OO0 =O0O0000OOOO0OO00O ['result']['userInfo']['openCardStatus']#line:390
            return OO00O0O0O0OOOO00O ,OOOO00OO0OO000OO0 #line:391
        else :#line:392
            return False ,1 #line:393
    except :#line:394
        return False ,1 #line:395
if __name__ =='__main__':#line:398
    r =redis_conn ()#line:399
    try :#line:400
        cks =getCk #line:401
        if not cks :#line:402
            sys .exit ()#line:403
    except :#line:404
        print ("未获取到有效COOKIE,退出程序！")#line:405
        sys .exit ()#line:406
    global shareUserId ,inviteSuccNum ,activityUrl ,firstCk ,MSG #line:407
    inviteSuccNum =0 #line:408
    MSG =''#line:409
    title ="🗣消息提醒：lzkjInteract邀请有礼"#line:410
    if len (cks )==1 :#line:411
        shareUserId =share_userId #line:412
        activityUrl =activity_url #line:413
    else :#line:414
        try :#line:415
            shareUserId =remote_redis (f"lzkj_{activityId}",2 )#line:416
            shareUserId =shareUserId if shareUserId else ""#line:417
        except :#line:418
            shareUserId =""#line:419
        activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:420
    num =0 #line:421
    for cookie in cks [:]:#line:422
        num +=1 #line:423
        if num ==1 :#line:424
            firstCk =cookie #line:425
        if num %5 ==0 :#line:426
            print ("⏰等待5s,休息一下")#line:427
            time .sleep (5 )#line:428
        global ua ,token #line:429
        ua =userAgent ()#line:430
        try :#line:431
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:432
            pt_pin =unquote_plus (pt_pin )#line:433
        except IndexError :#line:434
            pt_pin =f'用户{num}'#line:435
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:436
        print (datetime .now ())#line:437
        result =check (cookie )#line:439
        if result ['code']!=200 :#line:440
            if num ==1 :#line:441
                print ("⚠️车头CK失效,退出程序！")#line:442
                sys .exit ()#line:443
            print (f"⚠️当前CK失效！跳过")#line:444
            continue #line:445
        token =getToken (cookie ,r )#line:446
        if token is None :#line:447
            if num ==1 :#line:448
                print (f"⚠️车头获取Token失败,退出本程序！")#line:449
                sys .exit ()#line:450
            print (f"⚠️获取Token失败！⏰等待3s")#line:451
            time .sleep (3 )#line:452
            continue #line:453
        time .sleep (0.5 )#line:454
        getActivity ()#line:455
        time .sleep (0.5 )#line:456
        userInfo =getUserInfo (shareUserId )#line:457
        if not userInfo :#line:458
            if num ==1 :#line:459
                print ('⚠️无法获取userInfo，退出本程序！')#line:460
                sys .exit ()#line:461
            time .sleep (2 )#line:462
            continue #line:463
        shopId =userInfo ['shopId']#line:464
        openCardUrl =userInfo ['joinInfo']['openCardUrl']#line:465
        venderId =re .findall (r"venderId=(\w+)",openCardUrl )#line:466
        venderId =venderId [0 ]if venderId else ""#line:467
        Token =userInfo ['token']#line:468
        shopName =userInfo ['shopName']#line:469
        actName =userInfo ['actName']#line:470
        joinCodeInfo =userInfo ['joinInfo']['joinCodeInfo']#line:471
        customerId =userInfo ['customerId']#line:472
        time .sleep (0.3 )#line:473
        followShop (Token )#line:474
        time .sleep (0.3 )#line:475
        guestMyself (Token ,shareUserId )#line:476
        time .sleep (0.3 )#line:477
        if num ==1 :#line:479
            print (f"✅ 开启【{actName}】活动")#line:480
            print (f"店铺名称：{shopName} {shopId}")#line:481
            MSG +=f'✅账号[{pt_pin}] 开启{actName}活动\n📝活动地址 {activityUrl.split("&shareUserId=")[0]}\n'#line:482
            if shareUserId :#line:483
                print (f"CK1准备助力【{shareUserId}】")#line:484
            else :#line:485
                print (f"未填写助力码,CK1准备助力💨")#line:486
            if "不是会员无法参加"not in joinCodeInfo ['joinDes']and "需加入会员"not in joinCodeInfo ['joinDes']:#line:487
                print ("已经是会员,助力失败！")#line:488
                joinCheck (Token )#line:489
                time .sleep (0.2 )#line:490
                inviteNum =getMember (Token ,shareUserId )#line:491
                time .sleep (0.2 )#line:492
                inviteSuccNum =inviteNum #line:493
                print (f"🧑‍🤝‍🧑 CK1已邀请{inviteNum}人\n")#line:494
                time .sleep (0.2 )#line:495
                prizeListResponse =prizeList (Token )#line:496
                prizeListRecord =[]#line:497
                prizeNameList =[]#line:498
                try :#line:499
                    for prizeitem in prizeListResponse ['data']['prizeInfo']:#line:500
                        print (f"🎁 奖品: {prizeitem['prizeName']}, 助力人数: {prizeitem['days']}, 总数：{prizeitem['allNum']}, 剩余：{prizeitem['leftNum']}, ID: {prizeitem['id']}")#line:501
                        prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},助力人数:{prizeitem['days']},总数:{prizeitem['allNum']},剩余:{prizeitem['leftNum']}\n")#line:502
                        if prizeitem ['leftNum']>0 :#line:503
                            prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['days'],prizeitem ['id']))#line:504
                    MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"#line:505
                except :#line:506
                    print ('⚠️无法获取奖品列表, 退出本程序！')#line:507
                    sys .exit ()#line:508
                if prizeListRecord ==[]:#line:509
                    print ('⚠️无奖品可领,退出本程序！')#line:510
                    sys .exit ()#line:511
                for prizeinfo in prizeListRecord :#line:512
                    if inviteSuccNum >=prizeinfo [1 ]:#line:513
                        print (f'已达到领取条件,开始领取 {prizeinfo[0]}')#line:514
                        receive_result =receiveAcquire (Token ,prizeinfo [2 ])#line:515
                        if receive_result ==0 :#line:516
                            print (f'🎉🎉 领取奖励成功')#line:517
                            MSG +=f"🎉成功领取 {prizeinfo[0]}\n"#line:518
                        elif receive_result ==60002 :#line:519
                            print (f'🎉🎉 奖励已经领取过')#line:520
                            MSG +=f"🎉已经领取过 {prizeinfo[0]}\n"#line:521
                        elif receive_result ==60009 :#line:522
                            print (f'🎉🎉 奖励已经领取过其他奖励或未达到领取标准建议手动领取！')#line:523
                            MSG +=f"🎉奖励已经领取过其他奖励或未达到领取标准建议手动领取 {prizeinfo[0]}\n"#line:524
                        else :#line:525
                            print (f'💥💥 领取奖励失败')#line:526
                            MSG +=f"💥💥 领取奖励失败 {prizeinfo[0]}\n"#line:527
                    time .sleep (1.5 )#line:528
                if inviteSuccNum >=prizeListRecord [-1 ][1 ]:#line:529
                    print ("奖励已领完")#line:530
                    MSG +=f"🤖奖励已领完\n"#line:531
                    if len (cks )>1 :#line:532
                        send (title ,MSG )#line:533
                    sys .exit ()#line:534
                actorUuid =getUserId (Token )#line:535
                time .sleep (0.3 )#line:536
                if not actorUuid :#line:537
                    if num ==1 :#line:538
                        print (f'⚠️ 无法获取车头邀请码, 退出本程序！')#line:539
                        sys .exit ()#line:540
                print (f"\n后面账号全部助力 {actorUuid}")#line:541
                shareUserId =actorUuid #line:542
                activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:543
                continue #line:544
            else :#line:545
                inviteSuccNum =0 #line:546
        if "不是会员无法参加"in joinCodeInfo ['joinDes']or "需加入会员"in joinCodeInfo ['joinDes']:#line:548
            print (f"未开卡 现在去开卡")#line:549
            open_result =bindWithVender (cookie ,shopId ,venderId )#line:550
            if open_result is not None :#line:551
                if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:552
                    print (f"\t💥💥 {open_result}\n‼️助力失败")#line:553
                    continue #line:554
                else :#line:555
                    print (f"\t🎉🎉 {open_result}")#line:556
                    if num !=1 :#line:557
                        inviteSuccNum +=1 #line:558
                        print (f"🛳已经邀请{inviteSuccNum}人")#line:559
                    time .sleep (0.3 )#line:560
                    joinCheck (Token )#line:561
                    time .sleep (0.3 )#line:562
                    getMember (Token ,shareUserId )#line:563
                    time .sleep (0.3 )#line:564
                    prizeListResponse =prizeList (Token )#line:565
                    prizeListRecord =[]#line:566
                    prizeNameList =[]#line:567
                    try :#line:568
                        for prizeitem in prizeListResponse ['data']['prizeInfo']:#line:569
                            if num ==1 :#line:570
                                print (f"🎁 奖品: {prizeitem['prizeName']}, 助力人数: {prizeitem['days']}, 总数：{prizeitem['allNum']}, 剩余：{prizeitem['leftNum']}, ID: {prizeitem['id']}")#line:571
                                prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},助力人数:{prizeitem['days']},总数:{prizeitem['allNum']},剩余:{prizeitem['leftNum']}\n")#line:572
                            if prizeitem ['leftNum']>0 :#line:573
                                prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['days'],prizeitem ['id']))#line:574
                        if prizeNameList :#line:575
                            MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"#line:576
                            print (f"‼️该活动部分有且仅能领取一次奖励,默认自动领最高档豆🎁,或者手动领取\n")#line:577
                    except :#line:578
                        print ('⚠️无法获取奖品列表, 退出本程序！')#line:579
                        sys .exit ()#line:580
                    if prizeListRecord ==[]:#line:581
                        print ('⚠️无奖品可领, 退出本程序！')#line:582
                        sys .exit ()#line:583
                    for prizeinfo in prizeListRecord [:]:#line:584
                        if inviteSuccNum ==prizeinfo [1 ]:#line:585
                            print (f'CK1已达到领取条件, 开始领取 {prizeinfo[0]}')#line:586
                            time .sleep (0.2 )#line:587
                            token =getToken (firstCk ,r )#line:588
                            time .sleep (0.2 )#line:589
                            getActivity ()#line:590
                            time .sleep (0.2 )#line:591
                            Token0 =getUserInfo (shareUserId )['token']#line:592
                            receive_result =receiveAcquire (Token0 ,prizeinfo [2 ])#line:593
                            if receive_result ==0 :#line:594
                                print (f'🎉🎉 领取奖励成功')#line:595
                                MSG +=f"🎉成功领取 {prizeinfo[0]}\n"#line:596
                            elif receive_result ==60002 :#line:597
                                print (f'🎉🎉 奖励已经领取过')#line:598
                                MSG +=f"🎉已经领取过 {prizeinfo[0]}\n"#line:599
                            elif receive_result ==60009 :#line:600
                                print (f'🎉🎉 奖励已经领取过其他奖励或未达到领取标准建议手动领取！')#line:601
                                MSG +=f"🎉奖励已经领取过其他奖励或未达到领取标准建议手动领取 {prizeinfo[0]}\n"#line:602
                            else :#line:603
                                print (f'💥💥 领取奖励失败')#line:604
                                MSG +=f"💥💥 领取奖励失败 {prizeinfo[0]}\n"#line:605
                            time .sleep (1.5 )#line:606
                    if inviteSuccNum >=prizeListRecord [-1 ][1 ]:#line:607
                        print ("🤖奖励已领完")#line:608
                        MSG +=f"🤖奖励已领完\n"#line:609
                        if len (cks )>1 :#line:610
                            send (title ,MSG )#line:611
                        sys .exit ()#line:612
                    time .sleep (0.3 )#line:613
                    if num ==1 :#line:614
                        actorUuid =getUserId (Token )#line:615
                        if not actorUuid :#line:616
                            print (f'⚠️无法获取车头邀请码, 退出本程序！')#line:617
                            sys .exit ()#line:618
                        print (f"后面账号全部助力 {actorUuid}")#line:619
                        shareUserId =actorUuid #line:620
                        activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}&shareUserId={shareUserId}&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:621
        else :#line:622
            print (f"⛈已开卡,无法完成助力")#line:623
        time .sleep (2 )
