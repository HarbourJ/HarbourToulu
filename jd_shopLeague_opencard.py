#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_shopLeague_opencard.py(通用开卡-超店shopLeague系列)
Author: HarbourJ
Date: 2022/8/12 20:37
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('通用开卡-超店shopLeague系列');
ActivityEntry: https://lzdz1-isv.isvjd.com/dingzhi/shop/league/activity?activityId=dzd16c3e4a819a0e14026da9shop
Description: dingzhi/shop/league系列通用开卡脚本(通常情况下,开一张卡5,最高获得220豆,邀请成功获得20豆)。
            本地sign算法+redis缓存Token
            变量: export jd_shopLeagueId="2b870a1a7450xxxxxxxxxxxxx" 变量值需要传入活动id
            并发变量：export jd_shopLeague_uuid="你的shareUuid"
Update: 2022/11/01 更新入会算法，内置船新入会本地算法
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from datetime import datetime #line:2
from urllib .parse import quote_plus ,unquote_plus #line:3
from functools import partial #line:4
print =partial (print ,flush =True )#line:5
import warnings #line:6
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:7
try :#line:9
    from jd_sign import *#line:10
except ImportError as e :#line:11
    print (e )#line:12
    if "No module"in str (e ):#line:13
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")#line:14
    sys .exit ()#line:15
try :#line:16
    from jdCookie import get_cookies #line:17
    getCk =get_cookies ()#line:18
except :#line:19
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:20
    sys .exit (3 )#line:21
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:23
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:24
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:25
jd_shopLeagueId =os .environ .get ("jd_shopLeagueId")if os .environ .get ("jd_shopLeagueId")else ""#line:26
inviterUuid =os .environ .get ("jd_shopLeague_uuid")if os .environ .get ("jd_shopLeague_uuid")else ""#line:27
if not jd_shopLeagueId :#line:29
    print ("⚠️未发现有效超店活动变量jd_shopLeagueId,退出程序!")#line:30
    sys .exit ()#line:31
if "lzdz1_remote"in jd_shopLeagueId :#line:33
    jd_jd_shopLeagueId_remote =remote_redis (jd_shopLeagueId )#line:34
    jd_shopLeagueId =jd_jd_shopLeagueId_remote #line:35
else :#line:36
    if not jd_shopLeagueId :#line:37
        print ("⚠️活动变量错误,退出程序!")#line:38
        sys .exit ()#line:39
activityId =jd_shopLeagueId .split ('&')[0 ]#line:41
activity_url =f"https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/activity/5929859?activityId={activityId}&shareUuid={inviterUuid}"#line:42
print (f"【🛳活动入口】https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/activity/5929859?activityId={activityId}")#line:43
def redis_conn ():#line:45
    try :#line:46
        import redis #line:47
        try :#line:48
            OO0OO0O000O000OO0 =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:49
            OO0OOO0000O0O00O0 =redis .Redis (connection_pool =OO0OO0O000O000OO0 )#line:50
            OO0OOO0000O0O00O0 .get ('conn_test')#line:51
            print ('✅redis连接成功')#line:52
            return OO0OOO0000O0O00O0 #line:53
        except :#line:54
            print ("⚠️redis连接异常")#line:55
    except :#line:56
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:57
        sys .exit ()#line:58
def getToken (OO0O00OOOO0O00OOO ,r =None ):#line:60
    O00O0OO0OO0OOOO0O =f'{activityUrl.split("com/")[0]}com'#line:61
    try :#line:62
        OOO0O00O0000O0O0O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OO0O00OOOO0O00OOO )[0 ])#line:63
    except :#line:64
        OOO0O00O0000O0O0O =OO0O00OOOO0O00OOO [:15 ]#line:65
    try :#line:66
        try :#line:67
            OOOOO00OO000O0OO0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOO0O00O0000O0O0O}')#line:68
        except Exception as OO0O0OOOOO0000O00 :#line:69
            OOOOO00OO000O0OO0 =None #line:71
        if OOOOO00OO000O0OO0 is not None :#line:72
            print (f"♻️获取缓存Token")#line:73
            return OOOOO00OO000O0OO0 #line:74
        else :#line:75
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0O00OOOO0O00OOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:86
            sign ({"url":f"{O00O0OO0OO0OOOO0O}","id":""},'isvObfuscator')#line:87
            OOO0O000OOOO00OOO =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:88
            if OOO0O000OOOO00OOO .status_code !=200 :#line:89
                print (OOO0O000OOOO00OOO .status_code )#line:90
                return #line:91
            else :#line:92
                if "参数异常"in OOO0O000OOOO00OOO .text :#line:93
                    print (OOO0O000OOOO00OOO .text )#line:94
                    return #line:95
            OO0OO00O0O0O0OOOO =OOO0O000OOOO00OOO .json ()['token']#line:96
            try :#line:97
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOO0O00O0000O0O0O}',OO0OO00O0O0O0OOOO ,ex =1800 ):#line:98
                    print ("✅Token缓存成功")#line:99
                else :#line:100
                    print ("❌Token缓存失败")#line:101
            except Exception as OO0O0OOOOO0000O00 :#line:102
                print (f"✅获取实时Token")#line:104
            return OO0OO00O0O0O0OOOO #line:105
    except Exception as OO0O0OOOOO0000O00 :#line:106
        print (f"Get Token Error: {str(OO0O0OOOOO0000O00)}")#line:107
        return #line:108
def getJdTime ():#line:110
    OO0O0OO00O00OO0OO =int (round (time .time ()*1000 ))#line:111
    return OO0O0OO00O00OO0OO #line:112
def randomString (O00O00OOOOO0OO0O0 ,flag =False ):#line:114
    OO00O0OO0OO0OO0OO ="0123456789abcdef"#line:115
    if flag :OO00O0OO0OO0OO0OO =OO00O0OO0OO0OO0OO .upper ()#line:116
    OO0O0O000000O0O00 =[random .choice (OO00O0OO0OO0OO0OO )for _O00OO0O0OOO0O0O0O in range (O00O00OOOOO0OO0O0 )]#line:117
    return ''.join (OO0O0O000000O0O00 )#line:118
def refresh_cookies (OOOOOO00O0000O0OO ):#line:120
    if OOOOOO00O0000O0OO .cookies :#line:121
        O00000OO0000O00OO =OOOOOO00O0000O0OO .cookies .get_dict ()#line:122
        OO0O000OOO000OO0O =[(O0O0O0OOOO00OOOO0 +"="+O00000OO0000O00OO [O0O0O0OOOO00OOOO0 ])for O0O0O0OOOO00OOOO0 in O00000OO0000O00OO ]#line:123
        global activityCookie #line:124
        O00O00O000O000000 =[O0O0OO0OOO0OOO00O for O0O0OO0OOO0OOO00O in activityCookie .split (';')if O0O0OO0OOO0OOO00O !='']#line:125
        for OOOOOOO0O0000O00O in O00O00O000O000000 :#line:126
            for OOO0OO0O00OO0OO00 in OO0O000OOO000OO0O :#line:127
                if OOOOOOO0O0000O00O .split ('=')[0 ]==OOO0OO0O00OO0OO00 .split ('=')[0 ]:#line:128
                    if OOOOOOO0O0000O00O .split ('=')[1 ]!=OOO0OO0O00OO0OO00 .split ('=')[1 ]:#line:129
                        O00O00O000O000000 .remove (OOOOOOO0O0000O00O )#line:130
        activityCookie =''.join (sorted ([(OOO0000O0O000OOOO +";")for OOO0000O0O000OOOO in list (set (O00O00O000O000000 +OO0O000OOO000OO0O ))]))#line:131
def getActivity ():#line:133
    O0O000OOO00O00O0O =activityUrl #line:134
    O0000O0000OO00000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:142
    O0O000OO00OOO0000 =requests .request ("GET",O0O000OOO00O00O0O ,headers =O0000O0000OO00000 )#line:143
    if O0O000OO00OOO0000 .status_code ==200 :#line:144
        if O0O000OO00OOO0000 .cookies :#line:145
            O000O0OOOO0000O00 =O0O000OO00OOO0000 .cookies .get_dict ()#line:146
            OOO0OO0OOOO0OOO0O =[(OO0OOO0O0O000O000 +"="+O000O0OOOO0000O00 [OO0OOO0O0O000O000 ])for OO0OOO0O0O000O000 in O000O0OOOO0000O00 ]#line:147
            OOOO000O0O000OOOO =''.join (sorted ([(O0OO0O0OOO0000000 +";")for O0OO0O0OOO0000000 in OOO0OO0OOOO0OOO0O ]))#line:148
        return OOOO000O0O000OOOO #line:149
    else :#line:150
        print (O0O000OO00OOO0000 .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:151
        sys .exit ()#line:152
def getSystemConfigForNew ():#line:154
    O0OO000000O000O00 ="https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:155
    O0OO0O0OO00O0OO00 =f'activityId={activityId}&activityType=99'#line:156
    OOO0OO0O00O0O00OO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:169
    OOOOOO00O0O000O00 =requests .request ("POST",O0OO000000O000O00 ,headers =OOO0OO0O00O0O00OO ,data =O0OO0O0OO00O0OO00 )#line:170
    refresh_cookies (OOOOOO00O0O000O00 )#line:171
def getSimpleActInfoVo ():#line:173
    O0OO00O0OO00OOOO0 ="https://lzdz1-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"#line:174
    O00000O0000O00OOO =f"activityId={activityId}"#line:175
    OO0O000OOO0O000OO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:188
    OO0OO00OOO000O0O0 =requests .request ("POST",O0OO00O0OO00OOOO0 ,headers =OO0O000OOO0O000OO ,data =O00000O0000O00OOO )#line:189
    refresh_cookies (OO0OO00OOO000O0O0 )#line:190
    O0O00O00OO00O00OO =OO0OO00OOO000O0O0 .json ()#line:191
    if O0O00O00OO00O00OO ['result']:#line:192
        return O0O00O00OO00O00OO ['data']#line:193
    else :#line:194
        print (f"getSimpleActInfoVo Error: {O0O00O00OO00O00OO['errorMessage']}")#line:195
def getMyPing (O00OO00O000OO0O00 ,OOO00OO0O0OOOOO00 ):#line:197
    OO0O0OOO00O00O00O ="https://lzdz1-isv.isvjcloud.com/customer/getMyPing"#line:198
    OOO0O000OOOOOOOO0 =f"userId={OOO00OO0O0OOOOO00}&token={token}&fromType=APP"#line:199
    O00O000O00O00OO00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:212
    O000000O0O0OOOO00 =requests .request ("POST",OO0O0OOO00O00O00O ,headers =O00O000O00O00OO00 ,data =OOO0O000OOOOOOOO0 )#line:213
    refresh_cookies (O000000O0O0OOOO00 )#line:214
    O0O0OOOOOO00000OO =O000000O0O0OOOO00 .json ()#line:215
    if O0O0OOOOOO00000OO ['result']:#line:216
        return O0O0OOOOOO00000OO ['data']['nickname'],O0O0OOOOOO00000OO ['data']['secretPin']#line:217
    else :#line:218
        print (f"⚠️getMyPing Error: {O0O0OOOOOO00000OO['errorMessage']}")#line:219
        if O00OO00O000OO0O00 ==1 and "火爆"in O0O0OOOOOO00000OO ['errorMessage']:#line:220
            print (f"\t⛈车头黑,退出本程序！")#line:221
            sys .exit ()#line:222
def accessLogWithAD (OOO0OOO00000OOOOO ,O00OOOO0OOOO000OO ):#line:224
    O0OOOO000OO0O0000 ="https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"#line:225
    O0OOOO0O0OO0O0O0O =f"venderId={OOO0OOO00000OOOOO}&code=99&pin={quote_plus(O00OOOO0OOOO000OO)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource=null"#line:226
    OOOOOO0O00O00OO0O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:239
    O00OOO0O0O00O00OO =requests .request ("POST",O0OOOO000OO0O0000 ,headers =OOOOOO0O00O00OO0O ,data =O0OOOO0O0OO0O0O0O )#line:240
    refresh_cookies (O00OOO0O0O00O00OO )#line:241
def getSystime ():#line:243
    O00000000OO000000 ="https://lzdz1-isv.isvjcloud.com/common/getSystime"#line:244
    OOO0000OOOO00000O ={'Host':'lzdz1-isv.isvjcloud.com','Origin':'https://lzdz1-isv.isvjcloud.com','Accept-Encoding':'gzip, deflate, br','Cookie':activityCookie ,'Content-Length':'0','Connection':'keep-alive','Accept':'application/json','User-Agent':ua ,'Referer':activityUrl ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','X-Requested-With':'XMLHttpRequest'}#line:257
    O0O0OOOO0O0OOO00O =requests .request ("POST",O00000000OO000000 ,headers =OOO0000OOOO00000O )#line:258
    refresh_cookies (O0O0OOOO0O0OOO00O )#line:259
def getUserInfo (O0OOO00OOOOO00OO0 ):#line:261
    OO0O000OO0OO0OOO0 ="https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo"#line:262
    OOOOO0O0OO0000000 =f"pin={quote_plus(O0OOO00OOOOO00OO0)}"#line:263
    O00O0O0OO0O0O0000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:276
    O0OOO0OOO00O00O0O =requests .request ("POST",OO0O000OO0OO0OOO0 ,headers =O00O0O0OO0O0O0000 ,data =OOOOO0O0OO0000000 )#line:277
    refresh_cookies (O0OOO0OOO00O00O0O )#line:278
    OO0OOOO0OO00000OO =O0OOO0OOO00O00O0O .json ()#line:279
    if OO0OOOO0OO00000OO ['result']:#line:280
        return OO0OOOO0OO00000OO ['data']['nickname'],OO0OOOO0OO00000OO ['data']['yunMidImageUrl'],OO0OOOO0OO00000OO ['data']['pin']#line:281
    else :#line:282
        print (f"getUserInfo Error: {OO0OOOO0OO00000OO['errorMessage']}")#line:283
def activityContent (OO00000O0OO0OOOO0 ,OOO0O0OOO0O0OO0OO ,O0O000O0OO00OOOO0 ):#line:285
    OOO000O0O0O0000O0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/activityContent"#line:286
    try :#line:287
        OO00OOO000000O00O =quote_plus (OOO0O0OOO0O0OO0OO )#line:288
    except :#line:289
        OO00OOO000000O00O =quote_plus ("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")#line:290
    OO0OO000OO000O0O0 =f"activityId={activityId}&pin={quote_plus(OO00000O0OO0OOOO0)}&pinImg={OO00OOO000000O00O}&nick={quote_plus(O0O000O0OO00OOOO0)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}"#line:291
    OOOO0OOO0O000O0O0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:304
    O000O0O0000O0O0O0 =requests .request ("POST",OOO000O0O0O0000O0 ,headers =OOOO0OOO0O000O0O0 ,data =OO0OO000OO000O0O0 )#line:305
    refresh_cookies (O000O0O0000O0O0O0 )#line:306
    OO00OO00O0OO00OO0 =O000O0O0000O0O0O0 .json ()#line:307
    if OO00OO00O0OO00OO0 ['result']:#line:308
        return OO00OO00O0OO00OO0 ['data']#line:309
    else :#line:310
        print (OO00OO00O0OO00OO0 ['errorMessage'])#line:311
        if "活动已结束"in OO00OO00O0OO00OO0 ['errorMessage']:#line:312
            sys .exit ()#line:313
def drawContent (OO00OO0O0O0OOO00O ):#line:315
    OO0O0O00000000OO0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent"#line:316
    O0OOOO00O00OO0000 =f"activityId={activityId}&pin={quote_plus(OO00OO0O0O0OOO00O)}"#line:317
    O000OO0OOO0OOOOO0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:330
    requests .request ("POST",OO0O0O00000000OO0 ,headers =O000OO0OOO0OOOOO0 ,data =O0OOOO00O00OO0000 )#line:331
def checkOpenCard (O00OO000O0O0OOO0O ,O0OO000OOOO0OOO0O ):#line:333
    try :#line:334
        OO0O0O0OO0O0O000O ="https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/checkOpenCard"#line:335
        OO0OO0O0OO0O0O00O =f"activityId={activityId}&pin={quote_plus(pin)}&shareUuid={O00OO000O0O0OOO0O}&actorUuid={O0OO000OOOO0OOO0O}"#line:336
        O00OO0O00OOO00O00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:349
        OO0OO0O00OO00OOOO =requests .request ("POST",OO0O0O0OO0O0O000O ,headers =O00OO0O00OOO00O00 ,data =OO0OO0O0OO0O0O00O )#line:350
        O000OOOOOOOOO0OO0 =OO0OO0O00OO00OOOO .json ()#line:352
        if O000OOOOOOOOO0OO0 ['result']:#line:353
            return O000OOOOOOOOO0OO0 ['data']#line:354
        else :#line:355
            print (f"checkOpenCard Error: {O000OOOOOOOOO0OO0['errorMessage']}")#line:356
            if "活动已结束"in O000OOOOOOOOO0OO0 ['errorMessage']:#line:357
                sys .exit ()#line:358
    except Exception as O0O000000OO0O0O0O :#line:359
        print (f"checkOpenCard Error: {O0O000000OO0O0O0O}")#line:360
def getDrawRecordHasCoupon (OO000O00O0O0OOOO0 ,O00O0OO000OOOOO00 ):#line:362
    O00000OO0O00OO0O0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/getDrawRecordHasCoupon"#line:363
    O0000O00OO00O0O00 =f"activityId={activityId}&pin={quote_plus(OO000O00O0O0OOOO0)}&actorUuid={O00O0OO000OOOOO00}"#line:364
    O0O000OO000O0O000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:377
    requests .request ("POST",O00000OO0O00OO0O0 ,headers =O0O000OO000O0O000 ,data =O0000O00OO00O0O00 )#line:378
def getShareRecord (OOOOOOOO0OO0OOOOO ):#line:380
    O0O0OO0OOOOO0O0O0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/getShareRecord"#line:381
    OOO000OO0OOOO000O =f"activityId={activityId}&actorUuid={OOOOOOOO0OO0OOOOO}"#line:382
    OOOOOO0O0O0O000O0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:395
    O0OO0O0000O0O00OO =requests .request ("POST",O0O0OO0OOOOO0O0O0 ,headers =OOOOOO0O0O0O000O0 ,data =OOO000OO0OOOO000O )#line:396
    O00OOOOOOO00000O0 =O0OO0O0000O0O00OO .json ()#line:397
    if O00OOOOOOO00000O0 ['result']:#line:398
        return O00OOOOOOO00000O0 ['data']#line:399
    else :#line:400
        print (f"getShareRecord Error: {O00OOOOOOO00000O0['errorMessage']}")#line:401
def saveTask (O0OO000O0O0O0O0OO ,O000OOO0000OOOO0O ,O0O00O0000O0OO0O0 ,O0OOOO0OOOO00OOO0 ,OOO0OOO00OO000OO0 ):#line:403
    OOO00OO00OOO0O0OO ="https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/saveTask"#line:404
    OOO00O0OOOO000O00 =f"activityId={activityId}&actorUuid={O0OO000O0O0O0O0OO}&pin={quote_plus(O0O00O0000O0OO0O0)}&shareUuid={O000OOO0000OOOO0O}&taskType={O0OOOO0OOOO00OOO0}&taskValue={OOO0OOO00OO000OO0}&taskUuid="#line:405
    O00000000O0O0OO00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:418
    OO00OOOOOO0OO0000 =requests .request ("POST",OOO00OO00OOO0O0OO ,headers =O00000000O0O0OO00 ,data =OOO00O0OOOO000O00 )#line:419
    O0O0OOO00OO0O00O0 =OO00OOOOOO0OO0000 .json ()#line:420
    if O0O0OOO00OO0O00O0 ['result']:#line:421
        print (O0O0OOO00OO0O00O0 ['data'])#line:422
        return O0O0OOO00OO0O00O0 ['data']#line:423
    else :#line:424
        print (f"saveTask Error: {O0O0OOO00OO0O00O0['errorMessage']}")#line:425
def bindWithVender (OO0O0000O0OO0O000 ,O0OOO00OOO00O0OOO ):#line:427
    try :#line:428
        OOOOOO0000O0O0OO0 ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':O0OOO00OOO00O0OOO ,'shopId':O0OOO00OOO00O0OOO ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:437
        OO0OO00O0OO0OO00O ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':OO0O0000O0OO0O000 }#line:450
        O000O00O0O00OO00O =requests .request ("POST","https://api.m.jd.com/",headers =OO0OO00O0OO0OO00O ,data =OOOOOO0000O0O0OO0 ,timeout =10 ).text #line:451
        O00OO0OOO000O000O =json .loads (O000O00O0O00OO00O )#line:452
        if O00OO0OOO000O000O ['success']:#line:453
            return O00OO0OOO000O000O ['message'],O00OO0OOO000O000O ['result']['giftInfo']if O00OO0OOO000O000O ['result']else ""#line:454
    except Exception as OO00O00O000O0OO0O :#line:455
        print (f"bindWithVender Error: {O0OOO00OOO00O0OOO} {OO00O00O000O0OO0O}")#line:456
def getShopOpenCardInfo (OOOOO00OO00O0000O ,OO00OO0O0OO0OOO0O ):#line:458
    try :#line:459
        OOOOOO00OOO0O000O ={"venderId":str (OO00OO0O0OO0OOO0O ),"channel":"401"}#line:460
        O0O0OO000O0OOOOOO =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OOOOOO00OOO0O000O)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:461
        O00OO00OO000OOOO0 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OOOOO00OO00O0000O ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate'}#line:471
        O00O0000O00O000OO =requests .get (url =O0O0OO000O0OOOOOO ,headers =O00OO00OO000OOOO0 ,timeout =10 ).text #line:472
        O0O0OO000OOOOOOOO =json .loads (O00O0000O00O000OO )#line:473
        if O0O0OO000OOOOOOOO ['success']:#line:474
            OO00O00OOO0OOOOOO =O0O0OO000OOOOOOOO ['result']['shopMemberCardInfo']['venderCardName']#line:475
            return OO00O00OOO0OOOOOO #line:476
        else :#line:477
            return OO00OO0O0OO0OOO0O #line:478
    except :#line:479
        return OO00OO0O0OO0OOO0O #line:480
if __name__ =='__main__':#line:483
    r =redis_conn ()#line:484
    try :#line:485
        cks =getCk #line:486
        if not cks :#line:487
            sys .exit ()#line:488
    except :#line:489
        print ("未获取到有效COOKIE,退出程序！")#line:490
        sys .exit ()#line:491
    global shareUuid ,inviteSuccNum ,activityUrl ,firstCk #line:492
    inviteSuccNum =0 #line:493
    if len (cks )==1 :#line:494
        shareUuid =inviterUuid #line:495
        activityUrl =activity_url #line:496
    else :#line:497
        shareUuid =remote_redis (f"lzdz1_{activityId}",2 )#line:498
        activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/activity/5929859?activityId={activityId}&shareUuid={shareUuid}"#line:499
    num =0 #line:500
    for cookie in cks [:]:#line:501
        num +=1 #line:502
        if num ==1 :#line:503
            firstCk =cookie #line:504
        if num %5 ==0 :#line:505
            print ("⏰等待10s,休息一下")#line:506
            time .sleep (10 )#line:507
        global ua ,activityCookie ,token #line:508
        ua =userAgent ()#line:509
        try :#line:510
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:511
            pt_pin =unquote_plus (pt_pin )#line:512
        except IndexError :#line:513
            pt_pin =f'用户{num}'#line:514
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:515
        print (datetime .now ())#line:516
        token =getToken (cookie ,r )#line:518
        if token is None :#line:519
            if num ==1 :#line:520
                print (f"⚠️车头获取Token失败,退出本程序！")#line:521
                sys .exit ()#line:522
            print (f"⚠️获取Token失败！⏰等待3s")#line:523
            time .sleep (3 )#line:524
            continue #line:525
        time .sleep (0.3 )#line:526
        activityCookie =getActivity ()#line:527
        time .sleep (0.3 )#line:528
        getSystemConfigForNew ()#line:529
        time .sleep (0.3 )#line:530
        getSimAct =getSimpleActInfoVo ()#line:531
        if getSimAct :#line:532
            venderId =getSimAct ['venderId']#line:533
        else :#line:534
            venderId ="1000003571"#line:535
        time .sleep (0.2 )#line:536
        getPin =getMyPing (num ,venderId )#line:537
        if getPin :#line:538
            nickname =getPin [0 ]#line:539
            secretPin =getPin [1 ]#line:540
            time .sleep (0.2 )#line:541
            accessLogWithAD (venderId ,secretPin )#line:542
            time .sleep (0.2 )#line:543
            userInfo =getUserInfo (secretPin )#line:544
            if not userInfo :#line:545
                continue #line:546
            time .sleep (0.3 )#line:547
            nickname =userInfo [0 ]#line:548
            yunMidImageUrl =userInfo [1 ]#line:549
            pin =userInfo [2 ]#line:550
            actContent =activityContent (pin ,yunMidImageUrl ,nickname )#line:551
            if not actContent :#line:552
                if num ==1 :#line:553
                    print ("⚠️无法获取车头邀请码,退出本程序！")#line:554
                    sys .exit ()#line:555
                time .sleep (3 )#line:556
                continue #line:557
            hasEnd =actContent ['hasEnd']#line:558
            if hasEnd :#line:559
                print ("活动已结束，下次早点来~")#line:560
                sys .exit ()#line:561
            print (f"✅开启【{actContent['activityName']}】活动\n")#line:562
            actorUuid =actContent ['actorUuid']#line:564
            followShop =actContent ['followShop']['allStatus']#line:565
            addSku =actContent ['addSku']['allStatus']#line:566
            print (f"邀请码->: {actorUuid}")#line:567
            print (f"准备助力->: {shareUuid}")#line:568
            time .sleep (0.2 )#line:569
            drawContent (pin )#line:570
            time .sleep (0.2 )#line:571
            checkOC =checkOpenCard (shareUuid ,actorUuid )#line:572
            allOpenCard =checkOC ['allOpenCard']#line:573
            assistStatus =checkOC ['assistStatus']#line:574
            beanNum =checkOC ['beanNum']#line:575
            sendBeanNum =checkOC ['sendBeanNum']#line:576
            cardList =checkOC ['cardList']#line:577
            assStat =False #line:578
            if allOpenCard :#line:579
                print ("已完成全部开卡任务")#line:580
                if assistStatus ==0 :#line:581
                    print ("已经助力过你~")#line:582
                elif assistStatus ==2 :#line:583
                    print ("已经助力过你~")#line:584
                elif assistStatus ==3 :#line:585
                    print ("已助力过其他好友~")#line:586
                elif assistStatus ==1 :#line:587
                    print ("已完成开卡关注任务,未助力过好友~")#line:588
                    assStat =True #line:589
                else :#line:590
                    assStat =True #line:591
            else :#line:592
                openCardLists =[(int (O00O00O0OOOO0OOO0 ['value']),O00O00O0OOOO0OOO0 ['name'])for O00O00O0OOOO0OOO0 in cardList if O00O00O0OOOO0OOO0 ['status']==0 ]#line:593
                print (f"现在去开卡,共计{len(openCardLists)}个会员💳")#line:594
                open_num =0 #line:595
                openExit =False #line:596
                for shop in openCardLists :#line:597
                    open_num +=1 #line:598
                    print (f"去开卡 {open_num}/{len(openCardLists)} {shop[0]}")#line:599
                    venderId =shop [0 ]#line:600
                    venderCardName =shop [1 ]#line:601
                    retry_time =0 #line:603
                    while True :#line:604
                        retry_time +=1 #line:605
                        open_result =bindWithVender (cookie ,venderId )#line:606
                        if open_result is not None :#line:607
                            if "火爆"in open_result [0 ]or "失败"in open_result [0 ]or "解绑"in open_result [0 ]:#line:608
                                print (f"\t⛈⛈{venderCardName} {open_result[0]}")#line:609
                                assStat =False #line:610
                                openExit =True #line:611
                            else :#line:612
                                print (f"\t🎉🎉{venderCardName} {open_result[0]}")#line:613
                                assStat =True #line:614
                            break #line:615
                        else :#line:616
                            time .sleep (0.5 )#line:617
                        if retry_time >=3 :#line:618
                            break #line:619
                    if openExit :#line:620
                        break #line:621
                    if open_num %5 ==0 :#line:622
                        print ("⏰等待5s,休息一下")#line:623
                        time .sleep (5 )#line:624
                    else :#line:625
                        time .sleep (2 )#line:626
                checkOC =checkOpenCard (shareUuid ,actorUuid )#line:627
                if not checkOC :#line:628
                    time .sleep (5 )#line:629
                    continue #line:630
                sendBeanNum =checkOC ['sendBeanNum']#line:631
                allOpenCard =checkOC ['allOpenCard']#line:632
                assistStatus =checkOC ['assistStatus']#line:633
                if sendBeanNum >0 :#line:634
                    print (f"\t🎁开卡获得{sendBeanNum}豆")#line:635
                else :#line:636
                    print (f"\t🤖开卡可能没水啦！")#line:637
                if allOpenCard and assistStatus ==1 :#line:638
                    assStat =True #line:639
                activityContent (pin ,yunMidImageUrl ,nickname )#line:640
                time .sleep (0.5 )#line:641
                drawContent (pin )#line:642
            print ("现在去一键关注店铺")#line:643
            saveTask (actorUuid ,shareUuid ,pin ,1 ,1 )#line:644
            time .sleep (0.3 )#line:645
            print ("现在去一键加购")#line:646
            saveTask (actorUuid ,shareUuid ,pin ,2 ,2 )#line:647
            time .sleep (0.3 )#line:648
            getSR =getShareRecord (actorUuid )#line:649
            if getSR and num ==1 :#line:650
                print (f"🧑‍🤝‍🧑已经邀请{len(getSR)}人")#line:651
            if assStat and num !=1 :#line:652
                print ("🎉🎉🎉助力成功~")#line:653
                inviteSuccNum +=1 #line:654
                print (f"本次车头已邀请{inviteSuccNum}人")#line:655
            if num ==1 :#line:656
                print (f"后面账号全部助力 {actorUuid}")#line:657
                shareUuid =actorUuid #line:658
                activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/shop/league/activity/5929859?activityId={activityId}&shareUuid={shareUuid}"#line:659
        time .sleep (3 )