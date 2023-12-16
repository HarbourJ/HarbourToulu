#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_lzkjInteractAddCart.py(jd_lzkjInteract加购有礼)
Author: HarbourJ
Date: 2022/11/24 10:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('jd_lzkjInteract加购有礼');
ActivityEntry: https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType=10024&activityId=1651947388458172418&templateId=20210518190900jgyl011&nodeId=101001&prd=null

Description: 加购xx商品xx豆,自动领奖
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
jd_lzkjInteractUrl =os .environ .get ("jd_lzkjInteractAddCartUrl")if os .environ .get ("jd_lzkjInteractAddCartUrl")else ""#line:25
share_userId =os .environ .get ("jd_lzkjInteractUserId")if os .environ .get ("jd_lzkjInteractUserId")else ""#line:26
runNums =os .environ .get ("jd_lzkjInteractAddRunNums")if os .environ .get ("jd_lzkjInteractAddRunNums")else 12 #line:27
if "lzkj-isv.isvjcloud.com/prod/cc/interactsaas"not in jd_lzkjInteractUrl :#line:29
    print ("⛈暂不支持变量设置的活动类型,请检查后重试！仅支持interactsaas类型活动")#line:30
    sys .exit ()#line:31
templateId =re .findall (r"templateId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:32
activityId =re .findall (r"activityId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:33
activityType =re .findall (r"activityType=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:34
print (f"【🛳活动入口】https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}")#line:36
runNums =int (runNums )#line:38
if runNums ==12 :#line:39
    print ('🤖本次加购默认跑前12个账号,设置自定义变量:export jd_lzkjInteractAddRunNums="需要运行加购的ck数量"')#line:40
else :#line:41
    print (f'🤖本次运行前{runNums}个账号')#line:42
def redis_conn ():#line:44
    try :#line:45
        import redis #line:46
        try :#line:47
            O0O00000OOO000OO0 =redis .ConnectionPool (host =redis_url ,port =6379 ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:48
            O0O000OO0O00O0000 =redis .Redis (connection_pool =O0O00000OOO000OO0 )#line:49
            O0O000OO0O00O0000 .get ('conn_test')#line:50
            print ('✅redis连接成功')#line:51
            return O0O000OO0O00O0000 #line:52
        except :#line:53
            print ("⚠️redis连接异常")#line:54
    except :#line:55
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:56
        sys .exit ()#line:57
def getToken (O0OO0O000O0OO000O ,r =None ):#line:59
    O0O0OOOOO0O0O0000 =f'{activityUrl.split("com/")[0]}com'#line:60
    try :#line:61
        O0OOO000O000O000O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0OO0O000O0OO000O )[0 ])#line:62
    except :#line:63
        O0OOO000O000O000O =O0OO0O000O0OO000O [:15 ]#line:64
    try :#line:65
        try :#line:66
            O0O00OOOOOOO000O0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0OOO000O000O000O}')#line:67
        except Exception as OO0OO0O00000000OO :#line:68
            O0O00OOOOOOO000O0 =None #line:69
        if O0O00OOOOOOO000O0 is not None :#line:70
            print (f"♻️获取缓存Token")#line:71
            return O0O00OOOOOOO000O0 #line:72
        else :#line:73
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0OO0O000O0OO000O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:84
            sign ({"url":f"{O0O0OOOOO0O0O0000}","id":""},'isvObfuscator')#line:85
            OO0OOOOO000O00000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:86
            if OO0OOOOO000O00000 .status_code !=200 :#line:87
                print (OO0OOOOO000O00000 .status_code )#line:88
                return #line:89
            else :#line:90
                if "参数异常"in OO0OOOOO000O00000 .text :#line:91
                    print (OO0OOOOO000O00000 .text )#line:92
                    return #line:93
            OOO0OOOOO000OO0O0 =OO0OOOOO000O00000 .json ()['token']#line:94
            try :#line:95
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0OOO000O000O000O}',OOO0OOOOO000OO0O0 ,ex =1800 ):#line:96
                    print ("✅Token缓存成功")#line:97
                else :#line:98
                    print ("❌Token缓存失败")#line:99
            except Exception as OO0OO0O00000000OO :#line:100
                print (f"✅获取实时Token")#line:101
            return OOO0OOOOO000OO0O0 #line:102
    except Exception as OO0OO0O00000000OO :#line:103
        print (f"Token error: {str(OO0OO0O00000000OO)}")#line:104
        return #line:105
def getJdTime ():#line:107
    OOOO00OO000O0O0O0 =int (round (time .time ()*1000 ))#line:108
    return OOOO00OO000O0O0O0 #line:109
def randomString (O0OOO00O00OOOO0O0 ,flag =False ):#line:111
    O0OOO0O0OO00O00O0 ="0123456789abcdef"#line:112
    if flag :O0OOO0O0OO00O00O0 =O0OOO0O0OO00O00O0 .upper ()#line:113
    O0O0O000O0O0000O0 =[random .choice (O0OOO0O0OO00O00O0 )for _O00O0O00O000O0000 in range (O0OOO00O00OOOO0O0 )]#line:114
    return ''.join (O0O0O000O0O0000O0 )#line:115
def check (OO00O0O0000O0O00O ):#line:117
    try :#line:118
        OOOOOO0O0O0000000 ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:119
        OO0000O0OOO0O00O0 ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OO00O0O0000O0O00O ,"User-Agent":ua ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:129
        O00O0O0000000OO0O =requests .get (url =OOOOOO0O0O0000000 ,headers =OO0000O0OOO0O00O0 ).text #line:130
        O0O0OO00OO000OO00 =json .loads (O00O0O0000000OO0O )#line:131
        if O0O0OO00OO000OO00 ['retcode']=='1001':#line:132
            O0OO00000OOO0OO00 ="当前ck已失效，请检查"#line:133
            return {'code':1001 ,'data':O0OO00000OOO0OO00 }#line:134
        elif O0O0OO00OO000OO00 ['retcode']=='0'and 'userInfo'in O0O0OO00OO000OO00 ['data']:#line:135
            OOO0OOO000OO00OOO =O0O0OO00OO000OO00 ['data']['userInfo']['baseInfo']['nickname']#line:136
            return {'code':200 ,'name':OOO0OOO000OO00OOO ,'ck':cookie }#line:137
    except Exception as OOO0OOOO0O00OOOO0 :#line:138
        return {'code':0 ,'data':OOO0OOOO0O00OOOO0 }#line:139
def getActivity ():#line:141
    OOO0O00O0O00O00O0 =activityUrl #line:142
    OOOO00OO0OO000OOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:150
    OO00O000O00O000O0 =requests .request ("GET",OOO0O00O0O00O00O0 ,headers =OOOO00OO0OO000OOO )#line:151
    if OO00O000O00O000O0 .status_code !=200 :#line:152
        print (OO00O000O00O000O0 .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:153
        sys .exit ()#line:154
def followShop (O000O0OOO0OOOO00O ):#line:156
    OO000OOOO000000OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followShop/follow"#line:157
    O0O0OOO0O000000O0 ={}#line:158
    OO0O0OO000O0OOOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O000O0OOO0OOOO00O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:170
    O0000000000O0O0O0 =requests .post (OO000OOOO000000OO ,headers =OO0O0OO000O0OOOO0 ,data =json .dumps (O0O0OOO0O000000O0 ))#line:171
    try :#line:172
        return O0000000000O0O0O0 .json ()#line:173
    except :#line:174
        return False #line:175
def getUserInfo (O0OO0O000O00OO0O0 ):#line:177
    OOO0000000O00OOO0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login"#line:178
    O0O0O00O0000O0OOO ={"status":"1","activityId":activityId ,"source":"01","tokenPin":token ,"shareUserId":O0OO0O000O00OO0O0 }#line:185
    O00O00OOOO0O0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':'','Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};'}#line:198
    OOO00000O0O0OO0O0 =requests .request ("POST",OOO0000000O00OOO0 ,headers =O00O00OOOO0O0O0OO ,data =json .dumps (O0O0O00O0000O0OOO ))#line:199
    if OOO00000O0O0OO0O0 .status_code ==200 :#line:200
        OOO0OOO0OOO0O0O0O =OOO00000O0O0OO0O0 .json ()#line:201
        if OOO0OOO0OOO0O0O0O ['data']:#line:202
            return OOO0OOO0OOO0O0O0O ['data']#line:203
        else :#line:204
            print (OOO0OOO0OOO0O0O0O )#line:205
    else :#line:206
        print (f"{OOO00000O0O0OO0O0.status_code} ⚠️ip疑似黑了,休息一会再来撸~")#line:207
        sys .exit ()#line:208
def drawPrize (O000OO0O000OOO0O0 ):#line:210
    OOO0OO00OO0OO00O0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/drawPrize"#line:211
    OOO0OO00OO0O0O0O0 ={}#line:212
    OOO0OO0O00O0OO00O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O000OO0O000OOO0O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:224
    O0O0O00OO0000000O =requests .post (OOO0OO00OO0OO00O0 ,headers =OOO0OO0O00O0OO00O ,data =json .dumps (OOO0OO00OO0O0O0O0 ))#line:225
    try :#line:226
        OO0O00OOO0OOOOO00 =O0O0O00OO0000000O .json ()#line:227
        O0O0O000OO00OO0OO =OO0O00OOO0OOOOO00 ['data']#line:228
        return O0O0O000OO00OO0OO #line:229
    except :#line:230
        return False #line:231
def addSkuAct (OOOO00OOOOO0OOO0O ):#line:233
    OOOOOOO0OO00OOO00 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/addSku/activity"#line:234
    O0O000O0OOO0O0000 ={}#line:235
    O000O0O00OOOOO00O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOOO00OOOOO0OOO0O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:247
    O0OOO00O0O00O00OO =requests .post (OOOOOOO0OO00OOO00 ,headers =O000O0O00OOOOO00O ,data =json .dumps (O0O000O0OOO0O0000 ))#line:248
    try :#line:249
        O0O0O000000O000OO =O0OOO00O0O00O00OO .json ()#line:250
        OO00O0OOOO0OOO000 =O0O0O000000O000OO ['data']#line:251
        return OO00O0OOOO0OOO000 #line:252
    except :#line:253
        return False #line:254
def addSku (OO000O0000OO000O0 ,OOO0OOO0O0OOOO0OO ,OOO0000OOOOOO0O00 ):#line:256
    O0OOO0000O00O0000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/addSku/toDo"#line:257
    OOO0O000OO0000OO0 ={"taskId":OOO0OOO0O0OOOO0OO ,"skuId":OOO0000OOOOOO0O00 ,}#line:261
    OOOOOOO00OOOO000O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO000O0000OO000O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:273
    O000OO00OOO0OOO0O =requests .post (O0OOO0000O00O0000 ,headers =OOOOOOO00OOOO000O ,data =json .dumps (OOO0O000OO0000OO0 ))#line:274
    try :#line:275
        O00O000OO0OO0O00O =O000OO00OOO0OOO0O .json ()#line:276
        if O00O000OO0OO0O00O ['resp_code']==0 :#line:277
            if "data"in str (O00O000OO0OO0O00O ):#line:278
                O0OO0O0000000OOOO =O00O000OO0OO0O00O ['data']#line:279
                return O0OO0O0000000OOOO #line:280
            else :#line:281
                return 99 #line:282
        else :#line:283
            print (f"addSku Error: {O00O000OO0OO0O00O['resp_msg']}")#line:284
    except Exception as OOOOOOOO00OOOOOO0 :#line:285
        print (f"addSku Error: {OOOOOOOO00OOOOOO0}")#line:286
def getMember (O0OOOO000OO0OO00O ,O00O00000O000OO0O ):#line:288
    OOO0000O000OOOO0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/getMember"#line:289
    OO0O000OOO0OO0000 ={"shareUserId":O00O00000O000OO0O }#line:292
    OOO0O0OO0OO0O0OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0OOOO000OO0OO00O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:304
    OOOO0000000OO0OO0 =requests .post (OOO0000O000OOOO0O ,headers =OOO0O0OO0OO0O0OO0 ,data =json .dumps (OO0O000OOO0OO0000 ))#line:305
    try :#line:306
        OOOO00O0O00OOOO00 =OOOO0000000OO0OO0 .json ()#line:307
        OO00OO00OOOO000O0 =OOOO00O0O00OOOO00 ['data']['shareUser']#line:308
        return OO00OO00OOOO000O0 #line:309
    except Exception as O0OO00OOO0OOOOO00 :#line:310
        print (str (O0OO00OOO0OOOOO00 ))#line:311
        return False #line:312
def prizeList (OOOOO00O000O000OO ):#line:314
    O00O0OOO0OO0O0OOO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/prizeList"#line:315
    O00O00000O00000OO ={}#line:316
    O000O0OO0O000OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOOOO00O000O000OO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:328
    OOO0OO000OOO00OOO =requests .post (O00O0OOO0OO0O0OOO ,headers =O000O0OO0O000OO0O ,data =json .dumps (O00O00000O00000OO ))#line:329
    try :#line:330
        return OOO0OO000OOO00OOO .json ()#line:331
    except :#line:332
        return False #line:333
def joinCheck (O00O0O000O00O0OO0 ):#line:335
    OOO0OOOO0OOO00O0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/join/check"#line:336
    OOO00O0OO0OO00O00 ={"status":"0"}#line:339
    O0O00O00O0O0O0000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O00O0O000O00O0OO0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:351
    O00O00000O0O0O0OO =requests .post (OOO0OOOO0OOO00O0O ,headers =O0O00O00O0O0O0000 ,data =json .dumps (OOO00O0OO0OO00O00 ))#line:352
    try :#line:353
        return O00O00000O0O0O0OO .json ()#line:354
    except :#line:355
        return False #line:356
def getUserId (O0O0O0O0OOO00O0OO ):#line:358
    OO0OOO0O0O0000O0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/share/getUserId"#line:359
    O00OOO0OOO00O0OOO ={}#line:360
    OO0O0O00O00OO00OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0O0O0O0OOO00O0OO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:372
    O00000OOO0O0OOO0O =requests .post (OO0OOO0O0O0000O0O ,headers =OO0O0O00O00OO00OO ,data =json .dumps (O00OOO0OOO00O0OOO ))#line:373
    try :#line:374
        return O00000OOO0O0OOO0O .json ()['data']['shareUserId']#line:375
    except Exception as O0O00O0OO0OO00O0O :#line:376
        print (str (O0O00O0OO0OO00O0O ))#line:377
def receiveAcquire (OOOOOO0O0000OOOO0 ,OOO0O00000O0O0OO0 ):#line:379
    O0OOOOOOO00O0OO00 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/receive/acquire"#line:380
    O0OOOO0OOO0O0O0O0 ={"prizeInfoId":OOO0O00000O0O0OO0 ,"status":1 }#line:384
    OO00OOOO0O000O00O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOOOOO0O0000OOOO0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:396
    OO000OOOOO0OOO0O0 =requests .post (O0OOOOOOO00O0OO00 ,headers =OO00OOOO0O000O00O ,data =json .dumps (O0OOOO0OOO0O0O0O0 ))#line:397
    try :#line:398
        return OO000OOOOO0OOO0O0 .json ()['resp_code']#line:399
    except :#line:400
        print (OO000OOOOO0OOO0O0 .text )#line:401
        return False #line:402
def bindWithVender (OOOO00O0OOO000000 ,OO000O0000OO0OO0O ,OOOOOO000OO00O000 ):#line:404
    try :#line:405
        OOOOO000OOO0000OO ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':OOOOOO000OO00O000 ,'shopId':OO000O0000OO0OO0O ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:414
        OOO0O00000OOO0O0O ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':OOOO00O0OOO000000 }#line:427
        O0OO00OO00O0OOOO0 =requests .request ("POST","https://api.m.jd.com/",headers =OOO0O00000OOO0O0O ,data =OOOOO000OOO0000OO ,timeout =10 ).text #line:428
        OOO0OOO0000OO0OO0 =json .loads (O0OO00OO00O0OOOO0 )#line:429
        if OOO0OOO0000OO0OO0 ['success']:#line:430
            return OOO0OOO0000OO0OO0 ['message']#line:431
    except Exception as OO0OOO00OOOO000OO :#line:432
        print (f"bindWithVender Error: {OOOOOO000OO00O000} {OO0OOO00OOOO000OO}")#line:433
def getShopOpenCardInfo (OOOOOOO0000000OOO ,OO000OOOO0000O00O ):#line:435
    OOOOOOOO000OOO0OO =f"https://shopmember.m.jd.com/shopcard/?venderId={OO000OOOO0000O00O}&channel=401&returnUrl={quote_plus(activityUrl)}"#line:436
    try :#line:437
        O000O000OOO0O0O00 ={"venderId":str (OO000OOOO0000O00O ),"channel":"8019006"}#line:438
        O0OO00O0OO000OO00 =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(O000O000OOO0O0O00)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:439
        O00OO0OOOOO0O0OO0 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OOOOOOO0000000OOO ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':OOOOOOOO000OOO0OO ,'Accept-Encoding':'gzip, deflate'}#line:449
        O0OOOOO00OOO0000O =requests .get (url =O0OO00O0OO000OO00 ,headers =O00OO0OOOOO0O0OO0 ,timeout =5 ).text #line:450
        O000000O0O0OO0O0O =json .loads (O0OOOOO00OOO0000O )#line:451
        if O000000O0O0OO0O0O ['success']:#line:452
            OO00000O0OO0000OO =O000000O0O0OO0O0O ['result']['shopMemberCardInfo']['venderCardName']#line:453
            OO00OOOO0OOOO0OO0 =O000000O0O0OO0O0O ['result']['userInfo']['openCardStatus']#line:454
            return OO00000O0OO0000OO ,OO00OOOO0OOOO0OO0 #line:455
        else :#line:456
            return False ,1 #line:457
    except :#line:458
        return False ,1 #line:459
if __name__ =='__main__':#line:462
    r =redis_conn ()#line:463
    try :#line:464
        cks =getCk #line:465
        if not cks :#line:466
            sys .exit ()#line:467
    except :#line:468
        print ("未获取到有效COOKIE,退出程序！")#line:469
        sys .exit ()#line:470
    global shareUserId ,inviteSuccNum ,activityUrl ,firstCk ,MSG #line:471
    inviteSuccNum =0 #line:472
    shareUserId =""#line:473
    MSG =''#line:474
    title ="🗣消息提醒：lzkjInteract加购有礼"#line:475
    activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&activityId={activityId}&templateId={templateId}&nodeId=101001&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:477
    num =0 #line:479
    for cookie in cks [:runNums ]:#line:480
        num +=1 #line:481
        if num ==1 :#line:482
            firstCk =cookie #line:483
        if num %5 ==0 :#line:484
            print ("⏰等待3s,休息一下")#line:485
            time .sleep (3 )#line:486
        global ua ,token #line:487
        ua =userAgent ()#line:488
        try :#line:489
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:490
            pt_pin =unquote_plus (pt_pin )#line:491
        except IndexError :#line:492
            pt_pin =re .compile (r'pin=(.*?);').findall (cookie )[0 ]#line:493
            pt_pin =unquote_plus (pt_pin )#line:494
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:495
        print (datetime .now ())#line:496
        try :#line:498
            result =check (cookie )#line:499
            if result ['code']!=200 :#line:500
                print (f"⚠️当前CK失效！跳过")#line:501
                continue #line:502
            token =getToken (cookie ,r )#line:503
            if token is None :#line:504
                print (f"⚠️获取Token失败！⏰等待3s")#line:505
                time .sleep (2 )#line:506
                continue #line:507
            time .sleep (0.2 )#line:508
            getActivity ()#line:509
            time .sleep (0.2 )#line:510
            userInfo =getUserInfo (shareUserId )#line:511
            if not userInfo :#line:512
                time .sleep (2 )#line:513
                continue #line:514
            shopId =userInfo ['shopId']#line:515
            openCardUrl =userInfo ['joinInfo']['openCardUrl']#line:516
            venderId =re .findall (r"venderId=(\w+)",openCardUrl )#line:517
            venderId =venderId [0 ]if venderId else ""#line:518
            Token =userInfo ['token']#line:519
            shopName =userInfo ['shopName']#line:520
            actName =userInfo ['actName']#line:521
            joinCodeInfo =userInfo ['joinInfo']['joinCodeInfo']#line:522
            customerId =userInfo ['customerId']#line:523
            time .sleep (0.2 )#line:524
            followShop (Token )#line:525
            time .sleep (0.2 )#line:526
            if num ==1 :#line:528
                print (f"✅ 开启【{actName}】活动")#line:529
                print (f"店铺名称：{shopName} {shopId}")#line:530
                MSG +=f'✅开启{shopName}--{actName}活动\n📝活动地址 {activityUrl.split("&shareUserId=")[0]}\n'#line:531
            prize =drawPrize (Token )#line:533
            prizeListRecord =[]#line:534
            prizeNameList =[]#line:535
            index =0 #line:536
            try :#line:537
                for prizeitem in prize ['prizeInfo']:#line:538
                    index +=1 #line:539
                    print (f"🎁 奖品: {prizeitem['prizeName']}, 剩余：{prizeitem['leftNum']}")#line:540
                    prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},剩余:{prizeitem['leftNum']}\n")#line:541
                    if prizeitem ['leftNum']>0 :#line:542
                        prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['id']))#line:543
                MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"if num ==1 else ""#line:544
            except :#line:545
                print ('⚠️无法获取奖品列表')#line:546
            print (f"参加活动状态：{joinCodeInfo['joinDes']}")#line:548
            if "关注店铺"in joinCodeInfo ['joinDes']:#line:549
                followShop (Token )#line:550
                print (f"关注店铺成功")#line:551
                time .sleep (0.2 )#line:552
            if "不是会员"in joinCodeInfo ['joinDes']or "加入会员"in joinCodeInfo ['joinDes']:#line:553
                venderCardName =getShopOpenCardInfo (cookie ,venderId )#line:554
                open_result =bindWithVender (cookie ,shopId ,venderId )#line:555
                if open_result is not None :#line:556
                    if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:557
                        print (f"⛈{open_result},无法完成关注任务")#line:558
                        continue #line:559
                    if "加入店铺会员成功"in open_result :#line:560
                        print (f"🎉🎉{venderCardName} {open_result}")#line:561
            skuInfo =addSkuAct (Token )#line:563
            finishNum =skuInfo ['addWares']['finishNum']#line:568
            completeCount =skuInfo ['addWares']['completeCount']#line:570
            oneClickPurchase =skuInfo ['addWares']['oneClickPurchase']#line:572
            print (f"需要加购{finishNum},已加购{completeCount}")#line:573
            taskId =skuInfo ['addWares']['taskId']#line:574
            skuInfoVO =skuInfo ['addWares']['skuInfoVO']#line:575
            skuIds =[O0OOO000O0O00O0OO ['skuId']for O0OOO000O0O00O0OO in skuInfoVO if not O0OOO000O0O00O0OO ['status']]#line:576
            status =skuInfo ['addWares']['status']#line:577
            if completeCount >=finishNum or status :#line:578
                print ("已经完成过加购任务")#line:579
            else :#line:580
                needAddCount =finishNum -completeCount #line:581
                for x in range (needAddCount ):#line:582
                    skuId =skuIds [x ]if oneClickPurchase else ""#line:583
                    addSkuResult =addSku (Token ,taskId ,skuId )#line:584
                    if addSkuResult ==99 :#line:586
                        if x ==needAddCount -1 :#line:587
                            print (f"成功加购{needAddCount}个商品,获得💨💨💨")#line:588
                    else :#line:589
                        prizeName =addSkuResult ['prizeName']#line:591
                        prizeType =addSkuResult ['prizeType']#line:592
                        print (f"🎁成功加购{needAddCount}个商品,获得{prizeName}")#line:593
                        MSG +=f'【账号{num}】{pt_pin} 🎉{prizeName}\n'#line:594
                        if "积分"not in prizeName and "京豆"not in prizeName and "优惠券"not in prizeName :#line:595
                            print (f"🎉恭喜获得实物,请前往{activityUrl}手动领取奖励！")#line:596
                            MSG_ =f'【账号{num}】{pt_pin} 🎉恭喜获得实物,请前往{activityUrl}手动领取奖励！'#line:597
                            msg_ =f"⏰{str(datetime.now())[:19]}\n"+MSG_ #line:598
                            send (title ,msg_ )#line:599
                    time .sleep (0.1 )#line:600
        except Exception as e :#line:601
            print (e )#line:602
        time .sleep (2 )#line:603
    msg =f"⏰{str(datetime.now())[:19]}\n"+MSG #line:605
    send (title ,msg )