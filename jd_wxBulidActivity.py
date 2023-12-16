#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxBulidActivity.py(盖楼有礼-监控脚本)
Author: HarbourJ
Date: 2022/9/18 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('盖楼有礼-JK');
ActivityEntry: https://lzkj-isv.isvjcloud.com/wxBuildActivity/activity?activityId=4bde809b95ec45a3b50f7086d77f3178
            变量: export jd_wxBulidActivityId="活动🆔"
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
activityId =os .environ .get ("jd_wxBulidActivityId")if os .environ .get ("jd_wxBulidActivityId")else ""#line:24
if not activityId :#line:26
    print ("⚠️未发现有效盖楼有礼活动变量,退出程序!")#line:27
    sys .exit ()#line:28
activityUrl =f"https://lzkj-isv.isvjcloud.com/wxBuildActivity/activity?activityId={activityId}"#line:29
def redis_conn ():#line:31
    try :#line:32
        import redis #line:33
        try :#line:34
            OO0O00O0000OOOOOO =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:35
            O0O0OO0O0O00O0O0O =redis .Redis (connection_pool =OO0O00O0000OOOOOO )#line:36
            O0O0OO0O0O00O0O0O .get ('conn_test')#line:37
            print ('✅redis连接成功')#line:38
            return O0O0OO0O0O00O0O0O #line:39
        except :#line:40
            print ("⚠️redis连接异常")#line:41
    except :#line:42
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:43
        sys .exit ()#line:44
def getToken (O0OOO00O0O000O00O ,r =None ):#line:46
    O0OOOO0OO00000O0O =f'{activityUrl.split("com/")[0]}com'#line:47
    try :#line:48
        OO000O0OO0OOOOOOO =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0OOO00O0O000O00O )[0 ])#line:50
    except :#line:51
        OO000O0OO0OOOOOOO =O0OOO00O0O000O00O [:15 ]#line:53
    try :#line:54
        if r is not None :#line:55
            OOOO0O000O000O0OO =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO000O0OO0OOOOOOO}')#line:56
            if OOOO0O000O000O0OO is not None :#line:58
                print (f"♻️获取缓存Token")#line:59
                return OOOO0O000O000O0OO #line:60
            else :#line:61
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0OOO00O0O000O00O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:73
                OO0OO00OO0O00OO0O =sign ({"url":f"{O0OOOO0OO00000O0O}","id":""},'isvObfuscator')#line:74
                OO00OOO0OOOOO0OOO =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:76
                if OO00OOO0OOOOO0OOO .status_code !=200 :#line:77
                    print (OO00OOO0OOOOO0OOO .status_code )#line:78
                    return #line:79
                else :#line:80
                    if "参数异常"in OO00OOO0OOOOO0OOO .text :#line:81
                        return #line:82
                O0O0OOO0OO0000O00 =OO00OOO0OOOOO0OOO .json ()['token']#line:83
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO000O0OO0OOOOOOO}',O0O0OOO0OO0000O00 ,ex =1800 ):#line:85
                    print ("✅Token缓存成功")#line:86
                else :#line:87
                    print ("❌Token缓存失败")#line:88
                return O0O0OOO0OO0000O00 #line:89
        else :#line:90
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0OOO00O0O000O00O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:101
            OO0OO00OO0O00OO0O =sign ({"url":f"{O0OOOO0OO00000O0O}","id":""},'isvObfuscator')#line:102
            OO00OOO0OOOOO0OOO =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:104
            if OO00OOO0OOOOO0OOO .status_code !=200 :#line:105
                print (OO00OOO0OOOOO0OOO .status_code )#line:106
                return #line:107
            else :#line:108
                if "参数异常"in OO00OOO0OOOOO0OOO .text :#line:109
                    return #line:110
            OOOO0O000O000O0OO =OO00OOO0OOOOO0OOO .json ()['token']#line:111
            print (f"✅获取实时Token")#line:112
            return OOOO0O000O000O0OO #line:113
    except :#line:114
        return #line:115
def getJdTime ():#line:117
    O00OO0OO0OO0OOOOO =int (round (time .time ()*1000 ))#line:118
    return O00OO0OO0OO0OOOOO #line:119
def randomString (OO00O00OOOOOO0O0O ,flag =False ):#line:121
    O00000O000O0OO0OO ="0123456789abcdef"#line:122
    if flag :O00000O000O0OO0OO =O00000O000O0OO0OO .upper ()#line:123
    OO0O00O00000O0OO0 =[random .choice (O00000O000O0OO0OO )for _OO00000000OO0O00O in range (OO00O00OOOOOO0O0O )]#line:124
    return ''.join (OO0O00O00000O0OO0 )#line:125
def refresh_cookies (O0OOOOO0O0O00000O ):#line:127
    if O0OOOOO0O0O00000O .cookies :#line:128
        O0OO000O000OOOOO0 =O0OOOOO0O0O00000O .cookies .get_dict ()#line:129
        OOOO0OOOOOO0O000O =[(O0O00OOO000O0OO0O +"="+O0OO000O000OOOOO0 [O0O00OOO000O0OO0O ])for O0O00OOO000O0OO0O in O0OO000O000OOOOO0 ]#line:130
        global activityCookie #line:131
        O000O0OOOO0000O0O =[O0000O00OOOOO0O00 for O0000O00OOOOO0O00 in activityCookie .split (';')if O0000O00OOOOO0O00 !='']#line:132
        for O0O00000OO000OOOO in O000O0OOOO0000O0O :#line:133
            for O00000OO0O0O000O0 in OOOO0OOOOOO0O000O :#line:134
                if O0O00000OO000OOOO .split ('=')[0 ]==O00000OO0O0O000O0 .split ('=')[0 ]:#line:135
                    if O0O00000OO000OOOO .split ('=')[1 ]!=O00000OO0O0O000O0 .split ('=')[1 ]:#line:136
                        O000O0OOOO0000O0O .remove (O0O00000OO000OOOO )#line:137
        activityCookie =''.join (sorted ([(O0OOO00O00O0OO0OO +";")for O0OOO00O00O0OO0OO in list (set (O000O0OOOO0000O0O +OOOO0OOOOOO0O000O ))]))#line:138
def getActivity ():#line:140
    OO0O0OOO0OO000OO0 =f"https://lzkj-isv.isvjcloud.com/wxBuildActivity/activity?activityId={activityId}"#line:141
    O0O0OO000O0O0OOOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:149
    O0O0OO000O0OOO0O0 =requests .request ("GET",OO0O0OOO0OO000OO0 ,headers =O0O0OO000O0O0OOOO )#line:150
    if O0O0OO000O0OOO0O0 .status_code ==200 :#line:151
        if O0O0OO000O0OOO0O0 .cookies :#line:152
            OO000O0OO00O0O0OO =O0O0OO000O0OOO0O0 .cookies .get_dict ()#line:153
            O0O00000OO00OO0OO =[(O0OO000000OOO0O0O +"="+OO000O0OO00O0O0OO [O0OO000000OOO0O0O ])for O0OO000000OOO0O0O in OO000O0OO00O0O0OO ]#line:154
            O0O00OO0OOOOO0000 =''.join (sorted ([(OO00O0OOOO0O0000O +";")for OO00O0OOOO0O0000O in O0O00000OO00OO0OO ]))#line:155
        return O0O00OO0OOOOO0000 #line:156
    else :#line:157
        print (O0O0OO000O0OOO0O0 .status_code ,"⚠️疑似ip黑了")#line:158
        sys .exit ()#line:159
def getSystemConfigForNew ():#line:161
    OOO0OOO0OO00000OO ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:162
    OOO0000O0O00OO0OO =f'activityId={activityId}&activityType=65'#line:163
    OOO0000OO0O0O000O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:176
    OOO0OOO0OO00OOOO0 =requests .request ("POST",OOO0OOO0OO00000OO ,headers =OOO0000OO0O0O000O ,data =OOO0000O0O00OO0OO )#line:177
    refresh_cookies (OOO0OOO0OO00OOOO0 )#line:178
def getSimpleActInfoVo ():#line:180
    O00O0OOOOO0OO0O00 ="https://lzkj-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:181
    O00O0OOOOO00OO0OO =f"activityId={activityId}"#line:182
    OO0OO0OOOO0O0OOOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:195
    OO0O0O00OOOOOOO00 =requests .request ("POST",O00O0OOOOO0OO0O00 ,headers =OO0OO0OOOO0O0OOOO ,data =O00O0OOOOO00OO0OO )#line:196
    refresh_cookies (OO0O0O00OOOOOOO00 )#line:197
    O0O0OOOO0O000O0O0 =OO0O0O00OOOOOOO00 .json ()#line:198
    if O0O0OOOO0O000O0O0 ['result']:#line:199
        return O0O0OOOO0O000O0O0 ['data']#line:200
def getMyPing (OO00O00000OOOOO00 ):#line:202
    O00O0O00OOOOO0000 ="https://lzkj-isv.isvjcloud.com/customer/getMyPing"#line:203
    O0O00O000O0O000OO =f"userId={OO00O00000OOOOO00}&token={token}&fromType=APP"#line:204
    O00OOO00OO00O0O00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:217
    OOOOOO000OO0OOO0O =requests .request ("POST",O00O0O00OOOOO0000 ,headers =O00OOO00OO00O0O00 ,data =O0O00O000O0O000OO )#line:218
    refresh_cookies (OOOOOO000OO0OOO0O )#line:219
    OO00OO00O0O00OO00 =OOOOOO000OO0OOO0O .json ()#line:220
    if OO00OO00O0O00OO00 ['result']:#line:221
        return OO00OO00O0O00OO00 ['data']['nickname'],OO00OO00O0O00OO00 ['data']['secretPin']#line:222
    else :#line:223
        print (f"⚠️{OO00OO00O0O00OO00['errorMessage']}")#line:224
def accessLogWithAD (OO0O00000O0O0OOO0 ,O00OOO00O0000O000 ):#line:226
    OOO0OOO0O00OO00OO ="https://lzkj-isv.isvjcloud.com/common/accessLogWithAD"#line:227
    O00OO0OOOOOOO00O0 =f"venderId={OO0O00000O0O0OOO0}&code=65&pin={quote_plus(O00OOO00O0000O000)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource="#line:228
    O00OO00OOOO0OO000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:241
    O0000OO0O00O0O000 =requests .request ("POST",OOO0OOO0O00OO00OO ,headers =O00OO00OOOO0OO000 ,data =O00OO0OOOOOOO00O0 )#line:242
    refresh_cookies (O0000OO0O00O0O000 )#line:243
def activityContent (O000O00O00OO0OOO0 ):#line:245
    O0OOO0O00OO0OOOOO ="https://lzkj-isv.isvjcloud.com/wxBuildActivity/activityContent"#line:246
    O0OO00000O0OO0O00 =f"activityId={activityId}&pin={quote_plus(O000O00O00OO0OOO0)}"#line:247
    O000O0000O00OOO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:260
    O00O00O000O00OO0O =requests .request ("POST",O0OOO0O00OO0OOOOO ,headers =O000O0000O00OOO00 ,data =O0OO00000O0OO0O00 )#line:261
    refresh_cookies (O00O00O000O00OO0O )#line:262
    OO0O000000O000O0O =O00O00O000O00OO0O .json ()#line:263
    if OO0O000000O000O0O ['result']:#line:264
        O0000OOOO0O00O00O =OO0O000000O000O0O ['data']['currentFloors']#line:265
        O00O0O0OOOO000OOO =OO0O000000O000O0O ['data']['totalJoinMans']#line:266
        OOO00O000O0000OOO =OO0O000000O000O0O ['data']['drawOkMans']#line:267
        O00O0OOO00000O0O0 =OO0O000000O000O0O ['data']['drawInfos']#line:268
        OOOO000O0O00O0OO0 =' '.join ([O000OO0OO0000O0OO ['priceInfo']for O000OO0OO0000O0OO in O00O0OOO00000O0O0 ])#line:269
        OOO0O0O0OO000OOO0 =' '.join ([O000OO00O0O0O0000 ['name']for O000OO00O0O0O0000 in O00O0OOO00000O0O0 ])#line:270
        return O0000OOOO0O00O00O ,O00O0O0OOOO000OOO ,OOO00O000O0000OOO ,OOOO000O0O00O0OO0 ,OOO0O0O0OO000OOO0 #line:271
    else :#line:272
        print (f"⛈{OO0O000000O000O0O['errorMessage']}")#line:273
        sys .exit ()#line:274
def getShopInfoVO (O0O00O0OO0O00000O ):#line:276
    O00OOO00O00O00O00 ="https://lzkj-isv.isvjcloud.com/wxActionCommon/getShopInfoVO"#line:277
    O0OO00O0OO0OO00OO =f"userId={O0O00O0OO0O00000O}"#line:278
    O00O0O0OO0OO0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:291
    O0000O0O0OO0OO00O =requests .request ("POST",O00OOO00O00O00O00 ,headers =O00O0O0OO0OO0O0OO ,data =O0OO00O0OO0OO00OO )#line:292
    refresh_cookies (O0000O0O0OO0OO00O )#line:293
    OO0OOO00OOOO00O00 =O0000O0O0OO0OO00O .json ()#line:294
    if OO0OOO00OOOO00O00 ['result']:#line:295
        OOOO00OOO0OO0000O =OO0OOO00OOOO00O00 ['data']['shopName']#line:296
        return OOOO00OOO0OO0000O #line:297
    else :#line:298
        print (f"⛈{OO0OOO00OOOO00O00['errorMessage']}")#line:299
def getActMemberInfo (OO0OO0O00O00O0O0O ,O0O0O00O00OO0OOO0 ):#line:301
    OOO0OOOOOOOOOOO0O ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getActMemberInfo"#line:302
    O00O00O00O000OOOO =f"venderId={OO0OO0O00O00O0O0O}&activityId={activityId}&pin={quote_plus(O0O0O00O00OO0OOO0)}"#line:303
    OO00O0OOOOOOOOOOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:316
    O00OOO0OOOOO0OOOO =requests .request ("POST",OOO0OOOOOOOOOOO0O ,headers =OO00O0OOOOOOOOOOO ,data =O00O00O00O000OOOO )#line:317
    refresh_cookies (O00OOO0OOOOO0OOOO )#line:318
    O0O0OO0O0O0OO00O0 =O00OOO0OOOOO0OOOO .json ()#line:319
    if O0O0OO0O0O0OO00O0 ['result']:#line:320
        O00O0O00OO00O0O0O =O0O0OO0O0O0OO00O0 ['data']['openCard']#line:321
        return O00O0O00OO00O0O0O #line:322
    else :#line:323
        print (f"⛈{O0O0OO0O0O0OO00O0['errorMessage']}")#line:324
def miniProgramShareInfo ():#line:326
    OOOOOO0OOOO0000OO =f"https://lzkj-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityUrl}"#line:327
    OOOOO00OOOO00O000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:338
    O0OO0O0O0OOOOO0O0 =requests .request ("GET",OOOOOO0OOOO0000OO ,headers =OOOOO00OOOO00O000 )#line:339
    refresh_cookies (O0OO0O0O0OOOOO0O0 )#line:340
def getPublishs (OOO0OO0O0O00000OO ):#line:342
    OOO000000OO00O00O ="https://lzkj-isv.isvjcloud.com/wxBuildActivity/getPublishs"#line:343
    O00000000O0000OO0 =f"activityId={activityId}&pin={quote_plus(OOO0OO0O0O00000OO)}&pageNo=1&pageSize=10"#line:344
    O00000O000OO0OOOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:357
    O0O0OO0O00OO00OOO =requests .request ("POST",OOO000000OO00O00O ,headers =O00000O000OO0OOOO ,data =O00000000O0000OO0 )#line:358
    refresh_cookies (O0O0OO0O00OO00OOO )#line:359
def currentFloor (O0000O00OOO0OO000 ):#line:361
    O00OOO00OOO0O00OO ="https://lzkj-isv.isvjcloud.com/wxBuildActivity/currentFloor"#line:362
    OO00O0OO0OO0O0000 =f"activityId={activityId}&pin={quote_plus(O0000O00OOO0OO000)}&pageNo=1&pageSize=10"#line:363
    O0O0OOO0OOO0O00OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:376
    OOOO000O00OO0O0OO =requests .request ("POST",O00OOO00OOO0O00OO ,headers =O0O0OOO0OOO0O00OO ,data =OO00O0OO0OO0O0000 )#line:377
    refresh_cookies (OOOO000O00OO0O0OO )#line:378
    OOO000OOO00000OOO =OOOO000O00OO0O0OO .json ()#line:379
    if OOO000OOO00000OOO ['result']:#line:380
        OO0OOOOOO0OOOOO0O =OOO000OOO00000OOO ['data']['currentFloors']#line:381
        return OO0OOOOOO0OOOOO0O #line:382
    else :#line:383
        print (f"⛈{OOO000OOO00000OOO['errorMessage']}")#line:384
def publish (O0OO000OOO000OO00 ):#line:386
    OO0O00000O000OOOO ="https://lzkj-isv.isvjcloud.com/wxBuildActivity/publish"#line:387
    O00O000OO0O000O0O =f"activityId={activityId}&pin={quote_plus(O0OO000OOO000OO00)}&content={quote_plus('必中冲冲冲')}"#line:388
    OO00OOO00OOOOOO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:401
    OOO0OOO00O00OOO00 =requests .request ("POST",OO0O00000O000OOOO ,headers =OO00OOO00OOOOOO00 ,data =O00O000OO0O000O0O )#line:402
    refresh_cookies (OOO0OOO00O00OOO00 )#line:403
    O0O00OOOO000O00O0 =OOO0OOO00O00OOO00 .json ()#line:404
    if O0O00OOOO000O00O0 ['result']:#line:405
        O0OOOOO0OO0000OOO =O0O00OOOO000O00O0 ['data']['currentFloors']#line:406
        OOOO0OOO00OO0OO0O =O0O00OOOO000O00O0 ['data']['drawResult']['drawInfo']#line:407
        if OOOO0OOO00OO0OO0O :#line:408
            print (f"🏗当前楼层{O0OOOOO0OO0000OOO} 🎉{OOOO0OOO00OO0OO0O['name']}")#line:409
            return OOOO0OOO00OO0OO0O ['name']#line:410
        else :#line:411
            print (f"🏗当前楼层{O0OOOOO0OO0000OOO} 💨💨💨")#line:412
            return 2 #line:413
    else :#line:414
        print (f"⛈{O0O00OOOO000O00O0['errorMessage']}")#line:415
        return 3 #line:416
if __name__ =='__main__':#line:419
    r =redis_conn ()#line:420
    try :#line:421
        cks =getCk #line:422
        if not cks :#line:423
            sys .exit ()#line:424
    except :#line:425
        print ("未获取到有效COOKIE,退出程序！")#line:426
        sys .exit ()#line:427
    num =0 #line:428
    for cookie in cks [:]:#line:429
        num +=1 #line:430
        if num %9 ==0 :#line:431
            print ("⏰等待5s,休息一下")#line:432
            time .sleep (5 )#line:433
        global ua ,activityCookie ,token #line:434
        ua =userAgent ()#line:435
        try :#line:436
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:437
            pt_pin =unquote_plus (pt_pin )#line:438
        except IndexError :#line:439
            pt_pin =f'用户{num}'#line:440
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:441
        print (datetime .now ())#line:442
        token =getToken (cookie ,r )#line:443
        if token is None :#line:444
            print (f"⚠️获取Token失败！⏰等待2s")#line:445
            time .sleep (2 )#line:446
            continue #line:447
        time .sleep (0.2 )#line:448
        activityCookie =getActivity ()#line:449
        time .sleep (0.5 )#line:450
        getSystemConfigForNew ()#line:451
        time .sleep (0.2 )#line:452
        getSimAct =getSimpleActInfoVo ()#line:453
        venderId =getSimAct ['venderId']#line:454
        time .sleep (0.2 )#line:455
        getPin =getMyPing (venderId )#line:456
        if getPin is not None :#line:457
            nickname =getPin [0 ]#line:458
            secretPin =getPin [1 ]#line:459
            time .sleep (0.3 )#line:460
            accessLogWithAD (venderId ,secretPin )#line:461
            time .sleep (0.2 )#line:462
            actCont =activityContent (secretPin )#line:463
            if not actCont :#line:465
                continue #line:466
            currentFloors =actCont [0 ]#line:467
            totalJoinMans =actCont [1 ]#line:468
            drawOkMans =actCont [2 ]#line:469
            priceInfo =actCont [3 ]#line:470
            pricename =actCont [4 ]#line:471
            time .sleep (0.3 )#line:472
            shopName =getShopInfoVO (venderId )#line:473
            if num ==1 :#line:474
                print (f"✅开启{shopName}-盖楼有礼活动")#line:475
                print (f"🎁奖品{pricename}")#line:476
            time .sleep (0.2 )#line:477
            getActMemberInfo (venderId ,secretPin )#line:478
            time .sleep (0.2 )#line:479
            miniProgramShareInfo ()#line:480
            time .sleep (0.2 )#line:481
            getPublishs (secretPin )#line:482
            time .sleep (0.2 )#line:483
            currentFloor (secretPin )#line:484
            time .sleep (0.2 )#line:485
            reward =publish (secretPin )#line:486
            if reward :#line:487
                if reward ==3 :#line:488
                    continue #line:489
                elif reward ==2 :#line:490
                    pass #line:491
                else :#line:492
                    reward #line:493
            time .sleep (1 )#line:494
            getPublishs (secretPin )#line:495
            time .sleep (0.2 )#line:496
            currentFloor (secretPin )#line:497
            time .sleep (0.2 )#line:498
            reward =publish (secretPin )#line:499
            if reward :#line:500
                if reward ==3 :#line:501
                    continue #line:502
                elif reward ==2 :#line:503
                    pass #line:504
                else :#line:505
                    reward #line:506
        time .sleep (5 )
