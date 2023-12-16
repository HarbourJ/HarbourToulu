#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxCollectionActivity.py(加购有礼-监控脚本)
Author: HarbourJ
Date: 2022/9/18 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('加购有礼-JK')
ActivityEntry: https://lzkj-isv.isvjd.com/wxCollectionActivity/activity2/df1bcc4c1e894444ae7579e124149999?activityId=df1bcc4c1e894444ae7579e124149999
Description: 本地sign算法+redis缓存Token
             变量: export jd_wxCollectionActivityUrl="https://lzkj-isv.isvjd.com/wxCollectionActivity/activity2/xxx?activityId=xxx" 变量值需要传入完整活动地址
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from datetime import datetime #line:2
from sendNotify import *#line:3
from urllib .parse import quote_plus ,unquote_plus #line:4
from functools import partial #line:5
print =partial (print ,flush =True )#line:6
import warnings #line:7
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:8
try :#line:9
    from jd_sign import *#line:10
except ImportError as e :#line:11
    print (e )#line:12
    if "No module"in str (e ):#line:13
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:14
    sys .exit ()#line:15
try :#line:16
    from jdCookie import get_cookies #line:17
    getCk =get_cookies ()#line:18
except :#line:19
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:20
    sys .exit (3 )#line:21
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:22
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:23
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:24
activity_url =os .environ .get ("jd_wxCollectionActivityUrl")if os .environ .get ("jd_wxCollectionActivityUrl")else ""#line:25
runNums =os .environ .get ("jd_wxCollectionActivityRunNums")if os .environ .get ("jd_wxCollectionActivityRunNums")else 10 #line:26
if not activity_url or "wxCollectionActivity/activity"not in activity_url :#line:28
    print ("⚠️未发现有效加购有礼活动变量,退出程序!")#line:29
    sys .exit ()#line:30
activityUrl =activity_url .replace ('isvjd','isvjcloud').split ('&')[0 ]#line:31
activityId =activityUrl .split ('activityId=')[1 ]#line:32
print (f"【🛳活动入口】{activityUrl}\n")#line:33
runNums =int (runNums )#line:34
if runNums ==10 :#line:35
    print ('🤖本次加购默认跑前10个账号,设置自定义变量:export jd_wxCollectionActivityRunNums="需要运行加购的ck数量"')#line:36
else :#line:37
    print (f'🤖本次运行前{runNums}个账号')#line:38
def redis_conn ():#line:41
    try :#line:42
        import redis #line:43
        try :#line:44
            O000O00O0OO000OOO =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:45
            O00OO00O0OO0O000O =redis .Redis (connection_pool =O000O00O0OO000OOO )#line:46
            O00OO00O0OO0O000O .get ('conn_test')#line:47
            print ('✅redis连接成功')#line:48
            return O00OO00O0OO0O000O #line:49
        except :#line:50
            print ("⚠️redis连接异常")#line:51
    except :#line:52
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:53
        sys .exit ()#line:54
def getToken (O0O0O0O0O0O0OO000 ,r =None ):#line:56
    O0000O0OO0O0000O0 =f'{activityUrl.split("com/")[0]}com'#line:57
    try :#line:58
        OOO0000O0OO00OOO0 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0O0O0O0O0O0OO000 )[0 ])#line:60
    except :#line:61
        OOO0000O0OO00OOO0 =O0O0O0O0O0O0OO000 [:15 ]#line:63
    try :#line:64
        if r is not None :#line:65
            OO00O0O000000O0OO =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOO0000O0OO00OOO0}')#line:66
            if OO00O0O000000O0OO is not None :#line:68
                print (f"♻️获取缓存Token")#line:69
                return OO00O0O000000O0OO #line:70
            else :#line:71
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0O0O0O0O0OO000 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:83
                O0OO000OOO0OOO0OO =sign ({"url":f"{O0000O0OO0O0000O0}","id":""},'isvObfuscator')#line:84
                OO0O0O00OO0O0O0O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:86
                if OO0O0O00OO0O0O0O0 .status_code !=200 :#line:87
                    print (OO0O0O00OO0O0O0O0 .status_code )#line:88
                    return #line:89
                else :#line:90
                    if "参数异常"in OO0O0O00OO0O0O0O0 .text :#line:91
                        return #line:92
                OO0OOO0OOOO00O00O =OO0O0O00OO0O0O0O0 .json ()['token']#line:93
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOO0000O0OO00OOO0}',OO0OOO0OOOO00O00O ,ex =1800 ):#line:95
                    print ("✅Token缓存成功")#line:96
                else :#line:97
                    print ("❌Token缓存失败")#line:98
                return OO0OOO0OOOO00O00O #line:99
        else :#line:100
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0O0O0O0O0OO000 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:111
            O0OO000OOO0OOO0OO =sign ({"url":f"{O0000O0OO0O0000O0}","id":""},'isvObfuscator')#line:112
            OO0O0O00OO0O0O0O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:114
            if OO0O0O00OO0O0O0O0 .status_code !=200 :#line:115
                print (OO0O0O00OO0O0O0O0 .status_code )#line:116
                return #line:117
            else :#line:118
                if "参数异常"in OO0O0O00OO0O0O0O0 .text :#line:119
                    return #line:120
            OO00O0O000000O0OO =OO0O0O00OO0O0O0O0 .json ()['token']#line:121
            print (f"✅获取实时Token")#line:122
            return OO00O0O000000O0OO #line:123
    except :#line:124
        return #line:125
def getJdTime ():#line:127
    O0O00OOOOO0OOOO00 =int (round (time .time ()*1000 ))#line:128
    return O0O00OOOOO0OOOO00 #line:129
def randomString (OOOO000000OO00O0O ,flag =False ):#line:131
    OO0O0O0O0O0O00OO0 ="0123456789abcdef"#line:132
    if flag :OO0O0O0O0O0O00OO0 =OO0O0O0O0O0O00OO0 .upper ()#line:133
    OO0OO00OO00OO0OO0 =[random .choice (OO0O0O0O0O0O00OO0 )for _OOO0OOO00OO000000 in range (OOOO000000OO00O0O )]#line:134
    return ''.join (OO0OO00OO00OO0OO0 )#line:135
def refresh_cookies (O0000OOO0O00O0O00 ):#line:137
    if O0000OOO0O00O0O00 .cookies :#line:138
        OOO0O00OO00O00O00 =O0000OOO0O00O0O00 .cookies .get_dict ()#line:139
        OOOOOOOOOO00O00OO =[(O000O00000OO000OO +"="+OOO0O00OO00O00O00 [O000O00000OO000OO ])for O000O00000OO000OO in OOO0O00OO00O00O00 ]#line:140
        global activityCookie #line:141
        OOOOOOO0OO0OO00OO =[OOO0O0OOO000O0OOO for OOO0O0OOO000O0OOO in activityCookie .split (';')if OOO0O0OOO000O0OOO !='']#line:142
        for O0O0000OOO00OO000 in OOOOOOO0OO0OO00OO :#line:143
            for O0O00OO0O0OO0O00O in OOOOOOOOOO00O00OO :#line:144
                if O0O0000OOO00OO000 .split ('=')[0 ]==O0O00OO0O0OO0O00O .split ('=')[0 ]:#line:145
                    if O0O0000OOO00OO000 .split ('=')[1 ]!=O0O00OO0O0OO0O00O .split ('=')[1 ]:#line:146
                        OOOOOOO0OO0OO00OO .remove (O0O0000OOO00OO000 )#line:147
        activityCookie =''.join (sorted ([(O00O00OO00OOO0O00 +";")for O00O00OO00OOO0O00 in list (set (OOOOOOO0OO0OO00OO +OOOOOOOOOO00O00OO ))]))#line:148
def getActivity ():#line:150
    OO0OOOOO0000OO0O0 =activityUrl #line:151
    O0000O0OO00OO0000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:159
    O00O0000OOO000000 =requests .request ("GET",OO0OOOOO0000OO0O0 ,headers =O0000O0OO00OO0000 )#line:160
    if O00O0000OOO000000 .status_code ==200 :#line:161
        if O00O0000OOO000000 .cookies :#line:162
            OO0O00O0O0000OO00 =O00O0000OOO000000 .cookies .get_dict ()#line:163
            OO00O0O0OO0OOO0O0 =[(OOOO0O0OO0O00OO0O +"="+OO0O00O0O0000OO00 [OOOO0O0OO0O00OO0O ])for OOOO0O0OO0O00OO0O in OO0O00O0O0000OO00 ]#line:164
            O00O00O00O00OO0OO =''.join (sorted ([(O0O00OOO0OO0O0O0O +";")for O0O00OOO0OO0O0O0O in OO00O0O0OO0OOO0O0 ]))#line:165
        OOO0OOO000OOOO000 =O00O0000OOO000000 .text #line:166
        if "活动已结束"in OOO0OOO000OOOO000 :#line:167
            print ("⛈活动已结束,下次早点来~")#line:168
            sys .exit ()#line:169
        if "活动未开始"in OOO0OOO000OOOO000 :#line:170
            print ("⛈活动未开始~")#line:171
            sys .exit ()#line:172
        if "关注"in OOO0OOO000OOOO000 and "加购"not in OOO0OOO000OOOO000 :#line:173
            OOOOOOO0O00O00O0O =5 #line:174
        else :#line:175
            OOOOOOO0O00O00O0O =6 #line:176
        return O00O00O00O00OO0OO ,OOOOOOO0O00O00O0O #line:177
    else :#line:178
        print (O00O0000OOO000000 .status_code ,"⚠️疑似ip黑了")#line:179
        OO00OO00O00O0O0OO +=f'{O00O0000OOO000000.status_code} ⚠️疑似ip黑了\n'#line:180
        sys .exit ()#line:181
def getSystemConfigForNew (OO000O0000O0OOO00 ):#line:183
    OOO0OOO00O0000OO0 ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:184
    OO00O0OO0OO0OOO00 =f'activityId={activityId}&activityType={OO000O0000O0OOO00}'#line:185
    O0OOO000OO0OO000O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:198
    OO0000O0000000O00 =requests .request ("POST",OOO0OOO00O0000OO0 ,headers =O0OOO000OO0OO000O ,data =OO00O0OO0OO0OOO00 )#line:199
    refresh_cookies (OO0000O0000000O00 )#line:200
def getSimpleActInfoVo ():#line:202
    O000O000OOO0OOOO0 ="https://lzkj-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:203
    O0O00O00O0O0000O0 =f"activityId={activityId}"#line:204
    OOO0OO0O0O0OOOOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:217
    OO00O00OOO0OO0O0O =requests .request ("POST",O000O000OOO0OOOO0 ,headers =OOO0OO0O0O0OOOOO0 ,data =O0O00O00O0O0000O0 )#line:218
    refresh_cookies (OO00O00OOO0OO0O0O )#line:219
    OO00O0000O00O0000 =OO00O00OOO0OO0O0O .json ()#line:220
    if OO00O0000O00O0000 ['result']:#line:221
        return OO00O0000O00O0000 ['data']#line:222
def getMyPing (O000O0OOO0OO0000O ):#line:224
    OO00O000OOO0O0O0O ="https://lzkj-isv.isvjcloud.com/customer/getMyPing"#line:225
    OO0OO0O0OO0O000OO =f"userId={O000O0OOO0OO0000O}&token={token}&fromType=APP"#line:226
    O00OO0OOO0OO0O00O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:239
    OO0OOO0OOOOOOOO00 =requests .request ("POST",OO00O000OOO0O0O0O ,headers =O00OO0OOO0OO0O00O ,data =OO0OO0O0OO0O000OO )#line:240
    if OO0OOO0OOOOOOOO00 .status_code ==200 :#line:241
        refresh_cookies (OO0OOO0OOOOOOOO00 )#line:242
        O0OO00O0O000OOOOO =OO0OOO0OOOOOOOO00 .json ()#line:243
        if O0OO00O0O000OOOOO ['result']:#line:244
            return O0OO00O0O000OOOOO ['data']['nickname'],O0OO00O0O000OOOOO ['data']['secretPin']#line:245
        else :#line:246
            print (f"⚠️{O0OO00O0O000OOOOO['errorMessage']}")#line:247
    else :#line:248
        print (OO0OOO0OOOOOOOO00 .status_code ,"⚠️疑似ip黑了")#line:249
        O0OO0O0O00O00OO00 +=f'{OO0OOO0OOOOOOOO00.status_code} ⚠️疑似ip黑了\n'#line:250
        sys .exit ()#line:251
def accessLogWithAD (OOO00O00OOOO0OOOO ,O0OO0000000O0O00O ,OO000O000O0000OOO ):#line:253
    O00O00OOO000O0OO0 ="https://lzkj-isv.isvjcloud.com/common/accessLogWithAD"#line:254
    OOOO0OOO00O0OO000 =f"venderId={OOO00O00OOOO0OOOO}&code={OO000O000O0000OOO}&pin={quote_plus(O0OO0000000O0O00O)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource="#line:255
    OOO0O000000O0OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:268
    OO0OO0000000OOO00 =requests .request ("POST",O00O00OOO000O0OO0 ,headers =OOO0O000000O0OO0O ,data =OOOO0OOO00O0OO000 )#line:269
    refresh_cookies (OO0OO0000000OOO00 )#line:270
def activityContent (OOOO0O0O0OO000O0O ):#line:272
    OO0OO0OOO000OOO0O ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/activityContent"#line:273
    O0O00000O0OO0OO00 =f"activityId={activityId}&pin={quote_plus(OOOO0O0O0OO000O0O)}"#line:274
    OO00O0O00OOO000O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:287
    OO0OOOO000OOOO0O0 =requests .request ("POST",OO0OO0OOO000OOO0O ,headers =OO00O0O00OOO000O0 ,data =O0O00000O0OO0OO00 )#line:288
    OOOO0O0O00O0O000O =OO0OOOO000OOOO0O0 .json ()#line:290
    if OOOO0O0O00O0O000O ['result']:#line:291
        OO0O0OO00OOO0OOO0 =OOOO0O0O00O0O000O ['data']['needCollectionSize']#line:292
        OO000O000OOO00OOO =OOOO0O0O00O0O000O ['data']['hasCollectionSize']#line:293
        O0O0000000O0O0000 =OOOO0O0O00O0O000O ['data']['needFollow']#line:294
        O000OOOO000OOOO00 =OOOO0O0O00O0O000O ['data']['hasFollow']#line:295
        O000000O00OOOOOO0 =OOOO0O0O00O0O000O ['data']['cpvos']#line:296
        O000000OOO00OO0O0 =OOOO0O0O00O0O000O ['data']['drawInfo']#line:297
        OOO00000OOOOO0OO0 =O000000OOO00OO0O0 ['drawOk']#line:298
        OOOOOO0O00O00O00O =O000000OOO00OO0O0 ['name']#line:299
        O0O00000O0OOOO0O0 =OOOO0O0O00O0O000O ['data']['oneKeyAddCart']#line:300
        return OO0O0OO00OOO0OOO0 ,OO000O000OOO00OOO ,O0O0000000O0O0000 ,O000OOOO000OOOO00 ,O000000O00OOOOOO0 ,OOO00000OOOOO0OO0 ,OOOOOO0O00O00O00O ,O0O00000O0OOOO0O0 #line:301
    else :#line:302
        print (f"⛈{OOOO0O0O00O0O000O['errorMessage']}")#line:303
        sys .exit ()#line:304
def shopInfo ():#line:306
    OO00O0O000O0OO0OO ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/shopInfo"#line:307
    OO0OO0O0OOOOOOOOO =f"activityId={activityId}"#line:308
    O00O0OO00O00000OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:321
    O00O0OOOO0000OO0O =requests .request ("POST",OO00O0O000O0OO0OO ,headers =O00O0OO00O00000OO ,data =OO0OO0O0OOOOOOOOO )#line:322
    refresh_cookies (O00O0OOOO0000OO0O )#line:323
    OOOOO00OOOOOOOOO0 =O00O0OOOO0000OO0O .json ()#line:324
    if OOOOO00OOOOOOOOO0 ['result']:#line:325
        O0O0O00O00OOO0OOO =OOOOO00OOOOOOOOO0 ['data']['shopName']#line:326
        return O0O0O00O00OOO0OOO #line:327
    else :#line:328
        print (f"⛈{OOOOO00OOOOOOOOO0['errorMessage']}")#line:329
def getActMemberInfo (O00O00O0O0O0000OO ,OOO000O00000OOOO0 ):#line:331
    OOO00O00O0O00OO0O ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getActMemberInfo"#line:332
    OO00OO0O0OOO0O00O =f"venderId={O00O00O0O0O0000OO}&activityId={activityId}&pin={quote_plus(OOO000O00000OOOO0)}"#line:333
    OOOOOO000OOOO00OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:346
    OO00O00OOO00O000O =requests .request ("POST",OOO00O00O0O00OO0O ,headers =OOOOOO000OOOO00OO ,data =OO00OO0O0OOO0O00O )#line:347
    O0000O0OO0O0OO0O0 =OO00O00OOO00O000O .json ()#line:349
    print (O0000O0OO0O0OO0O0 )#line:350
    if O0000O0OO0O0OO0O0 ['result']:#line:351
        O00000000OOO0OO0O =O0000O0OO0O0OO0O0 ['data']['openCard']#line:352
        return O00000000OOO0OO0O #line:353
    else :#line:354
        print (f"⛈{O0000O0OO0O0OO0O0['errorMessage']}")#line:355
def followShop (O0000OO0O0000OOO0 ,OO0O0O00OO0OOO000 ,OO000O0000O00OO00 ):#line:357
    OO0OO00O00OOO0O00 ="https://lzkj-isv.isvjcloud.com/wxActionCommon/followShop"#line:358
    O000O0O0OOO00O0O0 =f"userId={O0000OO0O0000OOO0}&activityId={activityId}&buyerNick={quote_plus(OO0O0O00OO0OOO000)}&activityType={OO000O0000O00OO00}"#line:359
    O0OO0OO0O00000OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:372
    O0OO0000OOO000O00 =requests .request ("POST",OO0OO00O00OOO0O00 ,headers =O0OO0OO0O00000OO0 ,data =O000O0O0OOO00O0O0 )#line:373
    refresh_cookies (O0OO0000OOO000O00 )#line:374
    O0OO0O00OOOO0OO0O =O0OO0000OOO000O00 .json ()#line:375
    if O0OO0O00OOOO0OO0O ['result']:#line:376
        OO00OO0000000OOOO =O0OO0O00OOOO0OO0O ['data']#line:377
        return OO00OO0000000OOOO #line:378
    else :#line:379
        print (f"⛈{O0OO0O00OOOO0OO0O['errorMessage']}")#line:380
        if "店铺会员"in O0OO0O00OOOO0OO0O ['errorMessage']:#line:381
            return 99 #line:382
def getInfo ():#line:384
    OOO0O0O0OOO0O0OO0 =f"https://lzkj-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"#line:385
    OOO00OO0O000OO0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:396
    OOO00OOOOO0OOO00O =requests .request ("GET",OOO0O0O0OOO0O0OO0 ,headers =OOO00OO0O000OO0OO )#line:397
    refresh_cookies (OOO00OOOOO0OOO00O )#line:398
def addCard (OOO00O0OOO00O0O00 ,O00O0OO00O0O00OOO ):#line:400
    ""#line:401
    OO0O0O0OOOO0OOO00 ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/addCart"#line:402
    O0O0OOOO00O0OOO0O =f"productId={OOO00O0OOO00O0O00}&activityId={activityId}&pin={quote_plus(O00O0OO00O0O00OOO)}"#line:403
    O0OOO00O0OO0O0000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:416
    O000000O00O00OO00 =requests .request ("POST",OO0O0O0OOOO0OOO00 ,headers =O0OOO00O0OO0O0000 ,data =O0O0OOOO00O0OOO0O )#line:417
    refresh_cookies (O000000O00O00OO00 )#line:418
    O00OOO0OO0OOO0OO0 =O000000O00O00OO00 .json ()#line:419
    if O00OOO0OO0OOO0OO0 ['result']:#line:420
        O0OOOO0O00OO00000 =O00OOO0OO0OOO0OO0 ['data']['hasAddCartSize']#line:421
        return O0OOOO0O00OO00000 #line:422
    else :#line:423
        print (f"⛈{O00OOO0OO0OOO0OO0['errorMessage']}")#line:424
def collection (OO0O0O0O0OOO0000O ,O0OOOO000OOO00OO0 ):#line:426
    ""#line:427
    O0OO00OO00O00O0OO ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/collection"#line:428
    OO00OOOO000OOO00O =f"productId={OO0O0O0O0OOO0000O}&activityId={activityId}&pin={quote_plus(O0OOOO000OOO00OO0)}"#line:429
    O00OOO0000O000O00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:442
    O0O000O000OO00000 =requests .request ("POST",O0OO00OO00O00O0OO ,headers =O00OOO0000O000O00 ,data =OO00OOOO000OOO00O )#line:443
    refresh_cookies (O0O000O000OO00000 )#line:444
    OO0O0000OO00OO0OO =O0O000O000OO00000 .json ()#line:445
    if OO0O0000OO00OO0OO ['result']:#line:446
        O00OOOO00O00OO0O0 =OO0O0000OO00OO0OO ['data']['hasCollectionSize']#line:447
        return O00OOOO00O00OO0O0 #line:448
    else :#line:449
        print (f"⛈{OO0O0000OO00OO0OO['errorMessage']}")#line:450
def oneKeyAdd (OO00OO00O00OO0O00 ,OOO00O0OOOO00O0O0 ):#line:452
    ""#line:453
    OO0O0OO0O000000O0 ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/oneKeyAddCart"#line:454
    O0OO0OOO00OOO0000 =f"productIds={OO00OO00O00OO0O00}&activityId={activityId}&pin={quote_plus(OOO00O0OOOO00O0O0)}"#line:455
    O000OOO0OO0O0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:468
    O0O0OOOO0OO0OOO0O =requests .request ("POST",OO0O0OO0O000000O0 ,headers =O000OOO0OO0O0O0OO ,data =O0OO0OOO00OOO0000 )#line:469
    refresh_cookies (O0O0OOOO0OO0OOO0O )#line:470
    O000OOO00O00O0OOO =O0O0OOOO0OO0OOO0O .json ()#line:471
    if O000OOO00O00O0OOO ['result']:#line:472
        O0000000000OOOOOO =O000OOO00O00O0OOO ['data']['hasAddCartSize']#line:473
        return O0000000000OOOOOO #line:474
    else :#line:475
        print (f"⛈{O000OOO00O00O0OOO['errorMessage']}")#line:476
def getPrize (OOOO0OOO00OOOO000 ):#line:478
    O0O00O00O0000OO0O ="https://lzkj-isv.isvjcloud.com/wxCollectionActivity/getPrize"#line:479
    O0O000O0OO0OO0000 =f"activityId={activityId}&pin={quote_plus(OOOO0OOO00OOOO000)}"#line:480
    O0OO00OOO00O0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:493
    OO00O0OOO000OO00O =requests .request ("POST",O0O00O00O0000OO0O ,headers =O0OO00OOO00O0O0OO ,data =O0O000O0OO0OO0000 )#line:494
    O00O00000OOO000OO =OO00O0OOO000OO00O .json ()#line:495
    if O00O00000OOO000OO ['result']:#line:496
        O0000OO0OOOOOOOO0 =O00O00000OOO000OO ['data']#line:497
        if O0000OO0OOOOOOOO0 ['drawOk']:#line:498
            OO0O00O0OOOOOOO0O =O0000OO0OOOOOOOO0 ['name']#line:499
            return OO0O00O0OOOOOOO0O #line:500
        else :#line:501
            O0000OOOOO00O0OOO =O0000OO0OOOOOOOO0 ['errorMessage']#line:502
            print (f"⛈{O0000OOOOO00O0OOO}")#line:503
            if "不足"in O0000OOOOO00O0OOO :#line:504
                sys .exit ()#line:505
            return O0000OOOOO00O0OOO #line:506
    else :#line:507
        print (f"⛈{O00O00000OOO000OO['errorMessage']}")#line:508
        if '奖品已发完'in O00O00000OOO000OO ['errorMessage']:#line:509
            sys .exit ()#line:510
        return O00O00000OOO000OO ['errorMessage']#line:511
if __name__ =='__main__':#line:514
    global msg #line:515
    msg =''#line:516
    r =redis_conn ()#line:517
    try :#line:518
        cks =getCk #line:519
        if not cks :#line:520
            sys .exit ()#line:521
    except :#line:522
        print ("未获取到有效COOKIE,退出程序！")#line:523
        sys .exit ()#line:524
    num =0 #line:525
    for cookie in cks [:runNums ]:#line:526
        num +=1 #line:527
        if num %5 ==0 :#line:528
            print ("⏰等待3s,休息一下")#line:529
            time .sleep (3 )#line:530
        global ua ,activityCookie ,token #line:531
        ua =userAgent ()#line:532
        try :#line:533
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:534
            pt_pin =unquote_plus (pt_pin )#line:535
        except IndexError :#line:536
            pt_pin =f'用户{num}'#line:537
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:538
        print (datetime .now ())#line:539
        token =getToken (cookie ,r )#line:540
        if token is None :#line:541
            print (f"⚠️获取Token失败！⏰等待2s")#line:542
            time .sleep (2 )#line:543
            continue #line:544
        time .sleep (0.3 )#line:545
        getAct =getActivity ()#line:546
        activityCookie =getAct [0 ]#line:547
        activityType =getAct [1 ]#line:548
        time .sleep (0.35 )#line:549
        getSystemConfigForNew (activityType )#line:550
        time .sleep (0.35 )#line:551
        getSimAct =getSimpleActInfoVo ()#line:552
        venderId =getSimAct ['venderId']#line:553
        time .sleep (0.35 )#line:554
        getPin =getMyPing (venderId )#line:555
        if getPin is not None :#line:556
            nickname =getPin [0 ]#line:557
            secretPin =getPin [1 ]#line:558
            time .sleep (0.35 )#line:559
            accessLogWithAD (venderId ,secretPin ,activityType )#line:560
            time .sleep (0.35 )#line:561
            actCont =activityContent (secretPin )#line:562
            if not actCont :#line:563
                continue #line:564
            needCollectionSize =actCont [0 ]#line:565
            hasCollectionSize =actCont [1 ]#line:566
            needFollow =actCont [2 ]#line:567
            hasFollow =actCont [3 ]#line:568
            cpvos =actCont [4 ]#line:569
            drawOk =actCont [5 ]#line:570
            priceName =actCont [6 ]#line:571
            oneKeyAddCart =actCont [7 ]#line:572
            time .sleep (0.35 )#line:573
            shopName =shopInfo ()#line:574
            if num ==1 :#line:575
                print (f"✅开启{shopName}-加购活动,需关注加购{needCollectionSize}个商品")#line:576
                print (f"🎁奖品{priceName}\n")#line:577
                msg +=f'✅开启{shopName}-加购活动\n📝活动地址{activityUrl}\n🎁奖品{priceName}\n\n'#line:578
            if needCollectionSize <=hasCollectionSize :#line:579
                print ("☃️已完成过加购任务,无法重复进行！")#line:580
                continue #line:581
            else :#line:582
                skuIds =[O000O0O0OO0O00OOO ['skuId']for O000O0O0OO0O00OOO in cpvos if not O000O0O0OO0O00OOO ['collection']]#line:583
            time .sleep (0.2 )#line:584
            getInfo ()#line:585
            if needFollow :#line:586
                if not hasFollow :#line:587
                    FS =followShop (venderId ,secretPin ,activityType )#line:588
                    if FS ==99 :#line:589
                        continue #line:590
            time .sleep (0.35 )#line:591
            addSkuNums =needCollectionSize -hasCollectionSize #line:592
            if oneKeyAddCart ==1 :#line:593
                hasAddCartSize =oneKeyAdd (skuIds ,secretPin )#line:594
                if hasAddCartSize :#line:595
                    if hasAddCartSize ==addSkuNums :#line:596
                        print (f"🛳成功一键加购{hasAddCartSize}个商品")#line:597
                else :#line:598
                    continue #line:599
            else :#line:600
                for productId in skuIds :#line:601
                    if activityType ==6 :#line:602
                        hasAddCartSize =addCard (productId ,secretPin )#line:603
                    elif activityType ==5 :#line:604
                        hasAddCartSize =collection (productId ,secretPin )#line:605
                    time .sleep (0.25 )#line:606
                    if hasAddCartSize :#line:607
                        if hasAddCartSize ==addSkuNums :#line:608
                            print (f"🛳成功加购{hasAddCartSize}个商品")#line:609
                            break #line:610
            time .sleep (0.35 )#line:611
            for i in range (3 ):#line:612
                priceName =getPrize (secretPin )#line:613
                if "擦肩"in priceName :#line:614
                    time .sleep (0.2 )#line:615
                    continue #line:616
                else :#line:617
                    break #line:618
            if "京豆"in priceName :#line:619
                print (f"🎉获得{priceName}")#line:620
                msg +=f'【账号{num}】{pt_pin} 🎉{priceName}\n'#line:621
            elif "擦肩"in priceName :#line:622
                print (f"😭获得💨💨💨")#line:623
            else :#line:624
                pass #line:625
        time .sleep (1.5 )#line:627
    title ="🗣消息提醒：加购有礼-JK"#line:629
    msg =f"⏰{str(datetime.now())[:19]}\n"+msg #line:630
    send (title ,msg )
