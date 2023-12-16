#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_lzkjInteractFollow.py(jd_lzkjInteract关注有礼)
Author: HarbourJ
Date: 2022/11/24 10:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('jd_lzkjInteract关注有礼');
ActivityEntry: https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType=10053&templateId=20210804190900gzspyl011&activityId=1656581196896083970

Description: 关注xx商品xx豆,自动领奖
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
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")#line:14
try :#line:15
    from jdCookie import get_cookies #line:16
    getCk =get_cookies ()#line:17
except :#line:18
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:19
    sys .exit (3 )#line:20
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:22
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:23
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:24
jd_lzkjInteractUrl =os .environ .get ("jd_lzkjInteractFollowUrl")if os .environ .get ("jd_lzkjInteractFollowUrl")else ""#line:25
share_userId =os .environ .get ("jd_lzkjInteractUserId")if os .environ .get ("jd_lzkjInteractUserId")else ""#line:26
runNums =os .environ .get ("jd_lzkjInteractFollowRunNums")if os .environ .get ("jd_lzkjInteractFollowRunNums")else 12 #line:27
if "lzkj-isv.isvjcloud.com/prod/cc/interactsaas"not in jd_lzkjInteractUrl :#line:29
    print ("⛈暂不支持变量设置的活动类型,请检查后重试！仅支持interactsaas类型活动")#line:30
    sys .exit ()#line:31
templateId =re .findall (r"templateId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:32
activityId =re .findall (r"activityId=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:33
activityType =re .findall (r"activityType=(.*?)&",jd_lzkjInteractUrl +"&")[0 ]#line:34
print (f"【🛳活动入口】https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}")#line:36
runNums =int (runNums )#line:38
if runNums ==12 :#line:39
    print ('🤖本次关注默认跑前12个账号,设置自定义变量:export jd_lzkjInteractAddRunNums="需要运行关注的ck数量"')#line:40
else :#line:41
    print (f'🤖本次运行前{runNums}个账号')#line:42
def redis_conn ():#line:44
    try :#line:45
        import redis #line:46
        try :#line:47
            OO0OOOO00OOO0000O =redis .ConnectionPool (host =redis_url ,port =6379 ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:48
            O0OO00O00O000OOO0 =redis .Redis (connection_pool =OO0OOOO00OOO0000O )#line:49
            O0OO00O00O000OOO0 .get ('conn_test')#line:50
            print ('✅redis连接成功')#line:51
            return O0OO00O00O000OOO0 #line:52
        except :#line:53
            print ("⚠️redis连接异常")#line:54
    except :#line:55
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:56
        sys .exit ()#line:57
def getToken (O0O00OOO0O00O0O0O ,r =None ):#line:59
    OOOOOOO0OO00000O0 =f'{activityUrl.split("com/")[0]}com'#line:60
    try :#line:61
        O0O0OO00000O0000O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0O00OOO0O00O0O0O )[0 ])#line:62
    except :#line:63
        O0O0OO00000O0000O =O0O00OOO0O00O0O0O [:15 ]#line:64
    try :#line:65
        try :#line:66
            OO00OOOOOOO00OOO0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0O0OO00000O0000O}')#line:67
        except Exception as O0O000O00OOO00000 :#line:68
            OO00OOOOOOO00OOO0 =None #line:69
        if OO00OOOOOOO00OOO0 is not None :#line:70
            print (f"♻️获取缓存Token")#line:71
            return OO00OOOOOOO00OOO0 #line:72
        else :#line:73
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O00OOO0O00O0O0O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:84
            sign ({"url":f"{OOOOOOO0OO00000O0}","id":""},'isvObfuscator')#line:85
            OOO0O00OOOO00000O =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:86
            if OOO0O00OOOO00000O .status_code !=200 :#line:87
                print (OOO0O00OOOO00000O .status_code )#line:88
                return #line:89
            else :#line:90
                if "参数异常"in OOO0O00OOOO00000O .text :#line:91
                    print (OOO0O00OOOO00000O .text )#line:92
                    return #line:93
            OOOOOO0OO0O0OOO0O =OOO0O00OOOO00000O .json ()['token']#line:94
            try :#line:95
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0O0OO00000O0000O}',OOOOOO0OO0O0OOO0O ,ex =1800 ):#line:96
                    print ("✅Token缓存成功")#line:97
                else :#line:98
                    print ("❌Token缓存失败")#line:99
            except Exception as O0O000O00OOO00000 :#line:100
                print (f"✅获取实时Token")#line:101
            return OOOOOO0OO0O0OOO0O #line:102
    except Exception as O0O000O00OOO00000 :#line:103
        print (f"Token error: {str(O0O000O00OOO00000)}")#line:104
        return #line:105
def getJdTime ():#line:107
    O0000O0000000O00O =int (round (time .time ()*1000 ))#line:108
    return O0000O0000000O00O #line:109
def randomString (O0O0000O0OO00O0O0 ,flag =False ):#line:111
    O0O0O0O0OOOOO0O0O ="0123456789abcdef"#line:112
    if flag :O0O0O0O0OOOOO0O0O =O0O0O0O0OOOOO0O0O .upper ()#line:113
    OO0OO0O0OOO0O0000 =[random .choice (O0O0O0O0OOOOO0O0O )for _O0OOOOOOO0000O0OO in range (O0O0000O0OO00O0O0 )]#line:114
    return ''.join (OO0OO0O0OOO0O0000 )#line:115
def check (OOO0OOO00000O0OO0 ):#line:117
    try :#line:118
        OO0OO00OO0OOO00O0 ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:119
        OOOOOOOOO000OO00O ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OOO0OOO00000O0OO0 ,"User-Agent":ua ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:129
        O0OO00000O0O000OO =requests .get (url =OO0OO00OO0OOO00O0 ,headers =OOOOOOOOO000OO00O ).text #line:130
        OO0000O0O0O0O0O00 =json .loads (O0OO00000O0O000OO )#line:131
        if OO0000O0O0O0O0O00 ['retcode']=='1001':#line:132
            OOOO0OO000O0OOOO0 ="当前ck已失效，请检查"#line:133
            return {'code':1001 ,'data':OOOO0OO000O0OOOO0 }#line:134
        elif OO0000O0O0O0O0O00 ['retcode']=='0'and 'userInfo'in OO0000O0O0O0O0O00 ['data']:#line:135
            OO0OOO00000O00O00 =OO0000O0O0O0O0O00 ['data']['userInfo']['baseInfo']['nickname']#line:136
            return {'code':200 ,'name':OO0OOO00000O00O00 ,'ck':cookie }#line:137
    except Exception as OO0O00OOOO0000000 :#line:138
        return {'code':0 ,'data':OO0O00OOOO0000000 }#line:139
def getActivity ():#line:141
    OOOOO0O00OOOOO000 =activityUrl #line:142
    OOOO00OOOOO00OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:150
    O0O000O0O0OOO0OOO =requests .request ("GET",OOOOO0O00OOOOO000 ,headers =OOOO00OOOOO00OO0O )#line:151
    if O0O000O0O0OOO0OOO .status_code !=200 :#line:152
        print (O0O000O0O0OOO0OOO .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:153
        sys .exit ()#line:154
def followShop (OOO0O0OOO000000OO ):#line:156
    OO0OO0000OO0OO0OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followShop/follow"#line:157
    OO0O00000OOO00OO0 ={}#line:158
    O0OO0O0O0OO0OOOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOO0O0OOO000000OO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:170
    O00O000O000OOOO0O =requests .post (OO0OO0000OO0OO0OO ,headers =O0OO0O0O0OO0OOOO0 ,data =json .dumps (OO0O00000OOO00OO0 ))#line:171
    try :#line:172
        return O00O000O000OOOO0O .json ()#line:173
    except :#line:174
        return False #line:175
def getUserInfo (OOOO0O0000OOOO0O0 ):#line:177
    OOO0OO00O0O0OOO0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login"#line:178
    O000O00O0O0000OOO ={"status":"1","activityId":activityId ,"source":"01","tokenPin":token ,"shareUserId":OOOO0O0000OOOO0O0 }#line:185
    O00OOOOO00000OO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':'','Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};'}#line:198
    OO00O0O00O000OO00 =requests .request ("POST",OOO0OO00O0O0OOO0O ,headers =O00OOOOO00000OO00 ,data =json .dumps (O000O00O0O0000OOO ))#line:199
    if OO00O0O00O000OO00 .status_code ==200 :#line:200
        O000OO00O0OO00OOO =OO00O0O00O000OO00 .json ()#line:201
        if O000OO00O0OO00OOO ['data']:#line:202
            return O000OO00O0OO00OOO ['data']#line:203
        else :#line:204
            print (O000OO00O0OO00OOO )#line:205
    else :#line:206
        print (f"{OO00O0O00O000OO00.status_code} ⚠️ip疑似黑了,休息一会再来撸~")#line:207
        sys .exit ()#line:208
def drawPrize (OO000OOOOO0000O0O ):#line:210
    OO00OOO0O0OOOO000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/drawPrize"#line:211
    O00O0OOOO00O0O00O ={}#line:212
    OOO0O000OO0O0OOOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO000OOOOO0000O0O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:224
    OO00OOOOO0O00OO00 =requests .post (OO00OOO0O0OOOO000 ,headers =OOO0O000OO0O0OOOO ,data =json .dumps (O00O0OOOO00O0O00O ))#line:225
    try :#line:226
        OO0O0OO0OO0OO0000 =OO00OOOOO0O00OO00 .json ()#line:227
        O0O000O0OOOOO0OO0 =OO0O0OO0OO0OO0000 ['data']#line:228
        return O0O000O0OOOOO0OO0 #line:229
    except :#line:230
        return False #line:231
def followGoodsAct (OOO00OOOOO0O0OO00 ):#line:233
    O0OO000O00000O000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followGoods/getFollowGoods"#line:234
    OO00OO0000O00OOO0 ={}#line:235
    O0OO0O00O00000O0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOO00OOOOO0O0OO00 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:247
    OO0O0000000OO00OO =requests .post (O0OO000O00000O000 ,headers =O0OO0O00O00000O0O ,data =json .dumps (OO00OO0000O00OOO0 ))#line:248
    try :#line:249
        OOO0O0O0000OO00O0 =OO0O0000000OO00OO .json ()#line:250
        O000OO0OO0O0O0OO0 =OOO0O0O0000OO00O0 ['data']#line:251
        return O000OO0OO0O0O0OO0 #line:252
    except :#line:253
        return False #line:254
def followGoods (OO00O0O0OO000OOOO ,O00OO00OO000O0000 ):#line:256
    OO0000OOO0O0000O0 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followGoods/followGoods"#line:257
    O0O00O00OOOO0OOOO ={"skuId":O00OO00OO000O0000 ,}#line:260
    O0O00OOOOO00OOOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO00O0O0OO000OOOO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:272
    O00000OO0000OOO00 =requests .post (OO0000OOO0O0000O0 ,headers =O0O00OOOOO00OOOO0 ,data =json .dumps (O0O00O00OOOO0OOOO ))#line:273
    try :#line:274
        O0O0O0OOOOOOOO000 =O00000OO0000OOO00 .json ()#line:275
        if O0O0O0OOOOOOOO000 ['resp_code']==0 :#line:276
            if "data"in str (O0O0O0OOOOOOOO000 ):#line:277
                OO00OOOO00OOO0000 =O0O0O0OOOOOOOO000 ['data']#line:278
                if OO00OOOO00OOO0000 ['result']:#line:279
                    return OO00OOOO00OOO0000 #line:280
                else :#line:281
                    return 99 #line:282
            else :#line:283
                return 99 #line:284
        else :#line:285
            print (f"followGoods Error: {O0O0O0OOOOOOOO000['resp_msg']}")#line:286
    except Exception as O0OOO0O0OO000OO00 :#line:287
        print (f"followGoods Error: {O0OOO0O0OO000OO00}")#line:288
def getMember (O000O00OOOOO00O00 ,OO00OO0OOO0O0O000 ):#line:290
    O0OO000O000OO00OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/getMember"#line:291
    OOOOO0OO000OO000O ={"shareUserId":OO00OO0OOO0O0O000 }#line:294
    OOOOOOOO000O000OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O000O00OOOOO00O00 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:306
    OO0O00OO0O0O000O0 =requests .post (O0OO000O000OO00OO ,headers =OOOOOOOO000O000OO ,data =json .dumps (OOOOO0OO000OO000O ))#line:307
    try :#line:308
        O0O000O0000O00OO0 =OO0O00OO0O0O000O0 .json ()#line:309
        OOOO0OO00OO0O0O00 =O0O000O0000O00OO0 ['data']['shareUser']#line:310
        return OOOO0OO00OO0O0O00 #line:311
    except Exception as O00OOO00OOO00OOO0 :#line:312
        print (str (O00OOO00OOO00OOO0 ))#line:313
        return False #line:314
def prizeList (OO0OO0O000OO00OO0 ):#line:316
    O0OO0O0O0O00OOO0O ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/prizeList"#line:317
    O0000OOOO00000O00 ={}#line:318
    O0OOO0000O000OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO0OO0O000OO00OO0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:330
    O00000000000000OO =requests .post (O0OO0O0O0O00OOO0O ,headers =O0OOO0000O000OO0O ,data =json .dumps (O0000OOOO00000O00 ))#line:331
    try :#line:332
        return O00000000000000OO .json ()#line:333
    except :#line:334
        return False #line:335
def joinCheck (O0000OOOO0O00OOOO ):#line:337
    O000000O0OOO000OO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/join/check"#line:338
    OO0OO0O000000OOOO ={"status":"0"}#line:341
    O00000000O0OO00O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0000OOOO0O00OOOO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:353
    OOO0OO00OO0OOO0OO =requests .post (O000000O0OOO000OO ,headers =O00000000O0OO00O0 ,data =json .dumps (OO0OO0O000000OOOO ))#line:354
    try :#line:355
        return OOO0OO00OO0OOO0OO .json ()#line:356
    except :#line:357
        return False #line:358
def getUserId (O00O00OO00OO000O0 ):#line:360
    O0000O000OO0O0OOO ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/share/getUserId"#line:361
    O0OO0OO000OO0O0O0 ={}#line:362
    OOO0OOOO000OO00O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O00O00OO00OO000O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:374
    O0O00OO00O00O000O =requests .post (O0000O000OO0O0OOO ,headers =OOO0OOOO000OO00O0 ,data =json .dumps (O0OO0OO000OO0O0O0 ))#line:375
    try :#line:376
        return O0O00OO00O00O000O .json ()['data']['shareUserId']#line:377
    except Exception as OOOOO0OO0O00OO0O0 :#line:378
        print (str (OOOOO0OO0O00OO0O0 ))#line:379
def receiveAcquire (OO000O00OOO0OO00O ,OO0O0OOOOO0O00OO0 ):#line:381
    OOO000000OO0OO000 ="https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/receive/acquire"#line:382
    OOO0OO000OO0OOOOO ={"prizeInfoId":OO0O0OOOOO0O00OO0 ,"status":1 }#line:386
    OOO0O00O0O000O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OO000O00OOO0OO00O ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl }#line:398
    O00O0O0O0O00OO00O =requests .post (OOO000000OO0OO000 ,headers =OOO0O00O0O000O0OO ,data =json .dumps (OOO0OO000OO0OOOOO ))#line:399
    try :#line:400
        return O00O0O0O0O00OO00O .json ()['resp_code']#line:401
    except :#line:402
        print (O00O0O0O0O00OO00O .text )#line:403
        return False #line:404
def bindWithVender (OO00O00OOO0O00O0O ,O0O0O00O00OO00000 ,OOO0O0OO0000O0O0O ):#line:406
    try :#line:407
        O0O000O000000000O ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':OOO0O0OO0000O0O0O ,'shopId':O0O0O00O00OO00000 ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:416
        OOO00OOO0OOO0OOOO ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':OO00O00OOO0O00O0O }#line:429
        OO0O00OO0OO00O0OO =requests .request ("POST","https://api.m.jd.com/",headers =OOO00OOO0OOO0OOOO ,data =O0O000O000000000O ,timeout =10 ).text #line:430
        O0000O00OOO0OO0OO =json .loads (OO0O00OO0OO00O0OO )#line:431
        if O0000O00OOO0OO0OO ['success']:#line:432
            return O0000O00OOO0OO0OO ['message']#line:433
    except Exception as O0000OO0OO0000000 :#line:434
        print (f"bindWithVender Error: {OOO0O0OO0000O0O0O} {O0000OO0OO0000000}")#line:435
def getShopOpenCardInfo (OO00O0OO000000O0O ,O000O0OO0OOO0O0O0 ):#line:437
        try :#line:438
            O0OO000O000OOO0OO ={"venderId":str (O000O0OO0OOO0O0O0 ),"channel":"401"}#line:439
            OO00OOOO0OO00OO00 =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(O0OO000O000OOO0OO)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:440
            OO00O0OOO000O0000 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OO00O0OO000000O0O ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate'}#line:450
            OOO0O0OO0O000OOO0 =requests .get (url =OO00OOOO0OO00OO00 ,headers =OO00O0OOO000O0000 ,timeout =10 ,proxies =proxies ).text #line:451
            O00OO0OOO00O0OO0O =json .loads (OOO0O0OO0O000OOO0 )#line:452
            if O00OO0OOO00O0OO0O ['success']:#line:453
                OOO000O00OO0OOOOO =O00OO0OOO00O0OO0O ['result']['shopMemberCardInfo']['venderCardName']#line:454
                return OOO000O00OO0OOOOO #line:455
            else :#line:456
                return O000O0OO0OOO0O0O0 #line:457
        except :#line:458
            return O000O0OO0OOO0O0O0 #line:459
if __name__ =='__main__':#line:461
    r =redis_conn ()#line:462
    try :#line:463
        cks =getCk #line:464
        if not cks :#line:465
            sys .exit ()#line:466
    except :#line:467
        print ("未获取到有效COOKIE,退出程序！")#line:468
        sys .exit ()#line:469
    global shareUserId ,inviteSuccNum ,activityUrl ,firstCk ,MSG #line:470
    inviteSuccNum =0 #line:471
    shareUserId =""#line:472
    MSG =''#line:473
    title ="🗣消息提醒：lzkjInteract关注有礼"#line:474
    activityUrl =f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&activityId={activityId}&templateId={templateId}&nodeId=101001&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"#line:476
    num =0 #line:478
    for cookie in cks [:runNums ]:#line:479
        num +=1 #line:480
        if num ==1 :#line:481
            firstCk =cookie #line:482
        if num %5 ==0 :#line:483
            print ("⏰等待3s,休息一下")#line:484
            time .sleep (3 )#line:485
        global ua ,token #line:486
        ua =userAgent ()#line:487
        try :#line:488
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:489
            pt_pin =unquote_plus (pt_pin )#line:490
        except IndexError :#line:491
            pt_pin =re .compile (r'pin=(.*?);').findall (cookie )[0 ]#line:492
            pt_pin =unquote_plus (pt_pin )#line:493
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:494
        print (datetime .now ())#line:495
        try :#line:497
            result =check (cookie )#line:498
            if result ['code']!=200 :#line:499
                print (f"⚠️当前CK失效！跳过")#line:500
                continue #line:501
            token =getToken (cookie ,r )#line:502
            if token is None :#line:503
                print (f"⚠️获取Token失败！⏰等待3s")#line:504
                time .sleep (2 )#line:505
                continue #line:506
            time .sleep (0.2 )#line:507
            getActivity ()#line:508
            time .sleep (0.2 )#line:509
            userInfo =getUserInfo (shareUserId )#line:510
            if not userInfo :#line:511
                time .sleep (2 )#line:512
                continue #line:513
            shopId =userInfo ['shopId']#line:514
            openCardUrl =userInfo ['joinInfo']['openCardUrl']#line:515
            venderId =re .findall (r"venderId=(\w+)",openCardUrl )#line:516
            venderId =venderId [0 ]if venderId else shopId #line:517
            Token =userInfo ['token']#line:518
            shopName =userInfo ['shopName']#line:519
            actName =userInfo ['actName']#line:520
            joinCodeInfo =userInfo ['joinInfo']['joinCodeInfo']#line:521
            customerId =userInfo ['customerId']#line:522
            time .sleep (0.2 )#line:523
            if num ==1 :#line:525
                print (f"✅ 开启【{actName}】活动")#line:526
                print (f"店铺名称：{shopName} {shopId}")#line:527
                MSG +=f'✅开启{shopName}--{actName}活动\n📝活动地址 {activityUrl.split("&shareUserId=")[0]}\n'#line:528
            prize =drawPrize (Token )#line:530
            prizeListRecord =[]#line:531
            prizeNameList =[]#line:532
            index =0 #line:533
            try :#line:534
                for prizeitem in prize ['prizeInfo']:#line:535
                    index +=1 #line:536
                    print (f"🎁 奖品: {prizeitem['prizeName']}, 剩余：{prizeitem['leftNum']}")#line:537
                    prizeNameList .append (f"🎁奖品:{prizeitem['prizeName']},剩余:{prizeitem['leftNum']}\n")#line:538
                    if prizeitem ['leftNum']>0 :#line:539
                        prizeListRecord .append ((prizeitem ['prizeName'],prizeitem ['id']))#line:540
                MSG +=f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n"if num ==1 else ""#line:541
            except :#line:542
                print ('⚠️无法获取奖品列表')#line:543
            print (f"参加活动状态：{joinCodeInfo['joinDes']}")#line:545
            if "未关注店铺"in joinCodeInfo ['joinDes']:#line:546
                followShop (Token )#line:547
                print (f"关注店铺成功")#line:548
                time .sleep (0.2 )#line:549
            if "不是会员"in joinCodeInfo ['joinDes']or "加入会员"in joinCodeInfo ['joinDes']:#line:550
                venderCardName =getShopOpenCardInfo (cookie ,venderId )#line:551
                open_result =bindWithVender (cookie ,shopId ,venderId )#line:552
                if open_result is not None :#line:553
                    if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:554
                        print (f"⛈{open_result},无法完成关注任务")#line:555
                        continue #line:556
                    if "加入店铺会员成功"in open_result :#line:557
                        print (f"🎉🎉{venderCardName} {open_result}")#line:558
            skuInfo =followGoodsAct (Token )#line:560
            finishNum =skuInfo [0 ]['finishNum']#line:562
            completeCount =skuInfo [0 ]['completeCount']#line:563
            oneClickFollowPurchase =skuInfo [0 ]['oneClickFollowPurchase']#line:564
            if oneClickFollowPurchase :#line:565
                print (f"需要关注{finishNum},已关注{completeCount}")#line:566
            else :#line:567
                print (f"需要一键关注{finishNum}个商品")#line:568
            taskId =skuInfo [0 ]['taskId']#line:569
            skuInfoVO =skuInfo [0 ]['skuInfoVO']#line:570
            skuIds =[OO000OOOO000O000O ['skuId']for OO000OOOO000O000O in skuInfoVO if not OO000OOOO000O000O ['status']]#line:571
            status =skuInfo [0 ]['status']#line:572
            if completeCount >=finishNum or status :#line:573
                print ("已经完成过关注任务")#line:574
            else :#line:575
                needAddCount =finishNum -completeCount #line:576
                for x in range (needAddCount ):#line:577
                    skuId =skuIds [x ]if oneClickFollowPurchase else ""#line:578
                    followGoodsResult =followGoods (Token ,skuId )#line:579
                    if followGoodsResult ==99 :#line:581
                        if x ==needAddCount -1 :#line:582
                            print (f"成功关注{needAddCount}个商品,获得💨💨💨")#line:583
                    else :#line:584
                        prizeName =followGoodsResult ['prizeName']#line:586
                        prizeType =followGoodsResult ['prizeType']#line:587
                        print (f"🎁成功关注{needAddCount}个商品,获得{prizeName}")#line:588
                        MSG +=f'【账号{num}】{pt_pin} 🎉{prizeName}\n'#line:589
                        if "积分"not in prizeName and "京豆"not in prizeName and "优惠券"not in prizeName :#line:590
                            print (f"🎉恭喜获得实物,请前往{activityUrl}手动领取奖励！")#line:591
                            MSG_ =f'【账号{num}】{pt_pin} 🎉恭喜获得实物,请前往{activityUrl} 手动领取奖励！'#line:592
                            msg_ =f"⏰{str(datetime.now())[:19]}\n"+MSG_ #line:593
                            send (title ,msg_ )#line:594
                    time .sleep (0.1 )#line:595
        except Exception as e :#line:596
            print (e )#line:597
        time .sleep (2 )#line:598
    msg =f"⏰{str(datetime.now())[:19]}\n"+MSG #line:600
    send (title ,msg )