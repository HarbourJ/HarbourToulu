#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_opencardH1216.py(12.16-12.25 年终礼遇盛典)
Author: HarbourJ
Date: 2023/9/12 00:00
TG: https://t.me/HarbourToulu
cron: 0 0 */3 16-25 12 *
new Env('年终礼遇盛典');
ActivityEntry: https://lzdz1-isv.isvjcloud.com/m/unite/dzlh0001?activityId=9ff9cd2abad04f7eb3f06815f7f7fffc&venderId=1000097462&adSource=DLJDZYQJD
并发变量：export jd_joinCommon_uuid="你的uuid"
并发命令：task HarbourJ_HarbourToulu_main/jd_opencardH1216.py conc JD_COOKIE 1-20
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
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:22
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:23
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:24
inviterUuid =os .environ .get ("jd_joinCommon_uuid")if os .environ .get ("jd_joinCommon_uuid")else ""#line:25
activityId ="9ff9cd2abad04f7eb3f06815f7f7fffc"#line:27
shopId ="1000003829"#line:28
activity_url =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={inviterUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:29
print (f"【🛳活动入口】https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}")#line:30
def redis_conn ():#line:32
    try :#line:33
        import redis #line:34
        try :#line:35
            O000OOOOO00OOO0O0 =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:36
            OOOOOO0OO0OO0O00O =redis .Redis (connection_pool =O000OOOOO00OOO0O0 )#line:37
            OOOOOO0OO0OO0O00O .get ('conn_test')#line:38
            print ('✅redis连接成功')#line:39
            return OOOOOO0OO0OO0O00O #line:40
        except :#line:41
            print ("⚠️redis连接异常")#line:42
    except :#line:43
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:44
        sys .exit ()#line:45
def getToken (OOOOOOO0O000OOOOO ,r =None ):#line:47
    OOOO00000OO0OO0O0 =f'{activityUrl.split("com/")[0]}com'#line:48
    try :#line:49
        OO00OO0OO00OOOO00 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OOOOOOO0O000OOOOO )[0 ])#line:50
    except :#line:51
        OO00OO0OO00OOOO00 =OOOOOOO0O000OOOOO [:15 ]#line:52
    try :#line:53
        try :#line:54
            O0OO0OO0OOOO0O0O0 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO00OO0OO00OOOO00}')#line:55
        except Exception as O0O000OO0OO0O0OO0 :#line:56
            O0OO0OO0OOOO0O0O0 =None #line:58
        if O0OO0OO0OOOO0O0O0 is not None :#line:59
            print (f"♻️获取缓存Token")#line:60
            return O0OO0OO0OOOO0O0O0 #line:61
        else :#line:62
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OOOOOOO0O000OOOOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:73
            sign ({"url":f"{OOOO00000OO0OO0O0}","id":""},'isvObfuscator')#line:74
            O0O0O00OOO0000OO0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:75
            if O0O0O00OOO0000OO0 .status_code !=200 :#line:76
                print (O0O0O00OOO0000OO0 .status_code )#line:77
                return #line:78
            else :#line:79
                if "参数异常"in O0O0O00OOO0000OO0 .text :#line:80
                    print (O0O0O00OOO0000OO0 .text )#line:81
                    return #line:82
            OOOOO0O0000OO000O =O0O0O00OOO0000OO0 .json ()['token']#line:83
            try :#line:84
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO00OO0OO00OOOO00}',OOOOO0O0000OO000O ,ex =1800 ):#line:85
                    print ("✅Token缓存成功")#line:86
                else :#line:87
                    print ("❌Token缓存失败")#line:88
            except Exception as O0O000OO0OO0O0OO0 :#line:89
                print (f"✅获取实时Token")#line:91
            return OOOOO0O0000OO000O #line:92
    except Exception as O0O000OO0OO0O0OO0 :#line:93
        print (f"Get Token Error: {str(O0O000OO0OO0O0OO0)}")#line:94
        return #line:95
def getJdTime ():#line:97
    OO00OOOO0OO0O0O0O =int (round (time .time ()*1000 ))#line:98
    return OO00OOOO0OO0O0O0O #line:99
def randomString (OO000OO0OOOO0O0O0 ,flag =False ):#line:101
    OO0OO00000OOOO000 ="0123456789abcdef"#line:102
    if flag :OO0OO00000OOOO000 =OO0OO00000OOOO000 .upper ()#line:103
    OO0000OOO0OOO0O00 =[random .choice (OO0OO00000OOOO000 )for _O000OO0OO0OO0OO0O in range (OO000OO0OOOO0O0O0 )]#line:104
    return ''.join (OO0000OOO0OOO0O00 )#line:105
def refresh_cookies (O0OOO0OOO0O0O0O0O ):#line:107
    if O0OOO0OOO0O0O0O0O .cookies :#line:108
        O000O0000000O000O =O0OOO0OOO0O0O0O0O .cookies .get_dict ()#line:109
        OOOOOOOOOOOOO0O0O =[(O0O00OOO0O00000O0 +"="+O000O0000000O000O [O0O00OOO0O00000O0 ])for O0O00OOO0O00000O0 in O000O0000000O000O ]#line:110
        global activityCookie #line:111
        O0O00OOO0000O0OOO =[O00O000O0O00O000O for O00O000O0O00O000O in activityCookie .split (';')if O00O000O0O00O000O !='']#line:112
        for OOO0O000OOO0000O0 in O0O00OOO0000O0OOO :#line:113
            for OOO00O00OOOO0O00O in OOOOOOOOOOOOO0O0O :#line:114
                if OOO0O000OOO0000O0 .split ('=')[0 ]==OOO00O00OOOO0O00O .split ('=')[0 ]:#line:115
                    if OOO0O000OOO0000O0 .split ('=')[1 ]!=OOO00O00OOOO0O00O .split ('=')[1 ]:#line:116
                        O0O00OOO0000O0OOO .remove (OOO0O000OOO0000O0 )#line:117
        activityCookie =''.join (sorted ([(O00OO0O00O0O0OOOO +";")for O00OO0O00O0O0OOOO in list (set (O0O00OOO0000O0OOO +OOOOOOOOOOOOO0O0O ))]))#line:118
def getActivity ():#line:120
    O00OO0OO0OO0OO0OO =activityUrl #line:121
    O000000OO000OOOOO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:129
    O0OOO0OO000OO00OO =requests .request ("GET",O00OO0OO0OO0OO0OO ,headers =O000000OO000OOOOO )#line:131
    if O0OOO0OO000OO00OO .status_code ==200 :#line:132
        if O0OOO0OO000OO00OO .cookies :#line:133
            OO0OOO0O0O000O000 =O0OOO0OO000OO00OO .cookies .get_dict ()#line:134
            O0OO0OO000O0OOO0O =[(O0O00O00OOOO0OO00 +"="+OO0OOO0O0O000O000 [O0O00O00OOOO0OO00 ])for O0O00O00OOOO0OO00 in OO0OOO0O0O000O000 ]#line:135
            O0OOOO0OO000O0OO0 =''.join (sorted ([(O00O0OO0OOO000O0O +";")for O00O0OO0OOO000O0O in O0OO0OO000O0OOO0O ]))#line:136
        return O0OOOO0OO000O0OO0 #line:137
    else :#line:138
        print (O0OOO0OO000OO00OO .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:139
        sys .exit ()#line:140
def getSystemConfigForNew ():#line:142
    O0O00OO00O0OOOO00 ="https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:143
    O00O00OOOO0O00O00 =f'activityId={activityId}&activityType=99'#line:144
    O0OOO0O0O0O000O00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:157
    O0O0O0O0O0OOO0O0O =requests .request ("POST",O0O00OO00O0OOOO00 ,headers =O0OOO0O0O0O000O00 ,data =O00O00OOOO0O00O00 )#line:158
    refresh_cookies (O0O0O0O0O0OOO0O0O )#line:159
def getSimpleActInfoVo ():#line:161
    O0O00OO0O00O00000 ="https://lzdz1-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"#line:162
    OOOO0OOO0000O00O0 =f"activityId={activityId}"#line:163
    OOOO0O0000OO0OOO0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:176
    O00O0OOOO0O0OOO0O =requests .request ("POST",O0O00OO0O00O00000 ,headers =OOOO0O0000OO0OOO0 ,data =OOOO0OOO0000O00O0 )#line:177
    refresh_cookies (O00O0OOOO0O0OOO0O )#line:178
    OOO00000OOO0O0O00 =O00O0OOOO0O0OOO0O .json ()#line:179
    if OOO00000OOO0O0O00 ['result']:#line:180
        return OOO00000OOO0O0O00 ['data']#line:181
    else :#line:182
        print (OOO00000OOO0O0O00 ['errorMessage'])#line:183
def getMyPing (O0000OO0O000O0O00 ,OO0OOOO0OOOO0O00O ):#line:185
    O00000O0O0O0O0000 ="https://lzdz1-isv.isvjcloud.com/customer/getMyPing"#line:186
    OO00OOO0OO0O000O0 =f"userId={OO0OOOO0OOOO0O00O}&token={token}&fromType=APP"#line:187
    O0000OO00000OOO0O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:200
    OO0OOO0000O0O0OOO =requests .request ("POST",O00000O0O0O0O0000 ,headers =O0000OO00000OOO0O ,data =OO00OOO0OO0O000O0 )#line:201
    refresh_cookies (OO0OOO0000O0O0OOO )#line:202
    OOOO00O0OOOO0OO0O =OO0OOO0000O0O0OOO .json ()#line:203
    if OOOO00O0OOOO0OO0O ['result']:#line:204
        return OOOO00O0OOOO0OO0O ['data']['nickname'],OOOO00O0OOOO0OO0O ['data']['secretPin']#line:205
    else :#line:206
        print (f"⚠️{OOOO00O0OOOO0OO0O['errorMessage']}")#line:207
        if O0000OO0O000O0O00 ==1 and "火爆"in OOOO00O0OOOO0OO0O ['errorMessage']:#line:208
            print (f"\t⛈车头黑,退出本程序！")#line:209
            sys .exit ()#line:210
def accessLogWithAD (OO0OOOOOO0OOO0O00 ,OOOOOO0OOO0O00O0O ):#line:212
    O000O00000000O0OO ="https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"#line:213
    OO0O0O00O00O0OO0O =f"venderId={OO0OOOOOO0OOO0O00}&code=99&pin={quote_plus(OOOOOO0OOO0O00O0O)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource=null"#line:214
    O000OOO00000OO000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:227
    OO00O00OOOO0000O0 =requests .request ("POST",O000O00000000O0OO ,headers =O000OOO00000OO000 ,data =OO0O0O00O00O0OO0O )#line:228
    refresh_cookies (OO00O00OOOO0000O0 )#line:229
def getSystime ():#line:231
    O00O0OO0O00000O0O ="https://lzdz1-isv.isvjcloud.com/common/getSystime"#line:232
    OO0000O0OOO00OO0O ={'Host':'lzdz1-isv.isvjcloud.com','Origin':'https://lzdz1-isv.isvjcloud.com','Accept-Encoding':'gzip, deflate, br','Cookie':activityCookie ,'Content-Length':'0','Connection':'keep-alive','Accept':'application/json','User-Agent':ua ,'Referer':activityUrl ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','X-Requested-With':'XMLHttpRequest'}#line:245
    OOOO00O0OO0OO0OOO =requests .request ("POST",O00O0OO0O00000O0O ,headers =OO0000O0OOO00OO0O )#line:246
    refresh_cookies (OOOO00O0OO0OO0OOO )#line:247
def getUserInfo (O0O00O0O0OOO0O0OO ):#line:249
    OO000O000OO00OOO0 ="https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo"#line:250
    OOO0O000OOOOO00OO =f"pin={quote_plus(O0O00O0O0OOO0O0OO)}"#line:251
    OO0OOOO00O00O00OO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:264
    O0000OOOOOOOOO00O =requests .request ("POST",OO000O000OO00OOO0 ,headers =OO0OOOO00O00O00OO ,data =OOO0O000OOOOO00OO )#line:265
    refresh_cookies (O0000OOOOOOOOO00O )#line:266
    OO0OOO0O0000OOO00 =O0000OOOOOOOOO00O .json ()#line:267
    if OO0OOO0O0000OOO00 ['result']:#line:268
        return OO0OOO0O0000OOO00 ['data']['nickname'],OO0OOO0O0000OOO00 ['data']['yunMidImageUrl'],OO0OOO0O0000OOO00 ['data']['pin']#line:269
    else :#line:270
        print (OO0OOO0O0000OOO00 ['errorMessage'])#line:271
def activityContent (O00OOOO000O000O00 ,OOO0OOOO00000OO0O ,O00OO0O000000OOO0 ):#line:273
    O0OOOOO0OOOOOOOOO ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activityContent"#line:274
    try :#line:275
        O0OOO000O00OOO0O0 =quote_plus (OOO0OOOO00000OO0O )#line:276
    except :#line:277
        O0OOO000O00OOO0O0 =quote_plus ("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")#line:278
    OOO00O000O00O0000 =f"activityId={activityId}&pin={quote_plus(O00OOOO000O000O00)}&pinImg={O0OOO000O00OOO0O0}&nick={quote_plus(O00OO0O000000OOO0)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}"#line:279
    OO00O0O0O0OO0OO0O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:292
    O000O00O0000O0OO0 =requests .request ("POST",O0OOOOO0OOOOOOOOO ,headers =OO00O0O0O0OO0OO0O ,data =OOO00O000O00O0000 )#line:293
    refresh_cookies (O000O00O0000O0OO0 )#line:294
    O000000OO00O0OO00 =O000O00O0000O0OO0 .json ()#line:295
    if O000000OO00O0OO00 ['result']:#line:296
        return O000000OO00O0OO00 ['data']#line:297
    else :#line:298
        print (O000000OO00O0OO00 ['errorMessage'])#line:299
        if "活动已结束"in O000000OO00O0OO00 ['errorMessage']:#line:300
            sys .exit ()#line:301
def shareRecord (OOOOOO0O00O000O00 ,O00OOOOO000O0OO00 ):#line:303
    O0O000OO000OOOOO0 ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/shareRecord"#line:304
    OO00OO000OOOO00O0 =f"activityId={activityId}&pin={quote_plus(OOOOOO0O00O000O00)}&uuid={O00OOOOO000O0OO00}&num=30"#line:305
    OO000OO000OOOOO0O ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:318
    OO0O0OOOOO000000O =requests .request ("POST",O0O000OO000OOOOO0 ,headers =OO000OO000OOOOO0O ,data =OO00OO000OOOO00O0 )#line:319
    refresh_cookies (OO0O0OOOOO000000O )#line:320
def taskRecord (OOOO0O0000OO00OO0 ,OO00O000OO0O00O0O ):#line:322
    O00OOOO00OOOOO000 ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/taskRecord"#line:323
    O00OO000O00OOO00O =f"activityId={activityId}&pin={quote_plus(OOOO0O0000OO00OO0)}&uuid={OO00O000OO0O00O0O}&taskType="#line:324
    OO0OOO0O0OOOO00O0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:337
    OO0OO0000OO00O00O =requests .request ("POST",O00OOOO00OOOOO000 ,headers =OO0OOO0O0OOOO00O0 ,data =O00OO000O00OOO00O )#line:338
    refresh_cookies (OO0OO0000OO00O00O )#line:339
def drawContent (OOO0O0000OO0O00O0 ,O0O0OO00O0O00O000 ):#line:341
    O00OO00OOO00OO0OO ="https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent"#line:342
    O00OO00OOOO00O0OO =f"activityId={OOO0O0000OO0O00O0}&pin={quote_plus(O0O0OO00O0O00O000)}"#line:343
    O00OOO0000O0O00O0 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:356
    requests .request ("POST",O00OO00OOO00OO0OO ,headers =O00OOO0000O0O00O0 ,data =O00OO00OOOO00O0OO )#line:357
def taskInfo (O00000O0O00000O0O ):#line:359
    OO00OOO00OOO0O0OO ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/taskInfo"#line:360
    OO00O00O0O0O00000 =f"activityId={activityId}&pin={quote_plus(O00000O0O00000O0O)}"#line:361
    OOOO0O0OOO0O00O00 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:374
    O00O0OO0OOOO00O00 =requests .request ("POST",OO00OOO00OOO0O0OO ,headers =OOOO0O0OOO0O00O00 ,data =OO00O00O0O0O00000 )#line:375
    OOO000O0OO000O0O0 =O00O0OO0OOOO00O00 .json ()#line:376
    if OOO000O0OO000O0O0 ['result']:#line:377
        return OOO000O0OO000O0O0 ['data']#line:378
    else :#line:379
        print (OOO000O0OO000O0O0 ['errorMessage'])#line:380
def assist (OO00OOOO0000O0000 ,O0O0OOOO0O000O0O0 ):#line:382
    OO000OO00OO0O0O0O ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/assist"#line:383
    OO0O000O00OOO00OO =f"activityId={activityId}&pin={quote_plus(OO00OOOO0000O0000)}&uuid={O0O0OOOO0O000O0O0}&shareUuid={shareUuid}"#line:384
    OOOOOO0O0O00OOOOO ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:397
    OO0000O0O0O00OO00 =requests .request ("POST",OO000OO00OO0O0O0O ,headers =OOOOOO0O0O00OOOOO ,data =OO0O000O00OOO00OO )#line:398
    OOOOOOO0OO000O0OO =OO0000O0O0O00OO00 .json ()#line:399
    if OOOOOOO0OO000O0OO ['result']:#line:400
        return OOOOOOO0OO000O0OO ['data']#line:401
    else :#line:402
        print (OOOOOOO0OO000O0OO ['errorMessage'])#line:403
def doTask (OOO0OOO0OOOO0O0OO ,OO0O000OOO00OO000 ,OO00O0OO0OOOO000O ):#line:405
    OOOO0OOO00O0OOO0O ="https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/doTask"#line:406
    OOOO0O000O000000O =f"activityId={activityId}&uuid={OOO0OOO0OOOO0O0OO}&pin={quote_plus(OO0O000OOO00OO000)}&taskType={OO00O0OO0OOOO000O}&taskValue="#line:407
    OOOO0O0O00O0OO000 ={'Host':'lzdz1-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzdz1-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:420
    OOOO000OOOO000O00 =requests .request ("POST",OOOO0OOO00O0OOO0O ,headers =OOOO0O0O00O0OO000 ,data =OOOO0O000O000000O )#line:421
    OO0O000O00O0O0OOO =OOOO000OOOO000O00 .json ()#line:422
    print ('doTask',OO0O000O00O0O0OOO )#line:423
    if OO0O000O00O0O0OOO ['result']:#line:424
        OO00OOOOO0000O0O0 =OO0O000O00O0O0OOO ['data']#line:425
        if OO00OOOOO0000O0O0 ['score']==0 :#line:426
            print ("\t获得 💨💨💨")#line:427
        else :#line:428
            print (f"\t🎉获得{OO00OOOOO0000O0O0['score']}积分")#line:429
    else :#line:430
        print (OO0O000O00O0O0OOO ['errorMessage'])#line:431
def bindWithVender (O000OO00OO0OO0O0O ,O0OOOOOO0O0O00OOO ):#line:433
    try :#line:434
        OOOOO0O0O00OO0000 ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':O0OOOOOO0O0O00OOO ,'shopId':O0OOOOOO0O0O00OOO ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:443
        O0O0O0OO0OOOOO000 ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':'https://shop.m.jd.com/','User-Agent':ua ,'Cookie':O000OO00OO0OO0O0O }#line:456
        O0O0OO0O0OOO00O0O =requests .request ("POST","https://api.m.jd.com/",headers =O0O0O0OO0OOOOO000 ,data =OOOOO0O0O00OO0000 ,timeout =10 ).text #line:457
        O0000OOOO0OOOOOO0 =json .loads (O0O0OO0O0OOO00O0O )#line:458
        if O0000OOOO0OOOOOO0 ['success']:#line:459
            return O0000OOOO0OOOOOO0 ['message'],O0000OOOO0OOOOOO0 ['result']['giftInfo']if O0000OOOO0OOOOOO0 ['result']else ""#line:460
    except Exception as O00OO0OO00OO0O00O :#line:461
        print (f"bindWithVender Error: {O0OOOOOO0O0O00OOO} {O00OO0OO00OO0O00O}")#line:462
def getShopOpenCardInfo (OOO0O000OOO0O00O0 ,O0O0OOO000000O00O ):#line:464
    try :#line:465
        OOOOO0OO0OO000000 ={"venderId":str (O0O0OOO000000O00O ),"channel":"401"}#line:466
        OOO00O0O0O000O0O0 =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OOOOO0OO0OO000000)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:467
        OO0OOO00O0OOOO0OO ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OOO0O000OOO0O00O0 ,'User-Agent':ua ,'Accept-Language':'zh-cn','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate'}#line:477
        OOOOOOO0OO0O00O0O =requests .get (url =OOO00O0O0O000O0O0 ,headers =OO0OOO00O0OOOO0OO ,timeout =5 ).text #line:478
        OO0O0O00OOOOOOO00 =json .loads (OOOOOOO0OO0O00O0O )#line:479
        if OO0O0O00OOOOOOO00 ['success']:#line:480
            OO00OO000OOO00OOO =OO0O0O00OOOOOOO00 ['result']['shopMemberCardInfo']['venderCardName']#line:481
            return OO00OO000OOO00OOO #line:482
        else :#line:483
            return O0O0OOO000000O00O #line:484
    except :#line:485
        return O0O0OOO000000O00O #line:486
if __name__ =='__main__':#line:489
    r =redis_conn ()#line:490
    try :#line:491
        cks =getCk #line:492
        if not cks :#line:493
            sys .exit ()#line:494
    except :#line:495
        print ("未获取到有效COOKIE,退出程序！")#line:496
        sys .exit ()#line:497
    global shareUuid ,inviteSuccNum ,activityUrl ,firstCk #line:498
    inviteSuccNum =0 #line:499
    if len (cks )==1 :#line:500
        shareUuid =inviterUuid #line:501
        activityUrl =activity_url #line:502
    else :#line:503
        shareUuid =remote_redis (f"lzdz1_{activityId}",2 )#line:504
        activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:505
    num =0 #line:506
    for cookie in cks :#line:507
        num +=1 #line:508
        if num ==1 :#line:509
            firstCk =cookie #line:510
        if num %8 ==0 :#line:511
            print ("⏰等待10s,休息一下")#line:512
            time .sleep (10 )#line:513
        global ua ,activityCookie ,token #line:514
        ua =userAgent ()#line:515
        try :#line:516
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:517
            pt_pin =unquote_plus (pt_pin )#line:518
        except IndexError :#line:519
            pt_pin =re .compile (r'pin=(.*?);').findall (cookie )[0 ]#line:520
            pt_pin =unquote_plus (pt_pin )#line:521
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:522
        print (datetime .now ())#line:523
        token =getToken (cookie ,r )#line:525
        if token is None :#line:526
            if num ==1 :#line:527
                print (f"⚠️车头获取Token失败,退出本程序！")#line:528
                sys .exit ()#line:529
            print (f"⚠️获取Token失败！⏰等待3s")#line:530
            time .sleep (3 )#line:531
            continue #line:532
        time .sleep (0.5 )#line:533
        activityCookie =getActivity ()#line:534
        time .sleep (0.5 )#line:535
        getSystemConfigForNew ()#line:536
        time .sleep (0.3 )#line:537
        getSimAct =getSimpleActInfoVo ()#line:538
        if getSimAct :#line:539
            venderId =getSimAct ['venderId']#line:540
        else :#line:541
            venderId =shopId #line:542
        time .sleep (0.2 )#line:543
        getPin =getMyPing (num ,venderId )#line:544
        if getPin is not None :#line:545
            nickname =getPin [0 ]#line:546
            secretPin =getPin [1 ]#line:547
            time .sleep (0.5 )#line:548
            accessLogWithAD (venderId ,secretPin )#line:549
            time .sleep (0.5 )#line:550
            userInfo =getUserInfo (secretPin )#line:551
            time .sleep (0.8 )#line:552
            nickname =userInfo [0 ]#line:553
            yunMidImageUrl =userInfo [1 ]#line:554
            pin =userInfo [2 ]#line:555
            actContent =activityContent (pin ,yunMidImageUrl ,nickname )#line:556
            if not actContent :#line:557
                if num ==1 :#line:558
                    print ("⚠️无法获取车头邀请码,退出本程序！")#line:559
                    sys .exit ()#line:560
                continue #line:561
            hasEnd =actContent ['hasEnd']#line:562
            if hasEnd :#line:563
                print ("活动已结束，下次早点来~")#line:564
                sys .exit ()#line:565
            print (f"✅开启【{actContent['activityName']}】活动\n")#line:566
            if num ==1 :#line:567
                print (f"🛳 已邀请{actContent['actorInfo']['totalAssistCount']}, 有效助力{actContent['actorInfo']['assistCount']}")#line:568
            actorUuid =actContent ['actorInfo']['uuid']#line:569
            taskType =actContent ['taskType']#line:570
            print (f"邀请码->: {actorUuid}")#line:571
            print (f"准备助力->: {shareUuid}")#line:572
            time .sleep (0.5 )#line:573
            shareRecord (pin ,actorUuid )#line:574
            time .sleep (0.5 )#line:575
            taskRecord (pin ,actorUuid )#line:576
            time .sleep (0.5 )#line:577
            print ("现在去一键关注店铺")#line:578
            doTask (actorUuid ,pin ,20 )#line:579
            time .sleep (1 )#line:580
            doTask (actorUuid ,pin ,23 )#line:581
            time .sleep (1 )#line:582
            ass0 =assist (pin ,actorUuid )#line:583
            assistState0 =ass0 ['assistState']#line:584
            openAll0 =ass0 ['openCardInfo']['openAll']#line:585
            openVenderId0 =ass0 ['openCardInfo']['openVenderId']#line:586
            assStat =False #line:587
            if openAll0 :#line:588
                print ("已完成全部开卡任务")#line:589
                if assistState0 ==0 :#line:590
                    print ("无法助力自己~")#line:591
                elif assistState0 ==3 :#line:592
                    print ("已助力过其他好友~")#line:593
                elif assistState0 ==1 :#line:594
                    print ("已完成开卡关注任务,未助力过好友~")#line:595
                    assStat =True #line:596
                else :#line:597
                    assStat =True #line:599
            else :#line:600
                print ("现在去开卡")#line:601
                task_info0 =taskInfo (pin )#line:602
                openCardList =task_info0 ['1']['settingInfo']#line:603
                openCardLists =[(int (OOO000O0O0OOO0O00 ['value']),OOO000O0O0OOO0O00 ['name'])for OOO000O0O0OOO0O00 in openCardList ]#line:604
                unOpenCardLists =[OOO00O0OO0O0O000O for OOO00O0OO0O0O000O in openCardLists if OOO00O0OO0O0O000O [0 ]not in openVenderId0 ]#line:605
                open_num =0 #line:606
                openExit =False #line:607
                for shop in unOpenCardLists :#line:608
                    open_num +=1 #line:609
                    print (f"去开卡 {open_num}/{len(unOpenCardLists)} {shop[0]}")#line:610
                    venderId =shop [0 ]#line:611
                    venderCardName =shop [1 ]#line:612
                    retry_time =0 #line:614
                    while True :#line:615
                        retry_time +=1 #line:616
                        open_result =bindWithVender (cookie ,venderId )#line:617
                        if open_result is not None :#line:618
                            if "火爆"in open_result [0 ]or "失败"in open_result [0 ]or "解绑"in open_result [0 ]:#line:619
                                print (f"\t⛈⛈{venderCardName} {open_result[0]}")#line:620
                                assStat =False #line:621
                                openExit =True #line:622
                            else :#line:623
                                print (f"\t🎉🎉{venderCardName} {open_result[0]}")#line:624
                                assStat =True #line:625
                            break #line:626
                        else :#line:627
                            time .sleep (0.5 )#line:628
                        if retry_time >=3 :#line:629
                            break #line:630
                    if openExit :#line:631
                        break #line:632
                    if open_num %5 ==0 :#line:633
                        print ("⏰等待3s,休息一下")#line:634
                        time .sleep (3 )#line:635
                    else :#line:636
                        time .sleep (1.5 )#line:637
            activityContent (pin ,yunMidImageUrl ,nickname )#line:639
            shareRecord (pin ,actorUuid )#line:640
            time .sleep (0.5 )#line:641
            taskRecord (pin ,actorUuid )#line:642
            time .sleep (0.5 )#line:643
            ass1 =assist (pin ,actorUuid )#line:644
            assistState1 =ass1 ['assistState']#line:645
            if assStat and assistState1 ==1 :#line:646
                print ("🎉🎉🎉助力成功~")#line:647
                if num !=1 :#line:648
                    inviteSuccNum +=1 #line:649
                    print (f"本次车头已邀请{inviteSuccNum}人")#line:650
            elif assStat and assistState0 ==1 :#line:651
                print ("🎉🎉🎉助力成功~")#line:652
                if num !=1 :#line:653
                    inviteSuccNum +=1 #line:654
                    print (f"本次车头已邀请{inviteSuccNum}人")#line:655
            if num ==1 :#line:657
                print (f"后面账号全部助力 {actorUuid}")#line:658
                shareUuid =actorUuid #line:659
                activityUrl =f"https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity/5929859?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid={shopId}"#line:660
        time .sleep (3 )