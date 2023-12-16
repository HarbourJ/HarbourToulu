#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_joinCommon_opencard.py(通用开卡-joinCommon系列)
Author: HarbourJ
Date: 2022/8/12 20:37
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('通用开卡-joinCommon系列');
ActivityEntry: https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity?activityId=2b870a1a74504c45995a5d5119487f3a
Description: dingzhi/joinCommon系列通用开卡脚本(通常情况下,开一张卡10豆，邀请成功获得20豆)。
            本地sign算法+redis缓存Token
            变量: export jd_joinCommonId="2b870a1a7450xxxxxxxxxxxxx&1000000904" 变量值需要传入活动id&shopId
Update: 2022/11/01 更新入会算法，内置船新入会本地算法
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
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")#line:13
    sys .exit ()#line:14
try :#line:15
    from jdCookie import get_cookies #line:16
    getCk =get_cookies ()#line:17
except :#line:18
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:19
    sys .exit (3 )#line:20
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:22
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:23
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:24
jd_joinCommonId =os .environ .get ("jd_joinCommonId")if os .environ .get ("jd_joinCommonId")else ""#line:25
inviterUuid =os .environ .get ("jd_joinCommon_uuid")if os .environ .get ("jd_joinCommon_uuid")else ""#line:26
if not jd_joinCommonId :#line:28
    print ("⚠️未发现有效活动变量,退出程序!")#line:29
    sys .exit ()#line:30
if "lzdz1_remote"in jd_joinCommonId :#line:32
    jd_joinCommonId_remote =remote_redis (jd_joinCommonId )#line:33
    jd_joinCommonId =jd_joinCommonId_remote #line:34
else :#line:35
    if "&"not in jd_joinCommonId :#line:36
        print ("⚠️活动变量错误,退出程序!")#line:37
        sys .exit ()#line:38
activityId =jd_joinCommonId .split ('&')[0 ]#line:40
shopId =jd_joinCommonId .split ('&')[1 ]#line:41
activity_url =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={inviterUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:42
print (f"【🛳活动入口】https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}")#line:43
def redis_conn ():#line:45
    try :#line:46
        import redis #line:47
        try :#line:48
            O000000O0O0000O0O =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:49
            OO00O0O0OO0O00OOO =redis .Redis (connection_pool =O000000O0O0000O0O )#line:50
            OO00O0O0OO0O00OOO .get ('conn_test')#line:51
            print ('✅redis连接成功')#line:52
            return OO00O0O0OO0O00OOO #line:53
        except :#line:54
            print ("⚠️redis连接异常")#line:55
    except :#line:56
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:57
        sys .exit ()#line:58
def getToken (OO0OOOOOO00O00O00 ,r =None ):#line:60
    O000O0O00O00000OO =f'{activityUrl.split("com/")[0]}com'#line:61
    try :#line:62
        OO0OO0OOOO000O0O0 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OO0OOOOOO00O00O00 )[0 ])#line:63
    except :#line:64
        OO0OO0OOOO000O0O0 =OO0OOOOOO00O00O00 [:15 ]#line:65
    try :#line:66
        try :#line:67
            OOO00OOOO00000O0O =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO0OO0OOOO000O0O0}')#line:68
        except Exception as O00O00000OO0OO0O0 :#line:69
            OOO00OOOO00000O0O =None #line:71
        if OOO00OOOO00000O0O is not None :#line:72
            print (f"♻️获取缓存Token")#line:73
            return OOO00OOOO00000O0O #line:74
        else :#line:75
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0OOOOOO00O00O00 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:86
            sign ({"url":f"{O000O0O00O00000OO}","id":""},'isvObfuscator')#line:87
            OO0O0O00OOO0OO00O =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:88
            if OO0O0O00OOO0OO00O .status_code !=200 :#line:89
                print (OO0O0O00OOO0OO00O .status_code )#line:90
                return #line:91
            else :#line:92
                if "参数异常"in OO0O0O00OOO0OO00O .text :#line:93
                    print (OO0O0O00OOO0OO00O .text )#line:94
                    return #line:95
            O00O0OO0000O0O000 =OO0O0O00OOO0OO00O .json ()['token']#line:96
            try :#line:97
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO0OO0OOOO000O0O0}',O00O0OO0000O0O000 ,ex =1800 ):#line:98
                    print ("✅Token缓存成功")#line:99
                else :#line:100
                    print ("❌Token缓存失败")#line:101
            except Exception as O00O00000OO0OO0O0 :#line:102
                print (f"✅获取实时Token")#line:104
            return O00O0OO0000O0O000 #line:105
    except Exception as O00O00000OO0OO0O0 :#line:106
        print (f"Get Token Error: {str(O00O00000OO0OO0O0)}")#line:107
        return #line:108
def getJdTime ():#line:110
    OOO0000O0O00000OO =int (round (time .time ()*1000 ))#line:111
    return OOO0000O0O00000OO #line:112
def randomString (O0O0OOOOO0O00O000 ,flag =False ):#line:114
    O00OO0O00OO00OO00 ="0123456789abcdef"#line:115
    if flag :O00OO0O00OO00OO00 =O00OO0O00OO00OO00 .upper ()#line:116
    O000OO0OO0OOOOO0O =[random .choice (O00OO0O00OO00OO00 )for _OOO0OOOOOOOO0000O in range (O0O0OOOOO0O00O000 )]#line:117
    return ''.join (O000OO0OO0OOOOO0O )#line:118
def refresh_cookies (OOO0OO0O0OOO000OO ):#line:120
    if OOO0OO0O0OOO000OO .cookies :#line:121
        O0O00OOOOOOOOOOO0 =OOO0OO0O0OOO000OO .cookies .get_dict ()#line:122
        O0O000O0OO000O00O =[(OOOO0O0O00OOOOO00 +"="+O0O00OOOOOOOOOOO0 [OOOO0O0O00OOOOO00 ])for OOOO0O0O00OOOOO00 in O0O00OOOOOOOOOOO0 ]#line:123
        global activityCookie #line:124
        O0O0OOO0OOOOOO0O0 =[OOOO0OOO00OO0O00O for OOOO0OOO00OO0O00O in activityCookie .split (';')if OOOO0OOO00OO0O00O !='']#line:125
        for O00OOOO0O00O000O0 in O0O0OOO0OOOOOO0O0 :#line:126
            for OOO00OOOOO000O0OO in O0O000O0OO000O00O :#line:127
                if O00OOOO0O00O000O0 .split ('=')[0 ]==OOO00OOOOO000O0OO .split ('=')[0 ]:#line:128
                    if O00OOOO0O00O000O0 .split ('=')[1 ]!=OOO00OOOOO000O0OO .split ('=')[1 ]:#line:129
                        O0O0OOO0OOOOOO0O0 .remove (O00OOOO0O00O000O0 )#line:130
        activityCookie =''.join (sorted ([(OOOOO0OOOOOO00000 +";")for OOOOO0OOOOOO00000 in list (set (O0O0OOO0OOOOOO0O0 +O0O000O0OO000O00O ))]))#line:131
def getActivity ():#line:133
    OOOOOO0OO00000O00 =activityUrl #line:134
    O0OO00O0O0O00OO00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:142
    OO000O0OO0O00000O =requests .request ("GET",OOOOOO0OO00000O00 ,headers =O0OO00O0O0O00OO00 )#line:144
    if OO000O0OO0O00000O .status_code ==200 :#line:145
        if OO000O0OO0O00000O .cookies :#line:146
            O0OO0000OOOO000O0 =OO000O0OO0O00000O .cookies .get_dict ()#line:147
            OO00OOOOO0OO0OOOO =[(OO000O000O0OO00OO +"="+O0OO0000OOOO000O0 [OO000O000O0OO00OO ])for OO000O000O0OO00OO in O0OO0000OOOO000O0 ]#line:148
            OO0OOOOO0OO0OOO0O =''.join (sorted ([(O0O0OO0O0OO000O00 +";")for O0O0OO0O0OO000O00 in OO00OOOOO0OO0OOOO ]))#line:149
        return OO0OOOOO0OO0OOO0O #line:150
    else :#line:151
        print (OO000O0OO0O00000O .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:152
        sys .exit ()#line:153
def getSystemConfigForNew ():#line:155
    O0OOO0O00O00O0OOO ="https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:156
    O0OOO0000O00O0O0O =f'activityId={activityId}&activityType=99'#line:157
    O0000OO0OO00OOOOO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:170
    OOOO00O00OOO0OOOO =requests .request ("POST",O0OOO0O00O00O0OOO ,headers =O0000OO0OO00OOOOO ,data =O0OOO0000O00O0O0O )#line:171
    refresh_cookies (OOOO00O00OOO0OOOO )#line:172
def getSimpleActInfoVo ():#line:174
    OO0OO0OOO0OOO0OOO ="https://lzdz1-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"#line:175
    O0O000000O00O00OO =f"activityId={activityId}"#line:176
    OOO0OO0O00OOO0O00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:189
    O0O0000OO0O0O000O =requests .request ("POST",OO0OO0OOO0OOO0OOO ,headers =OOO0OO0O00OOO0O00 ,data =O0O000000O00O00OO )#line:190
    refresh_cookies (O0O0000OO0O0O000O )#line:191
    OO0000OOOO0O00000 =O0O0000OO0O0O000O .json ()#line:192
    if OO0000OOOO0O00000 ['result']:#line:193
        return OO0000OOOO0O00000 ['data']#line:194
    else :#line:195
        print (OO0000OOOO0O00000 ['errorMessage'])#line:196
def getMyPing (OO0000OOOO0OOO00O ,OO000OO00000O0OOO ):#line:198
    OO00O0O00O0O0OOO0 ="https://lzdz1-isv.isvjcloud.com/customer/getMyPing"#line:199
    OOO000O0OO00O0O0O =f"userId={OO000OO00000O0OOO}&token={token}&fromType=APP"#line:200
    O0O0OOO00O0OO000O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:213
    OO00O00O0O0OO0O0O =requests .request ("POST",OO00O0O00O0O0OOO0 ,headers =O0O0OOO00O0OO000O ,data =OOO000O0OO00O0O0O )#line:214
    refresh_cookies (OO00O00O0O0OO0O0O )#line:215
    OOO0O00O00O0OOOO0 =OO00O00O0O0OO0O0O .json ()#line:216
    if OOO0O00O00O0OOOO0 ['result']:#line:217
        return OOO0O00O00O0OOOO0 ['data']['nickname'],OOO0O00O00O0OOOO0 ['data']['secretPin']#line:218
    else :#line:219
        print (f"⚠️{OOO0O00O00O0OOOO0['errorMessage']}")#line:220
        if OO0000OOOO0OOO00O ==1 and "火爆"in OOO0O00O00O0OOOO0 ['errorMessage']:#line:221
            print (f"\t⛈车头黑,退出本程序！")#line:222
            sys .exit ()#line:223
def accessLogWithAD (OO0OOOOOOOO0OO00O ,OOOO0OOOOOOOOOO00 ):#line:225
    O00O0O0O0O0000O0O ="https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"#line:226
    O00000O00OOOOOOO0 =f"venderId={OO0OOOOOOOO0OO00O}&code=99&pin={quote_plus(OOOO0OOOOOOOOOO00)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource=null"#line:227
    OO00OO00OO0O00000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:240
    O0OOO0000000O0000 =requests .request ("POST",O00O0O0O0O0000O0O ,headers =OO00OO00OO0O00000 ,data =O00000O00OOOOOOO0 )#line:241
    refresh_cookies (O0OOO0000000O0000 )#line:242
def getSystime ():#line:244
    O00O0OO0O000OOOO0 ="https://lzdz1-isv.isvjcloud.com/common/getSystime"#line:245
    OO000OOO00OOOOO00 ={'Host':'lzdz1-isv.isvjcloud.com','Origin':'https://lzdz1-isv.isvjcloud.com','Accept-Encoding':'gzip, deflate, br','Cookie':activityCookie ,'Content-Length':'0','Connection':'keep-alive','Accept':'application/json','User-Agent':ua ,'Referer':activityUrl ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','X-Requested-With':'XMLHttpRequest'}#line:258
    O00OOO0OOOOOO00OO =requests .request ("POST",O00O0OO0O000OOOO0 ,headers =OO000OOO00OOOOO00 )#line:259
    refresh_cookies (O00OOO0OOOOOO00OO )#line:260
def getUserInfo (O0O0O0000O0O0O00O ):#line:262
    OOOO0OOO000O0O00O ="https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo"#line:263
    O0O00O00OOOO00OO0 =f"pin={quote_plus(O0O0O0000O0O0O00O)}"#line:264
    OOO0O00O0OO00O00O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:277
    O0OO000OO000OOOO0 =requests .request ("POST",OOOO0OOO000O0O00O ,headers =OOO0O00O0OO00O00O ,data =O0O00O00OOOO00OO0 )#line:278
    refresh_cookies (O0OO000OO000OOOO0 )#line:279
    O0000O00OO0OOO0OO =O0OO000OO000OOOO0 .json ()#line:280
    if O0000O00OO0OOO0OO ['result']:#line:281
        return O0000O00OO0OOO0OO ['data']['nickname'],O0000O00OO0OOO0OO ['data']['yunMidImageUrl'],O0000O00OO0OOO0OO ['data']['pin']#line:282
    else :#line:283
        print (O0000O00OO0OOO0OO ['errorMessage'])#line:284
def activityContent (O0O000OOOO0O00000 ,O0O0O000OO0OO0OO0 ,O000OO00OO0O000O0 ):#line:286
    O000OO0O00OOO0O0O ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activityContent"#line:287
    try :#line:288
        O0OO00000OOOO0000 =quote_plus (O0O0O000OO0OO0OO0 )#line:289
    except :#line:290
        O0OO00000OOOO0000 =quote_plus ("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")#line:291
    OOO0O00O0O0O000O0 =f"activityId={activityId}&pin={quote_plus(O0O000OOOO0O00000)}&pinImg={O0OO00000OOOO0000}&nick={quote_plus(O000OO00OO0O000O0)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}"#line:292
    O00OOO0O00000OO00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:305
    OO0O0OO0OOO0OOOOO =requests .request ("POST",O000OO0O00OOO0O0O ,headers =O00OOO0O00000OO00 ,data =OOO0O00O0O0O000O0 )#line:306
    refresh_cookies (OO0O0OO0OOO0OOOOO )#line:307
    OOOO00OOO0O000O0O =OO0O0OO0OOO0OOOOO .json ()#line:308
    if OOOO00OOO0O000O0O ['result']:#line:309
        return OOOO00OOO0O000O0O ['data']#line:310
    else :#line:311
        print (OOOO00OOO0O000O0O ['errorMessage'])#line:312
        if "活动已结束"in OOOO00OOO0O000O0O ['errorMessage']:#line:313
            sys .exit ()#line:314
def shareRecord (O0OOO0OOOO000O0OO ,OOO00000OOO0O0O00 ):#line:316
    O0O00OOO0000O00OO ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/shareRecord"#line:317
    O0O0OO000OOOOO0O0 =f"activityId={activityId}&pin={quote_plus(O0OOO0OOOO000O0OO)}&uuid={OOO00000OOO0O0O00}&num=30"#line:318
    OOO00OOO00O0O0000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:331
    O00OO000O00O0OO00 =requests .request ("POST",O0O00OOO0000O00OO ,headers =OOO00OOO00O0O0000 ,data =O0O0OO000OOOOO0O0 )#line:332
    refresh_cookies (O00OO000O00O0OO00 )#line:333
def taskRecord (OOO0O0O0O0000O0O0 ,O0000O0O0O000OOOO ):#line:335
    O0OO00O000O0O0OO0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/taskRecord"#line:336
    O000O0O000OO0OO00 =f"activityId={activityId}&pin={quote_plus(OOO0O0O0O0000O0O0)}&uuid={O0000O0O0O000OOOO}&taskType="#line:337
    OOO000OO000OOO0OO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:350
    OO0OO0O0O0O0OOO00 =requests .request ("POST",O0OO00O000O0O0OO0 ,headers =OOO000OO000OOO0OO ,data =O000O0O000OO0OO00 )#line:351
    refresh_cookies (OO0OO0O0O0O0OOO00 )#line:352
def drawContent (OO0O0OO000000000O ,O00OOOO000O00000O ):#line:354
    O00O0000OOOO0O0OO ="https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent"#line:355
    O0OOO00O00O0O0OOO =f"activityId={OO0O0OO000000000O}&pin={quote_plus(O00OOOO000O00000O)}"#line:356
    O00OO0OOOOO0OOOO0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:369
    requests .request ("POST",O00O0000OOOO0O0OO ,headers =O00OO0OOOOO0OOOO0 ,data =O0OOO00O00O0O0OOO )#line:370
def taskInfo (O00OO0OOOOO0O000O ):#line:372
    OOO0000OOO0OOO000 ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/taskInfo"#line:373
    OOOOOOO0000O00O00 =f"activityId={activityId}&pin={quote_plus(O00OO0OOOOO0O000O)}"#line:374
    O00O00O0O000O0000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:387
    O00OOOO00OO0O000O =requests .request ("POST",OOO0000OOO0OOO000 ,headers =O00O00O0O000O0000 ,data =OOOOOOO0000O00O00 )#line:388
    O000O0OO00OOO0000 =O00OOOO00OO0O000O .json ()#line:389
    if O000O0OO00OOO0000 ['result']:#line:390
        return O000O0OO00OOO0000 ['data']#line:391
    else :#line:392
        print (O000O0OO00OOO0000 ['errorMessage'])#line:393
def assist (OO00O00OO000O0OOO ,OOO00O00OOOOO000O ):#line:395
    O0O0OOO0O0OOO0O0O ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/assist"#line:396
    O0OO0O0OO0O0OOO00 =f"activityId={activityId}&pin={quote_plus(OO00O00OO000O0OOO)}&uuid={OOO00O00OOOOO000O}&shareUuid={shareUuid}"#line:397
    OOO000OO0000OOO00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:410
    O0O000OO00OO0OO0O =requests .request ("POST",O0O0OOO0O0OOO0O0O ,headers =OOO000OO0000OOO00 ,data =O0OO0O0OO0O0OOO00 )#line:411
    O00O0O00000O000O0 =O0O000OO00OO0OO0O .json ()#line:412
    if O00O0O00000O000O0 ['result']:#line:413
        return O00O0O00000O000O0 ['data']#line:414
    else :#line:415
        print (O00O0O00000O000O0 ['errorMessage'])#line:416
def doTask (O0OOOO0OO00OOO000 ,OOO00O00000000000 ,O00OOO0O00O0OOOO0 ):#line:418
    OO00OO00OOO0000O0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/doTask"#line:419
    O0O00OOO00OOO0000 =f"activityId={activityId}&uuid={O0OOOO0OO00OOO000}&pin={quote_plus(OOO00O00000000000)}&taskType={O00OOO0O00O0OOOO0}&taskValue="#line:420
    OO0O00OOOOO00O000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:433
    O0O0O000OOO00O000 =requests .request ("POST",OO00OO00OOO0000O0 ,headers =OO0O00OOOOO00O000 ,data =O0O00OOO00OOO0000 )#line:434
    O0OO00O000OOOOO00 =O0O0O000OOO00O000 .json ()#line:435
    print ('doTask',O0OO00O000OOOOO00 )#line:436
    if O0OO00O000OOOOO00 ['result']:#line:437
        OOOO0OOO0000OO00O =O0OO00O000OOOOO00 ['data']#line:438
        if OOOO0OOO0000OO00O ['score']==0 :#line:439
            print ("\t获得 💨💨💨")#line:440
        else :#line:441
            print (f"\t🎉获得{OOOO0OOO0000OO00O['score']}积分")#line:442
    else :#line:443
        print (O0OO00O000OOOOO00 ['errorMessage'])#line:444
def bindWithVender (O0O000O0000O0O000 ,OO0OO0OO0OO0OO0O0 ):#line:446
    try :#line:447
        OO0OOO0OO0O0OOO00 ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':OO0OO0OO0OO0OO0O0 ,'shopId':OO0OO0OO0OO0OO0O0 ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:456
        O0OOOO0O0OOOOOOO0 ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':O0O000O0000O0O000 }#line:469
        O0O000000OO00OO00 =requests .request ("POST","https://api.m.jd.com/",headers =O0OOOO0O0OOOOOOO0 ,data =OO0OOO0OO0O0OOO00 ,timeout =10 ).text #line:470
        O0OOOOOOO0OO0O0OO =json .loads (O0O000000OO00OO00 )#line:471
        if O0OOOOOOO0OO0O0OO ['success']:#line:472
            return O0OOOOOOO0OO0O0OO ['message'],O0OOOOOOO0OO0O0OO ['result']['giftInfo']if O0OOOOOOO0OO0O0OO ['result']else ""#line:473
    except Exception as O000OOOO00O000OOO :#line:474
        print (f"bindWithVender Error: {OO0OO0OO0OO0OO0O0} {O000OOOO00O000OOO}")#line:475
def getShopOpenCardInfo (OOO0O0O00OOO00OOO ,O0O0OO000OO0OO0OO ):#line:477
    try :#line:478
        OOOO0O0OO0OO0O000 ={"venderId":str (O0O0OO000OO0OO0OO ),"channel":"401"}#line:479
        OOOOOO0000O00OO00 =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OOOO0O0OO0OO0O000)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:480
        O0O0OO00OOOO00O0O ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OOO0O0O00OOO00OOO ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate'}#line:490
        O00OO00OOO0OO0OOO =requests .get (url =OOOOOO0000O00OO00 ,headers =O0O0OO00OOOO00O0O ,timeout =5 ).text #line:491
        OOO0OO0OOO0OO0OOO =json .loads (O00OO00OOO0OO0OOO )#line:492
        if OOO0OO0OOO0OO0OOO ['success']:#line:493
            O00O000OO0OOOOOO0 =OOO0OO0OOO0OO0OOO ['result']['shopMemberCardInfo']['venderCardName']#line:494
            return O00O000OO0OOOOOO0 #line:495
        else :#line:496
            return O0O0OO000OO0OO0OO #line:497
    except :#line:498
        return O0O0OO000OO0OO0OO #line:499
if __name__ =='__main__':#line:502
    r =redis_conn ()#line:503
    try :#line:504
        cks =getCk #line:505
        if not cks :#line:506
            sys .exit ()#line:507
    except :#line:508
        print ("未获取到有效COOKIE,退出程序！")#line:509
        sys .exit ()#line:510
    global shareUuid ,inviteSuccNum ,activityUrl ,firstCk #line:511
    inviteSuccNum =0 #line:512
    if len (cks )==1 :#line:513
        shareUuid =inviterUuid #line:514
        activityUrl =activity_url #line:515
    else :#line:516
        shareUuid =remote_redis (f"lzdz1_{activityId}",2 )#line:517
        activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:518
    num =0 #line:519
    for cookie in cks [:]:#line:520
        num +=1 #line:521
        if num ==1 :#line:522
            firstCk =cookie #line:523
        if num %8 ==0 :#line:524
            print ("⏰等待10s,休息一下")#line:525
            time .sleep (10 )#line:526
        global ua ,activityCookie ,token #line:527
        ua =userAgent ()#line:528
        try :#line:529
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:530
            pt_pin =unquote_plus (pt_pin )#line:531
        except IndexError :#line:532
            pt_pin =re .compile (r'pin=(.*?);').findall (cookie )[0 ]#line:533
            pt_pin =unquote_plus (pt_pin )#line:534
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:535
        print (datetime .now ())#line:536
        token =getToken (cookie ,r )#line:538
        if token is None :#line:539
            if num ==1 :#line:540
                print (f"⚠️车头获取Token失败,退出本程序！")#line:541
                sys .exit ()#line:542
            print (f"⚠️获取Token失败！⏰等待3s")#line:543
            time .sleep (3 )#line:544
            continue #line:545
        time .sleep (0.5 )#line:546
        activityCookie =getActivity ()#line:547
        time .sleep (0.5 )#line:548
        getSystemConfigForNew ()#line:549
        time .sleep (0.3 )#line:550
        getSimAct =getSimpleActInfoVo ()#line:551
        if getSimAct :#line:552
            venderId =getSimAct ['venderId']#line:553
        else :#line:554
            venderId =shopId #line:555
        time .sleep (0.2 )#line:556
        getPin =getMyPing (num ,venderId )#line:557
        if getPin is not None :#line:558
            nickname =getPin [0 ]#line:559
            secretPin =getPin [1 ]#line:560
            time .sleep (0.5 )#line:561
            accessLogWithAD (venderId ,secretPin )#line:562
            time .sleep (0.5 )#line:563
            userInfo =getUserInfo (secretPin )#line:564
            time .sleep (0.8 )#line:565
            nickname =userInfo [0 ]#line:566
            yunMidImageUrl =userInfo [1 ]#line:567
            pin =userInfo [2 ]#line:568
            actContent =activityContent (pin ,yunMidImageUrl ,nickname )#line:569
            if not actContent :#line:570
                if num ==1 :#line:571
                    print ("⚠️无法获取车头邀请码,退出本程序！")#line:572
                    sys .exit ()#line:573
                continue #line:574
            hasEnd =actContent ['hasEnd']#line:575
            if hasEnd :#line:576
                print ("活动已结束，下次早点来~")#line:577
                sys .exit ()#line:578
            print (f"✅开启【{actContent['activityName']}】活动\n")#line:579
            if num ==1 :#line:580
                print (f"🛳 已邀请{actContent['actorInfo']['totalAssistCount']}, 有效助力{actContent['actorInfo']['assistCount']}")#line:581
            actorUuid =actContent ['actorInfo']['uuid']#line:582
            taskType =actContent ['taskType']#line:583
            print (f"邀请码->: {actorUuid}")#line:584
            print (f"准备助力->: {shareUuid}")#line:585
            time .sleep (0.5 )#line:586
            shareRecord (pin ,actorUuid )#line:587
            time .sleep (0.5 )#line:588
            taskRecord (pin ,actorUuid )#line:589
            time .sleep (0.5 )#line:590
            print ("现在去一键关注店铺")#line:591
            doTask (actorUuid ,pin ,20 )#line:592
            time .sleep (1 )#line:593
            doTask (actorUuid ,pin ,23 )#line:594
            time .sleep (1 )#line:595
            ass0 =assist (pin ,actorUuid )#line:596
            assistState0 =ass0 ['assistState']#line:597
            openAll0 =ass0 ['openCardInfo']['openAll']#line:598
            openVenderId0 =ass0 ['openCardInfo']['openVenderId']#line:599
            assStat =False #line:600
            if openAll0 :#line:601
                print ("已完成全部开卡任务")#line:602
                if assistState0 ==0 :#line:603
                    print ("无法助力自己~")#line:604
                elif assistState0 ==3 :#line:605
                    print ("已助力过其他好友~")#line:606
                elif assistState0 ==1 :#line:607
                    print ("已完成开卡关注任务,未助力过好友~")#line:608
                    assStat =True #line:609
                else :#line:610
                    assStat =True #line:612
            else :#line:613
                print ("现在去开卡")#line:614
                task_info0 =taskInfo (pin )#line:615
                openCardList =task_info0 ['1']['settingInfo']#line:616
                openCardLists =[(int (OOOO0O0O00OOO00OO ['value']),OOOO0O0O00OOO00OO ['name'])for OOOO0O0O00OOO00OO in openCardList ]#line:617
                unOpenCardLists =[OOOO000OO0O0OOO00 for OOOO000OO0O0OOO00 in openCardLists if OOOO000OO0O0OOO00 [0 ]not in openVenderId0 ]#line:618
                open_num =0 #line:619
                openExit =False #line:620
                for shop in unOpenCardLists :#line:621
                    open_num +=1 #line:622
                    print (f"去开卡 {open_num}/{len(unOpenCardLists)} {shop[0]}")#line:623
                    venderId =shop [0 ]#line:624
                    venderCardName =shop [1 ]#line:625
                    retry_time =0 #line:627
                    while True :#line:628
                        retry_time +=1 #line:629
                        open_result =bindWithVender (cookie ,venderId )#line:630
                        if open_result is not None :#line:631
                            if "火爆"in open_result [0 ]or "失败"in open_result [0 ]or "解绑"in open_result [0 ]:#line:632
                                print (f"\t⛈⛈{venderCardName} {open_result[0]}")#line:633
                                assStat =False #line:634
                                openExit =True #line:635
                            else :#line:636
                                print (f"\t🎉🎉{venderCardName} {open_result[0]}")#line:637
                                assStat =True #line:638
                            break #line:639
                        else :#line:640
                            time .sleep (0.5 )#line:641
                        if retry_time >=3 :#line:642
                            break #line:643
                    if openExit :#line:644
                        break #line:645
                    if open_num %5 ==0 :#line:646
                        print ("⏰等待3s,休息一下")#line:647
                        time .sleep (3 )#line:648
                    else :#line:649
                        time .sleep (1.5 )#line:650
            activityContent (pin ,yunMidImageUrl ,nickname )#line:652
            shareRecord (pin ,actorUuid )#line:653
            time .sleep (0.5 )#line:654
            taskRecord (pin ,actorUuid )#line:655
            time .sleep (0.5 )#line:656
            ass1 =assist (pin ,actorUuid )#line:657
            assistState1 =ass1 ['assistState']#line:658
            if assStat and assistState1 ==1 :#line:659
                print ("🎉🎉🎉助力成功~")#line:660
                if num !=1 :#line:661
                    inviteSuccNum +=1 #line:662
                    print (f"本次车头已邀请{inviteSuccNum}人")#line:663
            elif assStat and assistState0 ==1 :#line:664
                print ("🎉🎉🎉助力成功~")#line:665
                if num !=1 :#line:666
                    inviteSuccNum +=1 #line:667
                    print (f"本次车头已邀请{inviteSuccNum}人")#line:668
            if num ==1 :#line:670
                print (f"后面账号全部助力 {actorUuid}")#line:671
                shareUuid =actorUuid #line:672
                activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:673
        time .sleep (3 )