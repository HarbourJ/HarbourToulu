#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxCompleteInfo.py(完善信息有礼-监控脚本)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('完善信息有礼-JK');
ActivityEntry: https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view/activity?activityId=f3325e3375a14866xxxxxxxxxxxx&venderId=1000086
               变量 export jd_wxCompleteInfoId="f3325e3375a14866xxxxxxxxxxxx&1000086192"(活动id&venderId)
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
jd_wxCompleteInfoId =os .environ .get ("jd_wxCompleteInfoId")if os .environ .get ("jd_wxCompleteInfoId")else ""#line:24
if not jd_wxCompleteInfoId or "&"not in jd_wxCompleteInfoId :#line:26
    print ("⚠️未发现有效活动变量jd_wxCompleteInfoId,退出程序!")#line:27
    sys .exit ()#line:28
activityId =jd_wxCompleteInfoId .split ('&')[0 ]#line:29
venderId =jd_wxCompleteInfoId .split ('&')[1 ]#line:30
activityUrl =f"https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/view/activity?activityId={activityId}&venderId={venderId}"#line:32
print (f"【🛳活动入口】{activityUrl}")#line:33
def redis_conn ():#line:35
    try :#line:36
        try :#line:37
            import redis #line:38
        except Exception as O0O0O0OO0OO0O0OOO :#line:39
            print (O0O0O0OO0OO0O0OOO )#line:40
            if "No module"in str (O0O0O0OO0OO0O0OOO ):#line:41
                os .system ("pip install redis")#line:42
            import redis #line:43
        try :#line:44
            O000O000OOO00O0OO =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:45
            OO00OO00000000O00 =redis .Redis (connection_pool =O000O000OOO00O0OO )#line:46
            OO00OO00000000O00 .get ('conn_test')#line:47
            print ('✅redis连接成功')#line:48
            return OO00OO00000000O00 #line:49
        except :#line:50
            print ("⚠️redis连接异常")#line:51
    except :#line:52
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:53
        sys .exit ()#line:54
def getToken (OO0OO0OO0OOO0OOOO ,r =None ):#line:56
    OO00OO0O0OO0OOO0O =f'{activityUrl.split("com/")[0]}com'#line:57
    try :#line:58
        OOOO00O00O000000O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OO0OO0OO0OOO0OOOO )[0 ])#line:60
    except :#line:61
        OOOO00O00O000000O =OO0OO0OO0OOO0OOOO [:15 ]#line:63
    try :#line:64
        if r is not None :#line:65
            O0O0O000OOO0OOO0O =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO00O00O000000O}')#line:66
            if O0O0O000OOO0OOO0O is not None :#line:68
                print (f"♻️获取缓存Token")#line:69
                return O0O0O000OOO0OOO0O #line:70
            else :#line:71
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0OO0OO0OOO0OOOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:83
                O0O0O0OOOOOOOO00O =sign ({"url":f"{OO00OO0O0OO0OOO0O}","id":""},'isvObfuscator')#line:84
                OO0O0O0OO00000000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:86
                if OO0O0O0OO00000000 .status_code !=200 :#line:87
                    print (OO0O0O0OO00000000 .status_code )#line:88
                    return #line:89
                else :#line:90
                    if "参数异常"in OO0O0O0OO00000000 .text :#line:91
                        return #line:92
                O0O0O00OO0OO00000 =OO0O0O0OO00000000 .json ()['token']#line:93
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OOOO00O00O000000O}',O0O0O00OO0OO00000 ,ex =1800 ):#line:95
                    print ("✅Token缓存成功")#line:96
                else :#line:97
                    print ("❌Token缓存失败")#line:98
                return O0O0O00OO0OO00000 #line:99
        else :#line:100
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0OO0OO0OOO0OOOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:111
            O0O0O0OOOOOOOO00O =sign ({"url":f"{OO00OO0O0OO0OOO0O}","id":""},'isvObfuscator')#line:112
            OO0O0O0OO00000000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:114
            if OO0O0O0OO00000000 .status_code !=200 :#line:115
                print (OO0O0O0OO00000000 .status_code )#line:116
                return #line:117
            else :#line:118
                if "参数异常"in OO0O0O0OO00000000 .text :#line:119
                    return #line:120
            O0O0O000OOO0OOO0O =OO0O0O0OO00000000 .json ()['token']#line:121
            print (f"✅获取实时Token")#line:122
            return O0O0O000OOO0OOO0O #line:123
    except :#line:124
        return #line:125
def getJdTime ():#line:127
    OO0O0000O0OO000OO =int (round (time .time ()*1000 ))#line:128
    return OO0O0000O0OO000OO #line:129
def randomString (O0O0OOOOO000OOOO0 ,flag =False ):#line:131
    O0OOO0OOOOOOO0OO0 ="0123456789abcdef"#line:132
    if flag :O0OOO0OOOOOOO0OO0 =O0OOO0OOOOOOO0OO0 .upper ()#line:133
    O0OO00O0000OOO00O =[random .choice (O0OOO0OOOOOOO0OO0 )for _OO00O00OO0000O000 in range (O0O0OOOOO000OOOO0 )]#line:134
    return ''.join (O0OO00O0000OOO00O )#line:135
def refresh_cookies (OOOOOOO0O0O0O00OO ):#line:137
    if OOOOOOO0O0O0O00OO .cookies :#line:138
        O0000OO000OOO0OO0 =OOOOOOO0O0O0O00OO .cookies .get_dict ()#line:139
        O00000OO000O0O00O =[(O0OOO0OO0O00O0O0O +"="+O0000OO000OOO0OO0 [O0OOO0OO0O00O0O0O ])for O0OOO0OO0O00O0O0O in O0000OO000OOO0OO0 ]#line:140
        global activityCookie #line:141
        O0O00OO000O000O0O =[OOOOO0OOOOOOO0O00 for OOOOO0OOOOOOO0O00 in activityCookie .split (';')if OOOOO0OOOOOOO0O00 !='']#line:142
        for O0OOO000O00OO0O0O in O0O00OO000O000O0O :#line:143
            for OOOO000OOOOO00O0O in O00000OO000O0O00O :#line:144
                if O0OOO000O00OO0O0O .split ('=')[0 ]==OOOO000OOOOO00O0O .split ('=')[0 ]:#line:145
                    if O0OOO000O00OO0O0O .split ('=')[1 ]!=OOOO000OOOOO00O0O .split ('=')[1 ]:#line:146
                        O0O00OO000O000O0O .remove (O0OOO000O00OO0O0O )#line:147
        activityCookie =''.join (sorted ([(O00OO00O00O000O0O +";")for O00OO00O00O000O0O in list (set (O0O00OO000O000O0O +O00000OO000O0O00O ))]))#line:148
def getActivity ():#line:150
    O0OOOOOOOOOO0O0OO =activityUrl #line:151
    O0OO0O00O0O0OO0OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:159
    OO0OOOOO0000O00O0 =requests .request ("GET",O0OOOOOOOOOO0O0OO ,headers =O0OO0O00O0O0OO0OO )#line:160
    if OO0OOOOO0000O00O0 .status_code ==200 :#line:161
        if OO0OOOOO0000O00O0 .cookies :#line:162
            OOOO00O00OOOO00O0 =OO0OOOOO0000O00O0 .cookies .get_dict ()#line:163
            OOO0O0O000OOOOO00 =[(O00OO0OO00OO0000O +"="+OOOO00O00OOOO00O0 [O00OO0OO00OO0000O ])for O00OO0OO00OO0000O in OOOO00O00OOOO00O0 ]#line:164
            OO00OO0O00OO0OOOO =''.join (sorted ([(O0000OOO00O0O0OOO +";")for O0000OOO00O0O0OOO in OOO0O0O000OOOOO00 ]))#line:165
        return OO00OO0O00OO0OOOO #line:166
    else :#line:167
        print (OO0OOOOO0000O00O0 .status_code )#line:168
        print ("⚠️疑似ip黑了")#line:169
        sys .exit ()#line:170
def getOpenStatus ():#line:172
    OOO000OO00000O0OO ="https://cjhy-isv.isvjcloud.com/assembleConfig/getOpenStatus"#line:173
    O00O0OO0O00OO0000 =f'activityId={activityId}'#line:174
    OOOOOO0OOO0OO000O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:187
    OOOO00O0O0OOO0000 =requests .request ("POST",OOO000OO00000O0OO ,headers =OOOOOO0OOO0OO000O ,data =O00O0OO0O00OO0000 )#line:188
def getSystemConfig ():#line:190
    O00OOOOO000O0OOOO ="https://cjhy-isv.isvjcloud.com/wxCommonInfo/getSystemConfig"#line:191
    O00O000000O0O0O00 =f'activityId={activityId}&activityType='#line:192
    O0O00OO00OOOOO00O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:205
    O000OO0O000O0OO00 =requests .request ("POST",O00OOOOO000O0OOOO ,headers =O0O00OO00OOOOO00O ,data =O00O000000O0O0O00 )#line:206
    refresh_cookies (O000OO0O000O0OO00 )#line:207
def getSimpleActInfoVo ():#line:209
    O0O0OOOOO0OOO0OOO ="https://cjhy-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:210
    O00O0000O0O00OOO0 =f"activityId={activityId}"#line:211
    OO0OO00OO00OO0OO0 ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:224
    O0OOO0OOO0OOO0OO0 =requests .request ("POST",O0O0OOOOO0OOO0OOO ,headers =OO0OO00OO00OO0OO0 ,data =O00O0000O0O00OOO0 )#line:225
    refresh_cookies (O0OOO0OOO0OOO0OO0 )#line:226
    OO0O00OOOO0OO0OO0 =O0OOO0OOO0OOO0OO0 .json ()#line:227
    if OO0O00OOOO0OO0OO0 ['result']:#line:228
        return OO0O00OOOO0OO0OO0 ['data']#line:229
    else :#line:230
        print (OO0O00OOOO0OO0OO0 ['errorMessage'])#line:231
def getMyPing (O0OO00O000OOO00OO ):#line:233
    OO0OOO000O000O0O0 ="https://cjhy-isv.isvjcloud.com/customer/getMyPing"#line:234
    O000O0O0OO00000OO =f"userId={O0OO00O000OOO00OO}&token={token}&fromType=APP&riskType=1"#line:235
    O0OO00OOO0OOOOOO0 ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:248
    O00OO0O0O00OOO000 =requests .request ("POST",OO0OOO000O000O0O0 ,headers =O0OO00OOO0OOOOOO0 ,data =O000O0O0OO00000OO )#line:249
    if O00OO0O0O00OOO000 .status_code ==200 :#line:250
        refresh_cookies (O00OO0O0O00OOO000 )#line:251
        OOO0OOO00O000OOOO =O00OO0O0O00OOO000 .json ()#line:252
        if OOO0OOO00O000OOOO ['result']:#line:253
            return OOO0OOO00O000OOOO ['data']['nickname'],OOO0OOO00O000OOOO ['data']['secretPin']#line:254
        else :#line:255
            print (f"⚠️{OOO0OOO00O000OOOO['errorMessage']}")#line:256
    else :#line:257
        print (O00OO0O0O00OOO000 .status_code )#line:258
        print ("⚠️疑似ip黑了")#line:259
        sys .exit ()#line:260
def _O0000O00000OO0O0O (OOO0OOOO0000O000O ):#line:262
    OOOO00000O00OOOOO ="https://cjhy-isv.isvjcloud.com/completeInfoActivity/selectById"#line:263
    OOOOOO000OO0000O0 =f"activityId={activityId}&venderId={OOO0OOOO0000O000O}"#line:264
    O0O00O0O0OOOO00OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:277
    OOO00O0O0OOOOOO0O =requests .request ("POST",OOOO00000O00OOOOO ,headers =O0O00O0O0OOOO00OO ,data =OOOOOO000OO0000O0 )#line:278
    O0OO000O0OOOOOOOO =OOO00O0O0OOOOOO0O .json ()#line:279
    if O0OO000O0OOOOOOOO ['result']:#line:280
        O0OO0OOO00OO0OOOO =""#line:281
        O0O0OOOOOOO0O0O00 =O0OO000O0OOOOOOOO ['data']#line:282
        O00O0000000000000 =O0O0OOOOOOO0O0O00 ['chooseName']#line:283
        O0O0O00O0O0O000O0 =O0O0OOOOOOO0O0O00 ['choosePhone']#line:284
        O0OO0O00O0000O00O =O0O0OOOOOOO0O0O00 ['chooseBirth']#line:285
        O0000O00O0OO000O0 =O0O0OOOOOOO0O0O00 ['chooseWeixin']#line:286
        O000OOO0O0OOO0O00 =O0O0OOOOOOO0O0O00 ['chooseAddress']#line:287
        O0O0OO0OO00O0O0O0 =O0O0OOOOOOO0O0O00 ['chooseQQ']#line:288
        O000O0OOO0O0OOO00 =O0O0OOOOOOO0O0O00 ['chooseEmail']#line:289
        O000OO0000O00O00O =O0O0OOOOOOO0O0O00 ['chooseGender']#line:290
        O00O0000O000O000O =O0O0OOOOOOO0O0O00 ['chooseProfessional']#line:291
        OOOO0OO0000O00O0O =O0O0OOOOOOO0O0O00 ['customJson']#line:292
        OOOOO0000000OOO0O =get_mobile ()#line:293
        if O00O0000000000000 =='y':#line:294
            O00O00OOOO00O00O0 =quote_plus (f"{random.choice(['A','B','C','D','E','F','G','H'])}贤笙")#line:295
            O0OO0OOO00OO0OOOO +=f"name={O00O00OOOO00O00O0}&"#line:296
        if O0O0O00O0O0O000O0 =='y':#line:297
            O0OO0OOO00OO0OOOO +=f"phone={OOOOO0000000OOO0O}&"#line:298
        if O0OO0O00O0000O00O =='y':#line:299
            O00000O000O00000O ="2000-01-01"#line:300
            O0OO0OOO00OO0OOOO +=f"birthDay={O00000O000O00000O}&"#line:301
        if O0000O00O0OO000O0 =='y':#line:302
            OOO0OO00OO0OO0000 =OOOOO0000000OOO0O #line:303
            O0OO0OOO00OO0OOOO +=f"weiXin={OOO0OO00OO0OO0000}&"#line:304
        if O000O0OOO0O0OOO00 =='y':#line:305
            O0OO00O0OOO000OO0 =quote_plus (f"{OOOOO0000000OOO0O}@163.com")#line:306
            O0OO0OOO00OO0OOOO +=f"email={O0OO00O0OOO000OO0}&"#line:307
        if O000OO0000O00O00O =='y':#line:308
            O0OO00O00OO0O00O0 =quote_plus ("男")#line:309
            O0OO0OOO00OO0OOOO +=f"gender={O0OO00O00OO0O00O0}&"#line:310
        if O00O0000O000O000O =='y':#line:311
            OOO0O00OO0O0OO00O ="Engineer"#line:312
            O0OO0OOO00OO0OOOO +=f"professional={OOO0O00OO0O0OO00O}&"#line:313
        if O0O0OO0OO00O0O0O0 =='y':#line:314
            OOO0O0O0000OOO000 =OOOOO0000000OOO0O #line:315
            O0OO0OOO00OO0OOOO +=f"{OOO0O0O0000OOO000}&"#line:316
        if O000OOO0O0OOO0O00 =='y':#line:317
            O00OO0000OOO0O0O0 =quote_plus ("北京市")#line:318
            O0O0O00O0OO00OOOO =quote_plus ("东城区")#line:319
            OOOOOOOO0OO00OOOO =quote_plus ("北京大学城北门")#line:320
            O0OO0OOO00OO0OOOO +=f"province={O00OO0000OOO0O0O0}&city={O0O0O00O0OO00OOOO}&address={OOOOOOOO0OO00OOOO}&"#line:321
        if OOOO0OO0000O00O0O !="[]":#line:322
            OOOO00000O000OO0O ="%5B%2222%22%5D"#line:323
            O0OO0OOO00OO0OOOO +=f"customContent={OOOO00000O000OO0O}&"#line:324
        return O0OO0OOO00OO0OOOO #line:325
    else :#line:326
        print (O0OO000O0OOOOOOOO ['errorMessage'])#line:327
def getOpenCardInfo (OOOO0O00O00OO000O ,OOO00OOOOOOOOO0O0 ,OOO0000OO0O0OOO0O ):#line:329
    OO0OO0O0O000OOOOO ="https://cjhy-isv.isvjcloud.com/mc/new/brandCard/common/shopAndBrand/getOpenCardInfo"#line:330
    O000O0O00O0OO000O =f"venderId={OOOO0O00O00OO000O}&buyerPin={OOO00OOOOOOOOO0O0}&activityType={OOO0000OO0O0OOO0O}"#line:331
    O00O0O00O0OOOO00O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:344
    O0OOO00O0OOOO0OOO =requests .request ("POST",OO0OO0O0O000OOOOO ,headers =O00O0O00O0OOOO00O ,data =O000O0O00O0OO000O )#line:345
    OO00O00000OOOO00O =O0OOO00O0OOOO0OOO .json ()#line:346
    if OO00O00000OOOO00O ['result']:#line:347
        return OO00O00000OOOO00O ['data']#line:348
    else :#line:349
        print (OO00O00000OOOO00O ['errorMessage'])#line:350
def getShopInfoVO (OOO0O000O0OOO0O0O ):#line:352
    OO0O00O0000O000OO ="https://cjhy-isv.isvjcloud.com/wxActionCommon/getShopInfoVO"#line:353
    O00O0OO000O0O000O =f"userId={OOO0O000O0OOO0O0O}"#line:354
    OO0OOO000OO0OOOOO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:367
    O0O0OOO00O0OO0O0O =requests .request ("POST",OO0O00O0000O000OO ,headers =OO0OOO000OO0OOOOO ,data =O00O0OO000O0O000O )#line:368
    O0OOOO00OOOO00O00 =O0O0OOO00O0OO0O0O .json ()#line:369
    if O0OOOO00OOOO00O00 ['result']:#line:370
        return O0OOOO00OOOO00O00 ['data']#line:371
    else :#line:372
        print (O0OOOO00OOOO00O00 ['errorMessage'])#line:373
def accessLog (OOO0OOO00000O0OOO ,OO0O0OOOOO0O0O000 ,O0O000000O0OOOO0O ):#line:375
    OO00O000O0OOO00O0 ="https://cjhy-isv.isvjcloud.com/common/accessLog"#line:376
    O0OOO0O0000O00000 =f"venderId={OOO0OOO00000O0OOO}&code={O0O000000O0OOOO0O}&pin={quote_plus(OO0O0OOOOO0O0O000)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType="#line:377
    O00OO0O00OO0000OO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:390
    requests .request ("POST",OO00O000O0OOO00O0 ,headers =O00OO0O00OO0000OO ,data =O0OOO0O0000O00000 )#line:391
def listDrawContent (OOOO00OO0O00OOO0O ):#line:393
    O0OOOO00OO00O0OOO ="https://cjhy-isv.isvjcloud.com/drawContent/listDrawContent"#line:394
    O0OO0OOOOOOO0O00O =f"activityId={activityId}&type={OOOO00OO0O00OOO0O}"#line:395
    OOOOOOO0O0O0O00O0 ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:408
    OOO00OOO0O00OO0OO =requests .request ("POST",O0OOOO00OO00O0OOO ,headers =OOOOOOO0O0O0O00O0 ,data =O0OO0OOOOOOO0O00O )#line:409
    O00O0O00OO00OOOO0 =OOO00OOO0O00OO0OO .json ()#line:410
    if O00O0O00OO00OOOO0 ['result']:#line:411
        return O00O0O00OO00OOOO0 ['data']#line:412
    else :#line:413
        if "暂未填写"in O00O0O00OO00OOOO0 ['errorMessage']:#line:415
            print ("📝现在去完善信息")#line:416
def selectById (O00000O0O000OOOO0 ,OO000O0OO00O0O00O ):#line:418
    O0OO00OO00OOOOO0O ="https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/selectById"#line:419
    OO0OO0OOOO000O000 =f"activityId={activityId}&pin={quote_plus(O00000O0O000OOOO0)}&venderId={OO000O0OO00O0O00O}"#line:420
    OO00O0O0OOO0O0O0O ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:433
    OO0O00O0O0O0O0O00 =requests .request ("POST",O0OO00OO00OOOOO0O ,headers =OO00O0O0OOO0O0O0O ,data =OO0OO0OOOO000O000 )#line:434
    refresh_cookies (OO0O00O0O0O0O0O00 )#line:435
    OOO0O0OO0OOOOOO0O =OO0O00O0O0O0O0O00 .json ()#line:436
    if OOO0O0OO0OOOOOO0O ['result']:#line:437
        return OOO0O0OO0OOOOOO0O ['data']#line:438
    else :#line:439
        if "暂未填写"in OOO0O0OO0OOOOOO0O ['errorMessage']:#line:441
            print ("📝现在去完善会员信息")#line:442
def getInfo ():#line:444
    OO00OOO0OO000000O =f"https://cjhy-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"#line:445
    OO0O00O0000O0000O ={'Host':'cjhy-isv.isvjcloud.com','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive','Accept':'application/json','User-Agent':ua ,'Referer':activityUrl ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','X-Requested-With':'XMLHttpRequest','Cookie':activityCookie ,}#line:456
    requests .request ("GET",OO00OOO0OO000000O ,headers =OO0O00O0000O0000O )#line:457
def get_mobile ():#line:459
    O0O00OOOO00OOOOOO =['130','131','132','133','134']#line:460
    O00OO0O00O0OOOO00 =str (int (time .time ()))[2 :]#line:461
    OOOOOO0OO0000O00O =random .choice (O0O00OOOO00OOOOOO )+O00OO0O00O0OOOO00 #line:462
    return OOOOOO0OO0000O00O #line:463
def save (O0OOO000OOO00O00O ,O0O00O00O0O0OOOO0 ,O000O000OOOO0OO0O ,O00OO0O00OO00OO0O ):#line:465
    OO0OO000000O00OO0 ="https://cjhy-isv.isvjcloud.com/wx/completeInfoActivity/save"#line:466
    O0OO00O0000O000OO =f"{O0OOO000OOO00O00O}drawInfoId={O00OO0O00OO00OO0O}&activityId={activityId}&venderId={O0O00O00O0O0OOOO0}&pin={quote_plus(O000O000OOOO0OO0O)}&vcode=&token={token}&fromType=APP"#line:467
    O0OOO00OO0O0O0OOO ={'Host':'cjhy-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://cjhy-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:480
    O0O0O00000O000OOO =requests .request ("POST",OO0OO000000O00OO0 ,headers =O0OOO00OO0O0O0OOO ,data =O0OO00O0000O000OO )#line:481
    OOOO00OOO0O0000OO =O0O0O00000O000OOO .json ()#line:482
    if OOOO00OOO0O0000OO ['result']:#line:483
        return OOOO00OOO0O0000OO ['data']#line:484
    else :#line:485
        print (OOOO00OOO0O0000OO ['errorMessage'])#line:486
if __name__ =='__main__':#line:489
    r =redis_conn ()#line:490
    try :#line:491
        cks =getCk #line:492
        if not cks :#line:493
            sys .exit ()#line:494
    except :#line:495
        print ("未获取到有效COOKIE,退出程序！")#line:496
        sys .exit ()#line:497
    num =0 #line:498
    for cookie in cks [:]:#line:499
        num +=1 #line:500
        if num %9 ==0 :#line:501
            print ("⏰等待5s,休息一下")#line:502
            time .sleep (5 )#line:503
        global ua ,activityCookie ,token #line:504
        ua =userAgent ()#line:505
        try :#line:506
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:507
            pt_pin =unquote_plus (pt_pin )#line:508
        except IndexError :#line:509
            pt_pin =f'用户{num}'#line:510
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:511
        print (datetime .now ())#line:512
        token =getToken (cookie ,r )#line:513
        if token is None :#line:514
            print (f"⚠️获取Token失败！⏰等待2s")#line:515
            time .sleep (2 )#line:516
            continue #line:517
        time .sleep (0.2 )#line:518
        activityCookie =getActivity ()#line:519
        time .sleep (0.3 )#line:520
        getOpenStatus ()#line:521
        time .sleep (0.1 )#line:522
        getSimAct =getSimpleActInfoVo ()#line:523
        venderId =getSimAct ['venderId']#line:524
        activityType =getSimAct ['activityType']#line:525
        time .sleep (0.2 )#line:526
        getPin =getMyPing (venderId )#line:527
        if getPin :#line:528
            nickname =getPin [0 ]#line:529
            secretPin =getPin [1 ]#line:530
            time .sleep (0.2 )#line:531
            getOC =getOpenCardInfo (venderId ,secretPin ,activityType )#line:532
            time .sleep (0.1 )#line:533
            if getOC ['openedCard']:#line:534
                getShopInfo =getShopInfoVO (venderId )#line:535
                shopName =getShopInfo ['shopName']#line:536
                print (f"✅开启{shopName} 店铺完善会员信息有礼")#line:537
                accessLog (venderId ,secretPin ,activityType )#line:538
                time .sleep (0.2 )#line:539
                saveInfo =_O0000O00000OO0O0O (venderId )#line:540
                time .sleep (0.2 )#line:541
                selectBI =selectById (secretPin ,venderId )#line:542
                if selectBI :#line:543
                    print (f"💨{nickname} 已经完善过店铺信息")#line:544
                    continue #line:545
                else :#line:546
                    time .sleep (0.2 )#line:547
                    listDraw =listDrawContent (activityType )#line:548
                    drawInfoId =listDraw [0 ]['drawInfoId']#line:549
                    time .sleep (0.2 )#line:550
                    getInfo ()#line:551
                    time .sleep (0.1 )#line:552
                    sv =save (saveInfo ,venderId ,secretPin ,drawInfoId )#line:553
                    if sv :#line:554
                        drawInfo =sv ['drawInfo']['name']#line:555
                        if drawInfo :#line:556
                            print (f"🎉🎉🎉{nickname} 成功领取 {drawInfo}")#line:557
                        else :#line:558
                            print (f"⛈⛈⛈{nickname} 领取完善有礼奖励失败,请重试~")#line:559
                    else :#line:560
                        print (f"💨{nickname} 已经领过完善有礼奖励~")#line:561
            else :#line:562
                print (f"⛈{nickname} 非店铺会员无法完善信息！")#line:563
                continue #line:564
        time .sleep (2.5 )