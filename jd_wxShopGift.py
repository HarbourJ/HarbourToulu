#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxShopGift.py(店铺特效关注有礼-监控脚本)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('店铺特效关注有礼-JK');
ActivityEntry: https://lzkj-isv.isvjcloud.com/wxShopGift/activity?activityId=971e85d5dfd445e1acfc63bafffb8ecc
               变量 export jd_wxShopGiftId="971e85d5dfd445e1axxxxxxxxxxxx"
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
activityId =os .environ .get ("jd_wxShopGiftId")if os .environ .get ("jd_wxShopGiftId")else ""#line:24
if not activityId :#line:26
    print ("⚠️未发现有效活动变量,退出程序!")#line:27
    sys .exit ()#line:28
activityUrl =f"https://lzkj-isv.isvjcloud.com/wxShopGift/activity?activityId={activityId}"#line:29
def redis_conn ():#line:31
    try :#line:32
        import redis #line:33
        try :#line:34
            O0000O00O0OO0OO00 =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:35
            O000OO0000OOOO000 =redis .Redis (connection_pool =O0000O00O0OO0OO00 )#line:36
            O000OO0000OOOO000 .get ('conn_test')#line:37
            print ('✅redis连接成功')#line:38
            return O000OO0000OOOO000 #line:39
        except :#line:40
            print ("⚠️redis连接异常")#line:41
    except :#line:42
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:43
        sys .exit ()#line:44
def getToken (O000OOOOOO00O0O0O ,r =None ):#line:46
    OO00O0O0000O0O000 =f'{activityUrl.split("com/")[0]}com'#line:47
    try :#line:48
        O00OO0OO000OO000O =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O000OOOOOO00O0O0O )[0 ])#line:50
    except :#line:51
        O00OO0OO000OO000O =O000OOOOOO00O0O0O [:15 ]#line:53
    try :#line:54
        if r is not None :#line:55
            O0OO000O00OOOOOO0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{O00OO0OO000OO000O}')#line:56
            if O0OO000O00OOOOOO0 is not None :#line:58
                print (f"♻️获取缓存Token")#line:59
                return O0OO000O00OOOOOO0 #line:60
            else :#line:61
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O000OOOOOO00O0O0O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:73
                O00OOOO0OO0OOO000 =sign ({"url":f"{OO00O0O0000O0O000}","id":""},'isvObfuscator')#line:74
                OO0O00O00OOOOO000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:76
                if OO0O00O00OOOOO000 .status_code !=200 :#line:77
                    print (OO0O00O00OOOOO000 .status_code )#line:78
                    return #line:79
                else :#line:80
                    if "参数异常"in OO0O00O00OOOOO000 .text :#line:81
                        return #line:82
                O00OO00O000000OO0 =OO0O00O00OOOOO000 .json ()['token']#line:83
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{O00OO0OO000OO000O}',O00OO00O000000OO0 ,ex =1800 ):#line:85
                    print ("✅Token缓存成功")#line:86
                else :#line:87
                    print ("❌Token缓存失败")#line:88
                return O00OO00O000000OO0 #line:89
        else :#line:90
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O000OOOOOO00O0O0O ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:101
            O00OOOO0OO0OOO000 =sign ({"url":f"{OO00O0O0000O0O000}","id":""},'isvObfuscator')#line:102
            OO0O00O00OOOOO000 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:104
            if OO0O00O00OOOOO000 .status_code !=200 :#line:105
                print (OO0O00O00OOOOO000 .status_code )#line:106
                return #line:107
            else :#line:108
                if "参数异常"in OO0O00O00OOOOO000 .text :#line:109
                    return #line:110
            O0OO000O00OOOOOO0 =OO0O00O00OOOOO000 .json ()['token']#line:111
            print (f"✅获取实时Token")#line:112
            return O0OO000O00OOOOOO0 #line:113
    except :#line:114
        return #line:115
def getJdTime ():#line:117
    OOOO00OOO0O00O0O0 =int (round (time .time ()*1000 ))#line:118
    return OOOO00OOO0O00O0O0 #line:119
def randomString (OOO0OOOOO0OOO0O00 ,flag =False ):#line:121
    O000O0O0O00OO0O0O ="0123456789abcdef"#line:122
    if flag :O000O0O0O00OO0O0O =O000O0O0O00OO0O0O .upper ()#line:123
    OO0O0O00OOO0O0000 =[random .choice (O000O0O0O00OO0O0O )for _O0O0O00OO0OO0O0O0 in range (OOO0OOOOO0OOO0O00 )]#line:124
    return ''.join (OO0O0O00OOO0O0000 )#line:125
def refresh_cookies (OOO0OOO0O0OOO0O00 ):#line:127
    if OOO0OOO0O0OOO0O00 .cookies :#line:128
        OO00OOO000O0OO0OO =OOO0OOO0O0OOO0O00 .cookies .get_dict ()#line:129
        O00000O000OO00OO0 =[(OOO00OO0000O00O0O +"="+OO00OOO000O0OO0OO [OOO00OO0000O00O0O ])for OOO00OO0000O00O0O in OO00OOO000O0OO0OO ]#line:130
        global activityCookie #line:131
        O0OOOOOO00O000OO0 =[OOOOOO000000O0O0O for OOOOOO000000O0O0O in activityCookie .split (';')if OOOOOO000000O0O0O !='']#line:132
        for OO0OOO0000OOO0O0O in O0OOOOOO00O000OO0 :#line:133
            for OO0OO0OOOO0OO0O00 in O00000O000OO00OO0 :#line:134
                if OO0OOO0000OOO0O0O .split ('=')[0 ]==OO0OO0OOOO0OO0O00 .split ('=')[0 ]:#line:135
                    if OO0OOO0000OOO0O0O .split ('=')[1 ]!=OO0OO0OOOO0OO0O00 .split ('=')[1 ]:#line:136
                        O0OOOOOO00O000OO0 .remove (OO0OOO0000OOO0O0O )#line:137
        activityCookie =''.join (sorted ([(OO0O0OO00000O0OOO +";")for OO0O0OO00000O0OOO in list (set (O0OOOOOO00O000OO0 +O00000O000OO00OO0 ))]))#line:138
def getActivity ():#line:140
    OOO0O00O0O00OO00O =f"https://lzkj-isv.isvjcloud.com/wxShopGift/activity?activityId={activityId}"#line:141
    OO00OOOOOOO0O0O00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:149
    OOOOO0O00OO00O0OO =requests .request ("GET",OOO0O00O0O00OO00O ,headers =OO00OOOOOOO0O0O00 )#line:150
    if OOOOO0O00OO00O0OO .status_code ==200 :#line:151
        if OOOOO0O00OO00O0OO .cookies :#line:152
            O0O00OO0O00OO00OO =OOOOO0O00OO00O0OO .cookies .get_dict ()#line:153
            OOOO0OOOO000000O0 =[(OOO000OO0OO000O0O +"="+O0O00OO0O00OO00OO [OOO000OO0OO000O0O ])for OOO000OO0OO000O0O in O0O00OO0O00OO00OO ]#line:154
            O000000O000O00OOO =''.join (sorted ([(O0000OOO00O0OOOOO +";")for O0000OOO00O0OOOOO in OOOO0OOOO000000O0 ]))#line:155
        return O000000O000O00OOO #line:156
    else :#line:157
        print (OOOOO0O00OO00O0OO .status_code )#line:158
        print ("⚠️疑似ip黑了")#line:159
        sys .exit ()#line:160
def getSystemConfigForNew ():#line:162
    OO0OOO00OOOOO00OO ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:163
    O0O00O00O0OOO0OOO =f'activityId={activityId}&activityType=99'#line:164
    O0O0000OO00OOO0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:177
    O000OO0OO0O0O0OO0 =requests .request ("POST",OO0OOO00OOOOO00OO ,headers =O0O0000OO00OOO0OO ,data =O0O00O00O0OOO0OOO )#line:178
    refresh_cookies (O000OO0OO0O0O0OO0 )#line:179
def getSimpleActInfoVo ():#line:181
    O0OOO00O00O0OO00O ="https://lzkj-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:182
    O0OOOOOOO00O0OOO0 =f"activityId={activityId}"#line:183
    OO0OO00O0OOO0O0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:196
    OO0O00OOO00O00OO0 =requests .request ("POST",O0OOO00O00O0OO00O ,headers =OO0OO00O0OOO0O0OO ,data =O0OOOOOOO00O0OOO0 )#line:197
    refresh_cookies (OO0O00OOO00O00OO0 )#line:198
    OOOOO00OOOOO0000O =OO0O00OOO00O00OO0 .json ()#line:199
    if OOOOO00OOOOO0000O ['result']:#line:200
        return OOOOO00OOOOO0000O ['data']#line:201
def getMyPing (OOOO00000OO000000 ):#line:203
    O000O00O00OO0OO00 ="https://lzkj-isv.isvjcloud.com/customer/getMyPing"#line:204
    OO0OO00O0OO00OO00 =f"userId={OOOO00000OO000000}&token={token}&fromType=APP_shopGift"#line:205
    O0OO0OO00O0O0OO0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:218
    OO00O000OOO00O0OO =requests .request ("POST",O000O00O00OO0OO00 ,headers =O0OO0OO00O0O0OO0O ,data =OO0OO00O0OO00OO00 )#line:219
    refresh_cookies (OO00O000OOO00O0OO )#line:220
    O0000O0OOOOO0OOOO =OO00O000OOO00O0OO .json ()#line:221
    if O0000O0OOOOO0OOOO ['result']:#line:222
        return O0000O0OOOOO0OOOO ['data']['nickname'],O0000O0OOOOO0OOOO ['data']['secretPin']#line:223
    else :#line:224
        print (f"⚠️{O0000O0OOOOO0OOOO['errorMessage']}")#line:225
def accessLogWithAD (OOO0OO000OO0OOOOO ,O00O0O0O00O000000 ):#line:227
    OOO000OO000O0O0OO ="https://lzkj-isv.isvjcloud.com/common/accessLogWithAD"#line:228
    OOO00OO0OOOO000OO =f"venderId={OOO0OO000OO0OOOOO}&code=24&pin={quote_plus(O00O0O0O00O000000)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource="#line:229
    O0OO000O0OO00O0O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:242
    O00O0OO000OOOO0O0 =requests .request ("POST",OOO000OO000O0O0OO ,headers =O0OO000O0OO00O0O0 ,data =OOO00OO0OOOO000OO )#line:243
    refresh_cookies (O00O0OO000OOOO0O0 )#line:244
def activityContent (OO00000OOO0O0OO00 ):#line:246
    OOO0OOOO0O00O00O0 ="https://lzkj-isv.isvjcloud.com/wxShopGift/activityContent"#line:247
    OO0OOO0OO00O0OO00 =f"activityId={activityId}&buyerPin={quote_plus(OO00000OOO0O0OO00)}"#line:248
    OOO00OOOO0O0OO000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:261
    OOOO0O0OO0OOOOO0O =requests .request ("POST",OOO0OOOO0O00O00O0 ,headers =OOO00OOOO0O0OO000 ,data =OO0OOO0OO00O0OO00 )#line:262
    refresh_cookies (OOOO0O0OO0OOOOO0O )#line:263
    O0OOOO0OO000O00OO =OOOO0O0OO0OOOOO0O .json ()#line:264
    O000O0OO00OOOOO0O =True #line:265
    OO0OOO000OOOO00OO =''#line:266
    if O0OOOO0OO000O00OO ['result']:#line:267
        O00OOOOOOO0OOO0OO =O0OOOO0OO000O00OO ['data']['endTime']#line:268
        O000O0000OOOO0O00 =O0OOOO0OO000O00OO ['data']['list']#line:269
        if getJdTime ()>O00OOOOOOO0OOO0OO :#line:270
            print ("⛈活动已结束,下次早点来~")#line:271
            sys .exit ()#line:272
        if len (O000O0000OOOO0O00 )==0 :#line:273
            print ("礼品已领完")#line:274
            O000O0OO00OOOOO0O =False #line:275
            return O000O0OO00OOOOO0O #line:276
        for O0OOO00OOOO00OOO0 in O000O0000OOOO0O00 :#line:277
            OO0OOO000OOOO00OO +=str (O0OOO00OOOO00OOO0 ['takeNum'])+O0OOO00OOOO00OOO0 ['type']+''#line:278
        if len (OO0OOO000OOOO00OO )>0 :#line:279
            OO0OOO000OOOO00OO =OO0OOO000OOOO00OO .replace ('jd','京豆').replace ('jf','积分').replace ('dq','东券')#line:280
    else :#line:281
        print (f"⛈{O0OOOO0OO000O00OO['errorMessage']}")#line:282
        sys .exit ()#line:283
    return OO0OOO000OOOO00OO ,O000O0OO00OOOOO0O #line:284
def draw (O0O00OOO0O0O0O0O0 ,OO000OOOO00OOO000 ,OOOO0O0O00O00OO00 ):#line:286
    O0OO0O000O0O000O0 ="https://lzkj-isv.isvjcloud.com/wxShopGift/draw"#line:287
    OOO0O000000OO0O00 =f"activityId={activityId}&buyerPin={quote_plus(O0O00OOO0O0O0O0O0)}&hasFollow=false&accessType=app"#line:288
    OOOOOO000OOO000O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:301
    O0O0000O0O0000000 =requests .request ("POST",O0OO0O000O0O000O0 ,headers =OOOOOO000OOO000O0 ,data =OOO0O000000OO0O00 )#line:302
    OO000O0O0OO0OOOOO =O0O0000O0O0000000 .json ()#line:303
    if OO000O0O0OO0OOOOO ['result']:#line:304
        print (f"🎉🎉🎉{OO000OOOO00OOO000} 成功领取 {OOOO0O0O00O00OO00}")#line:305
    else :#line:306
        print (f"⛈⛈⛈{OO000OOOO00OOO000} {OO000O0O0OO0OOOOO['errorMessage']}")#line:307
def attendLog (O0OOOO00O0O00000O ,OOO0000O0O000OOOO ):#line:309
    O00000O0O0O0OOOO0 ="https://lzkj-isv.isvjcloud.com/common/attendLog"#line:310
    OO000O00O00O000OO =f"venderId={O0OOOO00O0O00000O}&activityType=24&activityId={activityId}&pin={quote_plus(OOO0000O0O000OOOO)}&clientType=app"#line:311
    O00O00OO0O0OO0OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:324
    requests .request ("POST",O00000O0O0O0OOOO0 ,headers =O00O00OO0O0OO0OO0 ,data =OO000O00O00O000OO )#line:325
if __name__ =='__main__':#line:328
    r =redis_conn ()#line:329
    try :#line:330
        cks =getCk #line:331
        if not cks :#line:332
            sys .exit ()#line:333
    except :#line:334
        print ("未获取到有效COOKIE,退出程序！")#line:335
        sys .exit ()#line:336
    num =0 #line:337
    for cookie in cks [:]:#line:338
        num +=1 #line:339
        if num %9 ==0 :#line:340
            print ("⏰等待8s,休息一下")#line:341
            time .sleep (8 )#line:342
        global ua ,activityCookie ,token #line:343
        ua =userAgent ()#line:344
        try :#line:345
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:346
            pt_pin =unquote_plus (pt_pin )#line:347
        except IndexError :#line:348
            pt_pin =f'用户{num}'#line:349
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:350
        print (datetime .now ())#line:351
        token =getToken (cookie ,r )#line:352
        if token is None :#line:353
            print (f"⚠️获取Token失败！⏰等待2s")#line:354
            time .sleep (2 )#line:355
            continue #line:356
        time .sleep (0.5 )#line:357
        activityCookie =getActivity ()#line:358
        time .sleep (0.5 )#line:359
        getSystemConfigForNew ()#line:360
        time .sleep (0.3 )#line:361
        getSimAct =getSimpleActInfoVo ()#line:362
        venderId =getSimAct ['venderId']#line:363
        time .sleep (0.2 )#line:364
        getPin =getMyPing (venderId )#line:365
        if getPin is not None :#line:366
            nickname =getPin [0 ]#line:367
            secretPin =getPin [1 ]#line:368
            time .sleep (0.3 )#line:369
            accessLogWithAD (venderId ,secretPin )#line:370
            time .sleep (0.5 )#line:371
            actCon =activityContent (secretPin )#line:372
            if not actCon :#line:373
                continue #line:374
            if not actCon [1 ]:#line:375
                continue #line:376
            reward =actCon [0 ]#line:377
            time .sleep (0.8 )#line:378
            draw (secretPin ,nickname ,reward )#line:379
        time .sleep (5 )