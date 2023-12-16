#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxBirthGifts.py(生日等级礼包-监控脚本)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('生日等级礼包-JK');
ActivityEntry: https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/activity?activityId=f3325e3375a14866xxxxxxxxxxxx
               变量 export jd_wxBirthGiftsId="活动🆔"
Update: 20221205 新增等级礼包模块
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from datetime import datetime #line:2
from urllib .parse import quote_plus ,unquote_plus #line:3
from functools import partial #line:4
print =partial (print ,flush =True )#line:5
import warnings #line:6
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:7
try :#line:8
    from jd_sign import *#line:9
except ImportError as e :#line:10
    print (e )#line:11
    if "No module"in str (e ):#line:12
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:13
    sys .exit ()#line:14
try :#line:15
    from jdCookie import get_cookies #line:16
    getCk =get_cookies ()#line:17
except :#line:18
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:19
    sys .exit (3 )#line:20
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:21
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:22
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:23
activityId =os .environ .get ("jd_wxBirthGiftsId")if os .environ .get ("jd_wxBirthGiftsId")else ""#line:24
if not activityId :#line:26
    print ("⚠️未发现有效活动变量,退出程序!")#line:27
    sys .exit ()#line:28
activityUrl =f"https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/activity?activityId={activityId}"#line:29
print (f"【🛳活动入口】{activityUrl}")#line:30
def redis_conn ():#line:32
    try :#line:33
        try :#line:34
            import redis #line:35
        except Exception as OOO0000O00O0O0000 :#line:36
            print (OOO0000O00O0O0000 )#line:37
            if "No module"in str (OOO0000O00O0O0000 ):#line:38
                os .system ("pip install redis")#line:39
            import redis #line:40
        try :#line:41
            OOOOO0OOOO0O0O00O =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:42
            O0O00O0O0O0O00OOO =redis .Redis (connection_pool =OOOOO0OOOO0O0O00O )#line:43
            O0O00O0O0O0O00OOO .get ('conn_test')#line:44
            print ('✅redis连接成功')#line:45
            return O0O00O0O0O0O00OOO #line:46
        except :#line:47
            print ("⚠️redis连接异常")#line:48
    except :#line:49
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:50
        sys .exit ()#line:51
def getToken (O0O0OOO0O000OO0O0 ,r =None ):#line:53
    OOO00O00O00OO0O00 =f'{activityUrl.split("com/")[0]}com'#line:54
    try :#line:55
        OOOO0O00O0000OOOO =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0O0OOO0O000OO0O0 )[0 ])#line:57
    except :#line:58
        OOOO0O00O0000OOOO =O0O0OOO0O000OO0O0 [:15 ]#line:60
    try :#line:61
        if r is not None :#line:62
            O0OOO0OO0O00O0OOO =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO0O00O0000OOOO}')#line:63
            if O0OOO0OO0O00O0OOO is not None :#line:65
                print (f"♻️获取缓存Token")#line:66
                return O0OOO0OO0O00O0OOO #line:67
            else :#line:68
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0OOO0O000OO0O0 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:80
                OO0O0O0000000OOOO =sign ({"url":f"{OOO00O00O00OO0O00}","id":""},'isvObfuscator')#line:81
                O00000O000O00OOO0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:83
                if O00000O000O00OOO0 .status_code !=200 :#line:84
                    print (O00000O000O00OOO0 .status_code )#line:85
                    return #line:86
                else :#line:87
                    if "参数异常"in O00000O000O00OOO0 .text :#line:88
                        return #line:89
                O0O00OO000OOOOO00 =O00000O000O00OOO0 .json ()['token']#line:90
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO0O00O0000OOOO}',O0O00OO000OOOOO00 ,ex =1800 ):#line:92
                    print ("✅Token缓存成功")#line:93
                else :#line:94
                    print ("❌Token缓存失败")#line:95
                return O0O00OO000OOOOO00 #line:96
        else :#line:97
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0OOO0O000OO0O0 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:108
            OO0O0O0000000OOOO =sign ({"url":f"{OOO00O00O00OO0O00}","id":""},'isvObfuscator')#line:109
            O00000O000O00OOO0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:111
            if O00000O000O00OOO0 .status_code !=200 :#line:112
                print (O00000O000O00OOO0 .status_code )#line:113
                return #line:114
            else :#line:115
                if "参数异常"in O00000O000O00OOO0 .text :#line:116
                    return #line:117
            O0OOO0OO0O00O0OOO =O00000O000O00OOO0 .json ()['token']#line:118
            print (f"✅获取实时Token")#line:119
            return O0OOO0OO0O00O0OOO #line:120
    except :#line:121
        return #line:122
def getJdTime ():#line:124
    OO00O00000OO0OO00 =int (round (time .time ()*1000 ))#line:125
    return OO00O00000OO0OO00 #line:126
def randomString (O0O00OOO0O000000O ,flag =False ):#line:128
    O0000O000O000OOOO ="0123456789abcdef"#line:129
    if flag :O0000O000O000OOOO =O0000O000O000OOOO .upper ()#line:130
    O0OOO00O00OOO000O =[random .choice (O0000O000O000OOOO )for _O0O000000O0000O00 in range (O0O00OOO0O000000O )]#line:131
    return ''.join (O0OOO00O00OOO000O )#line:132
def refresh_cookies (OO00000O00OO0OOOO ):#line:134
    if OO00000O00OO0OOOO .cookies :#line:135
        O00OOO0O0O0OOO00O =OO00000O00OO0OOOO .cookies .get_dict ()#line:136
        O0OOO0000O0O0OOOO =[(O0OO00O00000OO0O0 +"="+O00OOO0O0O0OOO00O [O0OO00O00000OO0O0 ])for O0OO00O00000OO0O0 in O00OOO0O0O0OOO00O ]#line:137
        global activityCookie #line:138
        OO000OO0OOO0000OO =[O0OO000OOOO00OO00 for O0OO000OOOO00OO00 in activityCookie .split (';')if O0OO000OOOO00OO00 !='']#line:139
        for OOOO000000OOOOO0O in OO000OO0OOO0000OO :#line:140
            for OOO0O00OOO0OO0OOO in O0OOO0000O0O0OOOO :#line:141
                if OOOO000000OOOOO0O .split ('=')[0 ]==OOO0O00OOO0OO0OOO .split ('=')[0 ]:#line:142
                    if OOOO000000OOOOO0O .split ('=')[1 ]!=OOO0O00OOO0OO0OOO .split ('=')[1 ]:#line:143
                        OO000OO0OOO0000OO .remove (OOOO000000OOOOO0O )#line:144
        activityCookie =''.join (sorted ([(O0OOO00OOOOO0000O +";")for O0OOO00OOOOO0000O in list (set (OO000OO0OOO0000OO +O0OOO0000O0O0OOOO ))]))#line:145
def getActivity ():#line:147
    OO0O00OOO0O0000O0 =activityUrl #line:148
    O00O000O00O0O000O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:156
    O000O00O00O0000O0 =requests .request ("GET",OO0O00OOO0O0000O0 ,headers =O00O000O00O0O000O )#line:157
    if O000O00O00O0000O0 .status_code ==200 :#line:158
        if O000O00O00O0000O0 .cookies :#line:159
            O0OO000000OO0000O =O000O00O00O0000O0 .cookies .get_dict ()#line:160
            OOOO00O0000OO00O0 =[(O00OO00O00O00O00O +"="+O0OO000000OO0000O [O00OO00O00O00O00O ])for O00OO00O00O00O00O in O0OO000000OO0000O ]#line:161
            O00O0OOO0O0OOO0OO =''.join (sorted ([(O00O000O000O00OO0 +";")for O00O000O000O00OO0 in OOOO00O0000OO00O0 ]))#line:162
        return O00O0OOO0O0OOO0OO #line:163
    else :#line:164
        print (O000O00O00O0000O0 .status_code )#line:165
        print ("⚠️疑似ip黑了")#line:166
        sys .exit ()#line:167
def getOpenStatus ():#line:169
    O0000OOO0OOO0OO0O ="https://cjhy-isv.isvjcloud.com/assembleConfig/getOpenStatus"#line:170
    OO0OO0OOOO0O00OO0 =f'activityId={activityId}'#line:171
    OOOO0OO000O0OO00O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:184
    O0000O0O00000OO0O =requests .request ("POST",O0000OOO0OOO0OO0O ,headers =OOOO0OO000O0OO00O ,data =OO0OO0OOOO0O00OO0 )#line:185
def getSystemConfig ():#line:187
    O0OO0O00O0OO00OO0 ="https://cjhy-isv.isvjcloud.com/wxCommonInfo/getSystemConfig"#line:188
    O000O00OOO0OOOOO0 =f'activityId={activityId}&activityType='#line:189
    OO0OO0O0O0O000OOO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:202
    OOO0OO0O0O00OOO0O =requests .request ("POST",O0OO0O00O0OO00OO0 ,headers =OO0OO0O0O0O000OOO ,data =O000O00OOO0OOOOO0 )#line:203
    refresh_cookies (OOO0OO0O0O00OOO0O )#line:204
def getSimpleActInfoVo ():#line:206
    OO0OO0O0000O0O000 ="https://cjhy-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:207
    OOO00O0O000OO0OOO =f"activityId={activityId}"#line:208
    OOOO0O000OO00O00O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:221
    O00OO0O00OOOOO0O0 =requests .request ("POST",OO0OO0O0000O0O000 ,headers =OOOO0O000OO00O00O ,data =OOO00O0O000OO0OOO )#line:222
    refresh_cookies (O00OO0O00OOOOO0O0 )#line:223
    O0000OOOO0O0OOOO0 =O00OO0O00OOOOO0O0 .json ()#line:224
    if O0000OOOO0O0OOOO0 ['result']:#line:225
        return O0000OOOO0O0OOOO0 ['data']#line:226
    else :#line:227
        print (O0000OOOO0O0OOOO0 ['errorMessage'])#line:228
def getMyPing (O00O0OO0000000000 ):#line:230
    O0OOO0O0OO0000OO0 ="https://cjhy-isv.isvjcloud.com/customer/getMyPing"#line:231
    OOOO0O0OOO0OOO0O0 =f"userId={O00O0OO0000000000}&token={token}&fromType=APP&riskType=1"#line:232
    OO0O0OO0O0O00O000 ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:245
    O0O0O0000OO0O000O =requests .request ("POST",O0OOO0O0OO0000OO0 ,headers =OO0O0OO0O0O00O000 ,data =OOOO0O0OOO0OOO0O0 )#line:246
    refresh_cookies (O0O0O0000OO0O000O )#line:247
    OOO00OOOOO000000O =O0O0O0000OO0O000O .json ()#line:248
    if OOO00OOOOO000000O ['result']:#line:249
        return OOO00OOOOO000000O ['data']['nickname'],OOO00OOOOO000000O ['data']['secretPin']#line:250
    else :#line:251
        print (f"⚠️{OOO00OOOOO000000O['errorMessage']}")#line:252
def getMemberLevel (OOO0O0O0O0OO000O0 ,OOOO0OOO00O00OO00 ):#line:254
    O00O00O0000OOO00O ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/getMemberLevel"#line:255
    O0O000000O0O00000 =f"venderId={OOO0O0O0O0OO000O0}&pin={quote_plus(OOOO0OOO00O00OO00)}"#line:256
    OO0OO0O00OOO0OOOO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:269
    O0O00000O0000O00O =requests .request ("POST",O00O00O0000OOO00O ,headers =OO0OO0O00OOO0OOOO ,data =O0O000000O0O00000 )#line:270
    refresh_cookies (O0O00000O0000O00O )#line:271
    O000000O00000OO00 =O0O00000O0000O00O .json ()#line:272
    if O000000O00000OO00 ['result']:#line:273
        return O000000O00000OO00 ['data']#line:274
    else :#line:275
        print (O000000O00000OO00 ['errorMessage'])#line:276
def getOpenCardInfo (OOOO0000OOOO000O0 ,O0O0OO0O000OO00OO ,OOOOOOOO0OO0000OO ):#line:278
    O0O00O0O0O0OOO00O ="https://cjhy-isv.isvjcloud.com/mc/new/brandCard/common/shopAndBrand/getOpenCardInfo"#line:279
    O0000O0OOOO0O0O00 =f"venderId={OOOO0000OOOO000O0}&buyerPin={quote_plus(O0O0OO0O000OO00OO)}&activityType={OOOOOOOO0OO0000OO}"#line:280
    O0O00OO00OOO0O00O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:293
    O00O000OOO000O000 =requests .request ("POST",O0O00O0O0O0OOO00O ,headers =O0O00OO00OOO0O00O ,data =O0000O0OOOO0O0O00 )#line:294
    O0000OO00O0O00OOO =O00O000OOO000O000 .json ()#line:295
    if O0000OO00O0O00OOO ['result']:#line:296
        return O0000OO00O0O00OOO ['data']#line:297
    else :#line:298
        print (O0000OO00O0O00OOO ['errorMessage'])#line:299
def accessLog (OOOOO00000O0OO0O0 ,OOOOOOO00O00OOO00 ,OO00OO000OOOOO00O ):#line:301
    OO00000000OOOOOOO ="https://cjhy-isv.isvjcloud.com/common/accessLog"#line:302
    O0000O0O0OO0O0000 =f"venderId={OOOOO00000O0OO0O0}&code={OO00OO000OOOOO00O}&pin={quote_plus(OOOOOOO00O00OOO00)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType="#line:303
    OO000000000O0000O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:316
    requests .request ("POST",OO00000000OOOOOOO ,headers =OO000000000O0000O ,data =O0000O0O0OO0O0000 )#line:317
def activityContent (O0O0OOOOOOO00OOOO ,O00000O0O00OOOOOO ):#line:319
    O0OO0O0000OO00OOO ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/activityContent"#line:320
    OO0O00OO0OOO0OOO0 =f"activityId={activityId}&pin={quote_plus(O0O0OOOOOOO00OOOO)}&level={O00000O0O00OOOOOO}"#line:321
    OO0OOO00OO00O00OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:334
    O0OOOO0OOO00OO0OO =requests .request ("POST",O0OO0O0000OO00OOO ,headers =OO0OOO00OO00O00OO ,data =OO0O00OO0OOO0OOO0 )#line:335
    refresh_cookies (O0OOOO0OOO00OO0OO )#line:336
    O0O00O000000OO000 =O0OOOO0OOO00OO0OO .json ()#line:337
    if O0O00O000000OO000 ['result']:#line:338
        OO0OO0OO00000OOO0 =O0O00O000000OO000 ['data']['endTime']#line:339
        if getJdTime ()>OO0OO0OO00000OOO0 :#line:340
            print ("⛈活动已结束,下次早点来~")#line:341
            sys .exit ()#line:342
        return O0O00O000000OO000 ['data']#line:343
    else :#line:344
        print (f"⛈{O0O00O000000OO000['errorMessage']}")#line:345
def getInfo ():#line:347
    OO00O0OOO00000000 =f"https://cjhy-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"#line:348
    O00OO0OO000OO00OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:361
    OO0000O0OO0O00O00 =requests .request ("GET",OO00O0OOO00000000 ,headers =O00OO0OO000OO00OO )#line:362
    refresh_cookies (OO0000O0OO0O00O00 )#line:363
def getBirthInfo (OO0O00OO000OO0OO0 ,O0O000O0OO0O0OOO0 ):#line:365
    OOO00OOOO00O0O0O0 ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/getBirthInfo"#line:366
    O000000O0000O00O0 =f"venderId={OO0O00OO000OO0OO0}&pin={quote_plus(O0O000O0OO0O0OOO0)}"#line:367
    O000O000OOOO00OOO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:380
    O0OOOOOO00OO00OO0 =requests .request ("POST",OOO00OOOO00O0O0O0 ,headers =O000O000OOOO00OOO ,data =O000000O0000O00O0 )#line:381
    refresh_cookies (O0OOOOOO00OO00OO0 )#line:382
def saveBirthDay (OOO000OOO0OO00OOO ,OO0OO000OOOO000O0 ):#line:384
    O000O0000000O00OO ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/saveBirthDay"#line:385
    OOOO000O00000OO00 =f"venderId={OOO000OOO0OO00OOO}&pin={quote_plus(OO0OO000OOOO000O0)}&birthDay={str(datetime.now())[:10]}"#line:386
    O00OO0OOO00OOO0OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:399
    O0O0OOOO0O00OO000 =requests .request ("POST",O000O0000000O00OO ,headers =O00OO0OOO00OOO0OO ,data =OOOO000O00000OO00 )#line:400
    refresh_cookies (O0O0OOOO0O00OO000 )#line:401
def sendBirthGifts (OO0OOO00O0O0O0OO0 ,OO0OO0O0000O0OO0O ,OOOOOO000000OO0OO ):#line:403
    O0O0O0OOO0O0O0OOO ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/sendBirthGifts"#line:404
    OO00OOOO0OOOO0OOO =f"venderId={OO0OOO00O0O0O0OO0}&pin={quote_plus(OO0OO0O0000O0OO0O)}&activityId={activityId}&level={OOOOOO000000OO0OO}"#line:405
    OOOOO00OO0OOOOO0O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:418
    OOO000OO0OOO00OOO =requests .request ("POST",O0O0O0OOO0O0O0OOO ,headers =OOOOO00OO0OOOOO0O ,data =OO00OOOO0OOOO0OOO )#line:419
    refresh_cookies (OOO000OO0OOO00OOO )#line:420
    O000OO00O00OOO00O =OOO000OO0OOO00OOO .json ()#line:421
    if O000OO00O00OOO00O ['result']:#line:422
        return O000OO00O00OOO00O ['data']#line:423
    else :#line:424
        print (f"⛈{O000OO00O00OOO00O['errorMessage']}")#line:425
def sendLevelGifts (O0O000O0O0000OOO0 ,OO0OO00000OOOO0OO ,OOO00O0OO0O00O000 ):#line:427
    O0O000O0OOOO0OO00 ="https://cjhy-isv.isvjcloud.com/mc/wxMcLevelAndBirthGifts/sendLevelGifts"#line:428
    OO0O0OOO00O000000 =f"venderId={O0O000O0O0000OOO0}&pin={quote_plus(OO0OO00000OOOO0OO)}&activityId={activityId}&level={OOO00O0OO0O00O000}"#line:429
    OO0000O0000OOOO00 ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:442
    OOO000OOOOO0O0OO0 =requests .request ("POST",O0O000O0OOOO0OO00 ,headers =OO0000O0000OOOO00 ,data =OO0O0OOO00O000000 )#line:443
    refresh_cookies (OOO000OOOOO0O0OO0 )#line:444
    O000O00O0O0O00O0O =OOO000OOOOO0O0OO0 .json ()#line:445
    if O000O00O0O0O00O0O ['result']:#line:446
        return O000O00O0O0O00O0O ['data']#line:447
    else :#line:448
        print (f"⛈{O000O00O0O0O00O0O['errorMessage']}")#line:449
if __name__ =='__main__':#line:452
    r =redis_conn ()#line:453
    try :#line:454
        cks =getCk #line:455
        if not cks :#line:456
            sys .exit ()#line:457
    except :#line:458
        print ("未获取到有效COOKIE,退出程序！")#line:459
        sys .exit ()#line:460
    num =0 #line:461
    for cookie in cks [:]:#line:462
        num +=1 #line:463
        if num %9 ==0 :#line:464
            print ("⏰等待5s,休息一下")#line:465
            time .sleep (5 )#line:466
        global ua ,activityCookie ,token #line:467
        ua =userAgent ()#line:468
        try :#line:469
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:470
            pt_pin =unquote_plus (pt_pin )#line:471
        except IndexError :#line:472
            pt_pin =f'用户{num}'#line:473
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:474
        print (datetime .now ())#line:475
        token =getToken (cookie ,r )#line:476
        if token is None :#line:477
            print (f"⚠️获取Token失败！⏰等待2s")#line:478
            time .sleep (2 )#line:479
            continue #line:480
        time .sleep (0.2 )#line:481
        activityCookie =getActivity ()#line:482
        time .sleep (0.3 )#line:483
        getOpenStatus ()#line:484
        time .sleep (0.2 )#line:485
        getSimAct =getSimpleActInfoVo ()#line:486
        venderId =getSimAct ['venderId']#line:487
        activityType =getSimAct ['activityType']#line:488
        time .sleep (0.3 )#line:489
        getPin =getMyPing (venderId )#line:490
        if getPin :#line:491
            nickname =getPin [0 ]#line:492
            secretPin =getPin [1 ]#line:493
            time .sleep (0.3 )#line:494
            getOC =getOpenCardInfo (venderId ,secretPin ,activityType )#line:495
            time .sleep (0.2 )#line:496
            if getOC ['openedCard']:#line:497
                memberLev =getMemberLevel (venderId ,secretPin )#line:498
                if memberLev :#line:499
                    level =memberLev ['level']#line:500
                    shopTitle =memberLev ['shopTitle']#line:501
                    print (f"✅开启{shopTitle} 生日等级礼包")#line:502
                    time .sleep (0.2 )#line:503
                    accessLog (venderId ,secretPin ,activityType )#line:504
                    time .sleep (0.2 )#line:505
                    actContent =activityContent (secretPin ,level )#line:506
                    if actContent :#line:507
                        if actContent ['isReceived']==1 :#line:508
                            print (f"💨{nickname} 今年已经领过了,明年再来吧~")#line:509
                            continue #line:510
                        else :#line:511
                            time .sleep (0.2 )#line:512
                            getInfo ()#line:513
                            time .sleep (0.2 )#line:514
                            try :#line:515
                                if activityType ==104 :#line:516
                                    sendGift =sendLevelGifts (venderId ,secretPin ,level )#line:517
                                    levelResult =sendGift ['levelResult']#line:518
                                    if levelResult :#line:519
                                        levelData =sendGift ['levelData']#line:520
                                        gifts =[(f"{O00OOO0000OO0O00O['beanNum']}{O00OOO0000OO0O00O['name']}")for O00OOO0000OO0O00O in levelData ]#line:521
                                        print (f"🎉🎉🎉{nickname} 成功领取 {','.join(gifts)}")#line:522
                                    else :#line:523
                                        print (f"💨{nickname} 生日等级礼包领取失败,请重试~")#line:524
                                else :#line:525
                                    getBirthInfo (venderId ,secretPin )#line:526
                                    time .sleep (0.2 )#line:527
                                    saveBirthDay (venderId ,secretPin )#line:528
                                    time .sleep (0.2 )#line:529
                                    sendGift =sendBirthGifts (venderId ,secretPin ,level )#line:530
                                    birthdayResult =sendGift ['birthdayResult']#line:531
                                    if birthdayResult :#line:532
                                        birthdayData =sendGift ['birthdayData']#line:533
                                        gifts =[(f"{O0OOOO00O0O0OO00O['beanNum']}{O0OOOO00O0O0OO00O['name']}")for O0OOOO00O0O0OO00O in birthdayData ]#line:534
                                        print (f"🎉🎉🎉{nickname} 成功领取 {','.join(gifts)}")#line:535
                                    else :#line:536
                                        print (f"💨{nickname} 生日等级礼包领取失败,请重试~")#line:537
                            except :#line:538
                                print (f"💨{nickname} 生日等级礼包领取失败,请重试~")#line:539
            else :#line:540
                print (f"⛈{nickname} 非店铺会员无法领取生日等级礼包！")#line:541
                continue #line:542
        time .sleep (1.5 )