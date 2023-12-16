#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_jinggengInvite.py(jinggeng邀请入会有礼)
Author: HarbourJ
Date: 2022/8/1 22:37
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('jinggeng邀请入会有礼');
活动入口: https://jinggeng-isv.isvjcloud.com/ql/front/showInviteJoin?id=9e80809282a4bdc90182ab254c7e0a12&user_id=1000121005
变量设置: export redis_url="xxx", export redis_port="xxx"(没有可省略), export redis_pwd="xxx"(没有可省略)
        export jinggengInviteJoin="9e80809282a4bdc90182ab254c7e0a12&1000121005"(活动id&店铺id)
Update: 2022/11/01 更新入会算法，内置船新入会本地算法
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from bs4 import BeautifulSoup #line:2
from datetime import datetime #line:3
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
jinggengInviteJoin =os .environ .get ("jinggengInviteJoin")if os .environ .get ("jinggengInviteJoin")else ""#line:25
inviterNicks =["Ny0m1K1tVHIJvt0j4SQ9RbRPXMHHf%2BDrNmMVfT8S5hq3SjYMAACrbEHZQ40J5yPY","pWGUWZJQ3actex0X2vQyLsjNhNaYFy2HteErE6izlhTf9nrGY7gBkCdGU4C6z%2FxD","3TQTImsIN0s9T85f1wS70V4tLNYA4seuA67MOIYQxEk3Vl9%2BAVo4NF%2BtgyeIc6A6kdK3rLBQpEQH9V4tdrrh0w%3D%3D"]#line:31
if "&"not in jinggengInviteJoin :#line:32
    print ("⚠️jinggengInviteJoin变量有误！退出程序！")#line:33
    sys .exit ()#line:34
ac_id =jinggengInviteJoin .split ("&")[0 ]#line:35
user_id =jinggengInviteJoin .split ("&")[1 ]#line:36
inviterNick =random .choice (inviterNicks )#line:37
activity_url =f"https://jinggeng-isv.isvjcloud.com/ql/front/showInviteJoin?id={ac_id}&user_id={user_id}&inviterNick={inviterNick}"#line:38
print (f"【🛳活动入口】https://jinggeng-isv.isvjcloud.com/ql/front/showInviteJoin?id={ac_id}&user_id={user_id}")#line:39
def redis_conn ():#line:41
    try :#line:42
        import redis #line:43
        try :#line:44
            OO000000O0OO00O00 =redis .ConnectionPool (host =redis_url ,port =redis_port ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:45
            OO0OOOO0OO0000000 =redis .Redis (connection_pool =OO000000O0OO00O00 )#line:46
            OO0OOOO0OO0000000 .get ('conn_test')#line:47
            print ('✅redis连接成功')#line:48
            return OO0OOOO0OO0000000 #line:49
        except :#line:50
            print ("⚠️redis连接异常")#line:51
    except :#line:52
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:53
def getToken (O0O0OOO0OO0OO0OO0 ,r =None ):#line:55
    try :#line:56
        OO000000000000000 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (O0O0OOO0OO0OO0OO0 )[0 ])#line:58
    except :#line:59
        OO000000000000000 =O0O0OOO0OO0OO0OO0 [:15 ]#line:61
    try :#line:62
        if r is not None :#line:63
            OOOOOOO0OO00O000O =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO000000000000000}')#line:64
            if OOOOOOO0OO00O000O is not None :#line:66
                print (f"♻️获取缓存Token")#line:67
                return OOOOOOO0OO00O000O #line:68
            else :#line:69
                s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0OOO0OO0OO0OO0 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:80
                O0O00000O0OOOO0OO =sign ({"url":f"{activityUrl}","id":""},'isvObfuscator')#line:81
                O00O0OO00OO0OO0O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:83
                if O00O0OO00OO0OO0O0 .status_code !=200 :#line:84
                    print (O00O0OO00OO0OO0O0 .status_code )#line:85
                    return #line:86
                else :#line:87
                    if "参数异常"in O00O0OO00OO0OO0O0 .text :#line:88
                        return #line:89
                O0O00O0O0O0O00OO0 =O00O0OO00OO0OO0O0 .json ()['token']#line:90
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{OO000000000000000}',O0O00O0O0O0O00OO0 ,ex =1800 ):#line:91
                    print ("✅Token缓存成功")#line:92
                else :#line:93
                    print ("❌Token缓存失败")#line:94
                return O0O00O0O0O0O00OO0 #line:95
        else :#line:96
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':O0O0OOO0OO0OO0OO0 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:107
            O0O00000O0OOOO0OO =sign ({"url":f"{activityUrl}","id":""},'isvObfuscator')#line:108
            O00O0OO00OO0OO0O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:110
            if O00O0OO00OO0OO0O0 .status_code !=200 :#line:111
                print (O00O0OO00OO0OO0O0 .status_code )#line:112
                return #line:113
            else :#line:114
                if "参数异常"in O00O0OO00OO0OO0O0 .text :#line:115
                    return #line:116
            OOOOOOO0OO00O000O =O00O0OO00OO0OO0O0 .json ()['token']#line:117
            print (f"✅获取实时Token")#line:118
            return OOOOOOO0OO00O000O #line:119
    except :#line:120
        return #line:121
def getJdTime ():#line:123
    OOO0OO0OO00OOOOO0 ="http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5"#line:124
    OOOO00OO000000OO0 ={'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9','Host':'api.m.jd.com','Proxy-Connection':'keep-alive','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}#line:133
    try :#line:134
        O0O0O0O0OOOO000O0 =requests .request ("GET",OOO0OO0OO00OOOOO0 ,headers =OOOO00OO000000OO0 ,timeout =2 )#line:135
        if O0O0O0O0OOOO000O0 .status_code ==200 :#line:136
            O0OOOO00OO0OO0000 =O0O0O0O0OOOO000O0 .json ()#line:137
            OOOO000O00O0000OO =O0OOOO00OO0OO0000 ['currentTime2']#line:138
    except :#line:139
        OOOO000O00O0000OO =int (round (time .time ()*1000 ))#line:140
    return OOOO000O00O0000OO #line:141
def randomString (O00O0OOOO00O0OO00 ,flag =False ):#line:143
    O000OO000O00OO0O0 ="0123456789abcdef"#line:144
    if flag :O000OO000O00OO0O0 =O000OO000O00OO0O0 .upper ()#line:145
    OO00O00O0OOOOO0OO =[random .choice (O000OO000O00OO0O0 )for _OO0OO0000OO0O0O0O in range (O00O0OOOO00O0OO00 )]#line:146
    return ''.join (OO00O00O0OOOOO0OO )#line:147
def refresh_cookies (O0OOO00OOOOO0O000 ):#line:149
    if O0OOO00OOOOO0O000 .cookies :#line:150
        OOO00O0OO00O000OO =O0OOO00OOOOO0O000 .cookies .get_dict ()#line:151
        O0O0O00O000OO00OO =[(O0O0O00O0OOO000OO +"="+OOO00O0OO00O000OO [O0O0O00O0OOO000OO ])for O0O0O00O0OOO000OO in OOO00O0OO00O000OO ]#line:152
        global activityCookie #line:153
        O00000O000O000000 =[OOOOO00OOO0OOOOO0 for OOOOO00OOO0OOOOO0 in activityCookie .split (';')if OOOOO00OOO0OOOOO0 !='']#line:154
        for O00O00OO0OO0OOO0O in O00000O000O000000 :#line:155
            for O0OO000OOOO000O00 in O0O0O00O000OO00OO :#line:156
                if O00O00OO0OO0OOO0O .split ('=')[0 ]==O0OO000OOOO000O00 .split ('=')[0 ]:#line:157
                    if O00O00OO0OO0OOO0O .split ('=')[1 ]!=O0OO000OOOO000O00 .split ('=')[1 ]:#line:158
                        O00000O000O000000 .remove (O00O00OO0OO0OOO0O )#line:159
        activityCookie =''.join (sorted ([(O0O0OOOOO0OOOOO0O +";")for O0O0OOOOO0OOOOO0O in list (set (O00000O000O000000 +O0O0O00O000OO00OO ))]))#line:160
def getActivity (index =1 ,isOpenCard =0 ,inviterCode =None ,getIndex =0 ):#line:162
    O00OO00O0OO0O0O0O =f"{activityUrl}&isOpenCard={isOpenCard}&from=kouling"#line:163
    if len (token )==0 :#line:164
        OOOO0O0OOO00OOOOO =''#line:165
    else :#line:166
        OOOO0O0OOO00OOOOO =f"IsvToken={token};"#line:167
    OOO0O0O0OO0O00OO0 ={'Host':'jinggeng-isv.isvjcloud.com','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Referer':O00OO00O0OO0O0O0O ,'Cookie':OOOO0O0OOO00OOOOO +activityCookie }#line:177
    O00O000O0OO0OOOOO =requests .request ("GET",O00OO00O0OO0O0O0O ,headers =OOO0O0O0OO0O00OO0 )#line:178
    OOOO0O0O00O000OOO =O00O000O0OO0OOOOO .text #line:179
    if O00O000O0OO0OOOOO .status_code ==493 :#line:180
        print (O00O000O0OO0OOOOO .status_code ,"⚠️ip疑似黑了,休息一会再来撸~")#line:181
        sys .exit ()#line:182
    OO00O000OOO0O00O0 =O00O000O0OO0OOOOO .cookies .get_dict ()#line:184
    OOO0OO0OOOO0OO000 =[(OO0O0OOO00OO00O0O +"="+OO00O000OOO0O00O0 [OO0O0OOO00OO00O0O ])for OO0O0OOO00OO00O0O in OO00O000OOO0O00O0 ]#line:185
    O00OO0O00OOOOOOOO =''.join (sorted ([(O00OOO0OO0O0OOOO0 +";")for O00OOO0OO0O0OOOO0 in OOO0OO0OOOO0OO000 ]))#line:186
    if getIndex ==3 :#line:187
        return O00OO0O00OOOOOOOO #line:188
    if "活动时间"in OOOO0O0O00O000OOO :#line:189
        refresh_cookies (O00O000O0OO0OOOOO )#line:190
        OOO000O00O000O0O0 =BeautifulSoup (OOOO0O0O00O000OOO ,'html.parser')#line:191
        O000OO0OOOOOOOOO0 =OOO000O00O000O0O0 .find ('input',attrs ={'id':'errorMsg'})['value']#line:192
        OO0OOO0O00O0OO0OO =OOO000O00O000O0O0 .find ('input',attrs ={'id':'inviteSucc'})['value']#line:193
        if len (O000OO0OOOOOOOOO0 )!=0 :#line:194
            O00O0OO0OOO00OOO0 =O000OO0OOOOOOOOO0 #line:195
        if len (OO0OOO0O00O0OO0OO )!=0 :#line:196
            O00O0OO0OOO00OOO0 =OO0OOO0O00O0OO0OO #line:197
        if index ==1 :#line:198
            if getIndex ==2 :#line:199
                pass #line:200
            OOOOOOO0000000OOO =OOO000O00O000O0O0 .find ('input',attrs ={'id':'shop_title'})['value'].replace (' ','')#line:201
            O0O00O00O000OOOO0 =OOO000O00O000O0O0 .find ('input',attrs ={'id':'actName'})['value']#line:202
            O00OO0O0O000O00O0 =OOO000O00O000O0O0 .find ('input',attrs ={'id':'shop_sid'})['value']#line:203
            OO0O0O0000O0000O0 =(OOO000O00O000O0O0 .find ('input',attrs ={'id':'helpLogs'})['value'])#line:204
            O00OOOO0OOOO0OO0O =eval (OOO000O00O000O0O0 .find ('input',attrs ={'id':'inviteSetting2'})['value'])#line:205
            print (f"店铺名称: {OOOOOOO0000000OOO} \n活动名称: {O0O00O00O000OOOO0} \n店铺ID: {O00OO0O0O000O00O0}")#line:206
            OOOO0000O0O000OOO ={'1':'one','2':'two','3':'three','4':'four'}#line:207
            OOO0O0OO000O00OOO ={'1':'leveOneNum','2':'leveTwoNum','3':'leveThreeNum','4':'leveFourNum'}#line:208
            O0OOO0O000O00O00O =[]#line:209
            for O0O00OO0000O00O0O in range (len (O00OOOO0OOOO0OO0O )):#line:210
                OO0O0OO000000OO0O =O0O00OO0000O00O0O +1 #line:211
                OOO00OO00O0O0OO0O =O00OOOO0OOOO0OO0O [OOOO0000O0O000OOO [str (OO0O0OO000000OO0O )]]#line:212
                OO000000OOO00OOOO =OOO00OO00O0O0OO0O ['freezeQuantity']#line:214
                O0OOOOO0O00OOO0OO =OOO00OO00O0O0OO0O ['availableQuantity']#line:215
                O0O00OOO000OO0O0O =OOO00OO00O0O0OO0O ['equityType']#line:216
                OO0OOOOOOOOO0O0OO =OOO00OO00O0O0OO0O ['equityName']#line:217
                O00O000OO00O0O0O0 =OOO00OO00O0O0OO0O [OOO0O0OO000O00OOO [str (OO0O0OO000000OO0O )]]#line:218
                if O0O00OOO000OO0O0O =="JD_GOODS":#line:219
                    OOOOOOO0O0O00O0OO =''#line:220
                else :#line:221
                    OOOOOOO0O0O00O0OO =OOO00OO00O0O0OO0O ['denomination']#line:222
                OO0O00O0O0OOOO000 =OOO00OO00O0O0OO0O ['id']#line:223
                print (f"奖品{OO0O0OO000000OO0O}: {OO0OOOOOOOOO0O0OO} 奖励: {OOOOOOO0O0O00O0OO} 总数: {OO000000OOO00OOOO}份 剩余: {O0OOOOO0O00OOO0OO}份 需要邀请: {O00O000OO00O0O0O0}人")#line:225
                if O0OOOOO0O00OOO0OO >0 :#line:226
                    O0OOO0O000O00O00O .append ((O00O000OO00O0O0O0 ,OO0O00O0O0OOOO000 ,O0O00OOO000OO0O0O ))#line:227
                if len (O0OOO0O000O00O00O )==0 :#line:228
                    print (f"⛈⛈⛈活动奖品全部发完啦！")#line:229
                    sys .exit ()#line:230
            return O000OO0OOOOOOOOO0 ,OO0O0O0000O0000O0 ,O0OOO0O000O00O00O #line:231
        return O00O0OO0OOO00OOO0 #line:232
    elif "活动已结束"in OOOO0O0O00O000OOO :#line:233
        print ("😭活动已结束,下次早点来~")#line:234
        sys .exit ()#line:235
    else :#line:236
        return O00OO0O00OOOOOOOO #line:237
def setMixNick (OOO0000OO0OO0OO0O ):#line:239
    O0OO00O0OOOOOOO0O ="https://jinggeng-isv.isvjcloud.com/front/setMixNick"#line:240
    O0O000OO000OOOOOO =f"strTMMixNick={OOO0000OO0OO0OO0O}&userId={user_id}&source=01"#line:241
    OO0OO00000O0O0000 ={'Host':'jinggeng-isv.isvjcloud.com','Accept':'application/json, text/javascript, */*; q=0.01','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'https://jinggeng-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':f'{activityUrl}&isOpenCard=0&from=kouling','Content-Length':'116','Cookie':activityCookie }#line:255
    try :#line:256
        O0OOO0OO0OOO00000 =requests .request ("POST",O0OO00O0OOOOOOO0O ,headers =OO0OO00000O0O0000 ,data =O0O000OO000OOOOOO )#line:257
        OO00O00000O0OOOO0 =O0OOO0OO0OOO00000 .text #line:258
        O0O0OO0O0OO00000O =eval (OO00O00000O0OOOO0 .replace ('true','True').replace ('false','False').replace ('none','None'))['msg']#line:259
        refresh_cookies (O0OOO0OO0OOO00000 )#line:260
        return O0O0OO0O0OO00000O #line:261
    except Exception as O0O00000O000OOO0O :#line:262
        print (O0O00000O000OOO0O )#line:263
        return #line:264
def recordActPvUvdata (OOOOOOOOO0O00OOO0 ):#line:266
    O00OO00OO0O000000 ="https://jinggeng-isv.isvjcloud.com/ql/front/reportActivity/recordActPvUvData"#line:267
    OO000O0OOO0O00000 =F"userId={user_id}&actId={ac_id}"#line:268
    OOO0OOOOO000OOO00 ={'Host':'jinggeng-isv.isvjcloud.com','Accept':'application/json, text/javascript, */*; q=0.01','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'https://jinggeng-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':f'{activityUrl}&isOpenCard=0&from=kouling','Content-Length':'56','Cookie':f"IsvToken={OOOOOOOOO0O00OOO0};"+activityCookie }#line:282
    OOOOOOO000OOO000O =requests .request ("POST",O00OO00OO0O000000 ,headers =OOO0OOOOO000OOO00 ,data =OO000O0OOO0O00000 )#line:283
    refresh_cookies (OOOOOOO000OOO000O )#line:284
def checkTokenInSession (OOOO0O0000OOOOOOO ):#line:286
    O00000O0000OO0O00 ="https://jinggeng-isv.isvjcloud.com/front/checkTokenInSession"#line:287
    O0OOO00000OO00OOO =f"userId={user_id}&token={OOOO0O0000OOOOOOO}"#line:288
    O0OO00000OOOO000O ={'Host':'jinggeng-isv.isvjcloud.com','Accept':'application/json, text/javascript, */*; q=0.01','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'https://jinggeng-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':f'{activityUrl}&isOpenCard=0&from=kouling','Content-Length':'99','Cookie':activityCookie }#line:302
    OO00O0OOOOOOOOOOO =requests .request ("POST",O00000O0000OO0O00 ,headers =O0OO00000OOOO000O ,data =O0OOO00000OO00OOO )#line:303
    refresh_cookies (OO00O0OOOOOOOOOOO )#line:304
def shopmember (OOOO000000OOO0O0O ):#line:306
    OOO00O0OO00OO0OO0 =f'https://shopmember.m.jd.com/shopcard/?venderId={user_id}&channel=401&returnUrl={quote_plus(activityUrl + "&isOpenCard=1")}'#line:307
    O00O0O0O0O0O00OOO ={'Host':'shopmember.m.jd.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive','Cookie':OOOO000000OOO0O0O ,'User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Referer':'https://jinggeng-isv.isvjcloud.com/','Accept-Encoding':'gzip, deflate, br'}#line:317
    requests .request ("GET",OOO00O0OO00OO0OO0 ,headers =O00O0O0O0O0O00OOO )#line:318
def bindWithVender (OOOO0O0OOO0O00OO0 ):#line:320
    try :#line:321
        OO000OOOOOO0OOOOO ={'appid':'shopmember_m_jd_com','functionId':'bindWithVender','body':json .dumps ({'venderId':user_id ,'shopId':user_id ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:330
        OOOO00000OO0O0O0O ={'Host':'api.m.jd.com','Accept':'*/*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://shop.m.jd.com','x-referer-page':'https://shop.m.jd.com/member/m/shopcard','Referer':f'https://shopmember.m.jd.com/shopcard/?venderId={user_id}&returnUrl={quote_plus(activityUrl + "&isOpenCard=1")}','User-Agent':ua ,'Cookie':OOOO0O0OOO0O00OO0 }#line:343
        OO0OO00O0000O000O =requests .request ("POST","https://api.m.jd.com/",headers =OOOO00000OO0O0O0O ,data =OO000OOOOOO0OOOOO ,timeout =10 ).text #line:344
        O0OO0O000O0OO0O0O =json .loads (OO0OO00O0000O000O )#line:345
        if O0OO0O000O0OO0O0O ['success']:#line:346
            if "火爆"in O0OO0O000O0OO0O0O ['message']or "失败"in O0OO0O000O0OO0O0O ['message']or "解绑"in O0OO0O000O0OO0O0O ['message']:#line:347
                print (f"\t⛈⛈⛈{O0OO0O000O0OO0O0O['message']}")#line:348
            else :#line:349
                print (f"\t🎉🎉🎉{O0OO0O000O0OO0O0O['message']}")#line:350
            return O0OO0O000O0OO0O0O ['message']#line:351
    except Exception as OO0000OOO0OOO0OOO :#line:352
        print (f"bindWithVender Error: {user_id} {OO0000OOO0OOO0OOO}")#line:353
def receiveInviteJoinAward (OOO00000OO0O00000 ,O00000OOO00OOO00O ):#line:355
    O00O0OOOO00OOO0O0 ="https://jinggeng-isv.isvjcloud.com/ql/front/receiveInviteJoinAward"#line:356
    OOOOO0OOOO0O00O0O =f"act_id={ac_id}&user_id={user_id}&awardId={O00000OOO00OOO00O}"#line:357
    O0OO0OOOO00O000O0 ={'Host':'jinggeng-isv.isvjcloud.com','Accept':'application/json, text/javascript, */*; q=0.01','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'https://jinggeng-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':f'{activityUrl}&isOpenCard=0&from=kouling&sid=09a25fb32a08d0b0fbdef65ab52a40dw&un_area=15_1213_1215_50108','Content-Length':'99','Cookie':f"IsvToken={OOO00000OO0O00000};"+activityCookie }#line:371
    OOOOOO000OO0O0000 =requests .request ("POST",O00O0OOOO00OOO0O0 ,headers =O0OO0OOOO00O000O0 ,data =OOOOO0OOOO0O00O0O ).text #line:372
    O0OO00OOOO00O0OO0 =eval (OOOOOO000OO0O0000 .replace ('true','True').replace ('false','False').replace ('none','None'))#line:373
    if O0OO00OOOO00O0OO0 ['succ']is True :#line:374
        O0O0O0O0O0O00OO0O =eval (str (O0OO00OOOO00O0OO0 ['msg']).replace ('\\\\',''))#line:375
        if O0O0O0O0O0O00OO0O ['isSendSucc']:#line:376
            O0OOO00O000O0O0OO =O0O0O0O0O0O00OO0O ['drawAwardDto']['awardType'].replace ('JD_BEAN','京豆').replace ('JD_POINT','积分')#line:377
            OOOO00OO0O0O000O0 =O0O0O0O0O0O00OO0O ['drawAwardDto']['awardDenomination']#line:378
            print (f"\t🎉🎉成功领取{OOOO00OO0O0O000O0}{O0OOO00O000O0O0OO}")#line:379
    else :#line:380
        print (f"\t🎉🎉{O0OO00OOOO00O0OO0['msg']}")#line:381
if __name__ =='__main__':#line:384
    r =redis_conn ()#line:385
    try :#line:386
        cks =getCk #line:387
        if not cks :#line:388
            sys .exit ()#line:389
    except :#line:390
        print ("未获取到有效COOKIE,退出程序！")#line:391
        sys .exit ()#line:392
    global inviterCode ,inviteSuccNums ,activityUrl ,needInviteNums ,rewardIndex ,firstCk #line:393
    inviteSuccNums =0 #line:394
    inviterCode =inviterNick #line:395
    activityUrl =activity_url #line:396
    needInviteNums =None #line:397
    rewardIndex =0 #line:398
    num =0 #line:399
    for cookie in cks :#line:400
        num +=1 #line:401
        if num ==1 :#line:402
            firstCk =cookie #line:403
        if num %5 ==0 :#line:404
            print ("⏰等待5s")#line:405
            time .sleep (5 )#line:406
        global ua ,activityCookie ,token ,getIndex #line:407
        getIndex =0 #line:408
        ua =userAgent ()#line:409
        try :#line:410
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:411
            pt_pin =unquote_plus (pt_pin )#line:412
        except IndexError :#line:413
            pt_pin =f'用户{num}'#line:414
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:415
        print (datetime .now ())#line:416
        token =''#line:417
        activityCookie =''#line:418
        activityCookie =getActivity (num ,0 ,inviterCode ,0 )#line:419
        try :#line:420
            token =getToken (cookie ,r )#line:421
            if token is None :#line:422
                if num ==1 :#line:423
                    print (f"⚠️车头获取Token失败,退出本程序！")#line:424
                    os ._exit ()#line:426
                print (f"⚠️获取Token失败！⏰等待3s")#line:427
                time .sleep (3 )#line:428
                continue #line:429
        except :#line:430
            print (f"⚠️获取Token失败！⏰等待3s")#line:431
            time .sleep (3 )#line:432
            continue #line:433
        time .sleep (1.5 )#line:434
        setMixNick0 =setMixNick (token )#line:435
        if setMixNick0 is None :#line:436
            if num ==1 :#line:437
                print (f"⚠️车头获取邀请码失败,退出本程序！")#line:438
                sys .exit ()#line:439
            else :#line:440
                continue #line:441
        else :#line:442
            print (f"邀请码->: {setMixNick0}")#line:443
        time .sleep (1 )#line:444
        print (f"准备助力-->: {inviterCode}")#line:445
        inviteSuccNum =getActivity (num ,0 ,inviterCode ,1 )#line:446
        if num ==1 :#line:447
            errorMsg0 =inviteSuccNum [0 ]#line:448
            if "跳开卡页面"not in errorMsg0 :#line:449
                print ("无法助力自己")#line:450
            inviteSuccNums0 =inviteSuccNum [1 ]#line:451
            needInviteNums =inviteSuccNum [2 ]#line:452
            inviteSuccNums =len (eval (inviteSuccNums0 ))#line:453
            print (f"🛳已经邀请{inviteSuccNums}人")#line:454
            for i ,needNum0 in enumerate (needInviteNums ):#line:455
                needNum =needNum0 [0 ]#line:456
                awardId =needNum0 [1 ]#line:457
                equityType =needNum0 [2 ]#line:458
                if inviteSuccNums >=needNum :#line:459
                    print (f"🎉恭喜已完成第{i + 1}档邀请，快去领奖吧！")#line:460
                    time .sleep (1 )#line:461
                    recordActPvUvdata (token )#line:462
                    checkTokenInSession (token )#line:463
                    time .sleep (1 )#line:464
                    if equityType =="JD_GOODS":#line:465
                        print (f"\t🎉🎉成功获得实物奖励,请尽快前往领取:{activityUrl}")#line:466
                    else :#line:467
                        receiveInviteJoinAward (token ,awardId )#line:468
                    rewardIndex +=1 #line:469
                    time .sleep (3 )#line:470
                    if i +1 ==len (needInviteNums ):#line:471
                        print ("🎉🎉🎉奖励全部领取完毕~")#line:472
                        sys .exit ()#line:473
                time .sleep (1 )#line:474
            inviterCode =setMixNick0 #line:475
            activityUrl =f"https://jinggeng-isv.isvjcloud.com/ql/front/showInviteJoin?id={ac_id}&user_id={user_id}&inviterNick={inviterCode}"#line:476
            continue #line:477
        else :#line:478
            errorMsg1 =inviteSuccNum #line:479
            if "跳开卡页面"not in errorMsg1 :#line:481
                if "已成功邀请您加入本店会员"in errorMsg1 :#line:482
                    print ("⛈已经是会员了,无法完成助力")#line:483
                else :#line:484
                    print (f"🛳{errorMsg1}")#line:485
                time .sleep (1 )#line:486
                continue #line:487
        time .sleep (1.5 )#line:488
        recordActPvUvdata (token )#line:489
        checkTokenInSession (token )#line:490
        time .sleep (1 )#line:491
        shopmember (cookie )#line:492
        print ("现在去开卡")#line:493
        open_result =bindWithVender (cookie )#line:494
        if open_result is not None :#line:495
            if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:496
                time .sleep (1.5 )#line:497
                print ("\t尝试重新入会 第1次")#line:498
                open_result =bindWithVender (cookie )#line:499
                if "火爆"in open_result or "失败"in open_result or "解绑"in open_result :#line:500
                    time .sleep (1.5 )#line:501
                    print ("\t尝试重新入会 第2次")#line:502
                    open_result =bindWithVender (cookie )#line:503
        time .sleep (1 )#line:504
        if num ==1 :#line:505
            getIndex =2 #line:506
        errorMsg2 =getActivity (num ,1 ,inviterCode ,getIndex )#line:507
        time .sleep (2 )#line:508
        recordActPvUvdata (token )#line:509
        checkTokenInSession (token )#line:510
        if num ==1 and "开卡失败"in errorMsg2 :#line:512
            print (f"⚠️车头疑似火爆号,退出本程序！")#line:513
            sys .exit ()#line:514
        if "已成功邀请您加入本店会员"in errorMsg2 :#line:515
            inviteSuccNums +=1 #line:516
            print (f"🛳已经邀请{inviteSuccNums}人")#line:517
            for i ,needNum1 in enumerate (needInviteNums ):#line:518
                needNum =needNum1 [0 ]#line:519
                awardId =needNum1 [1 ]#line:520
                equityType =needNum1 [2 ]#line:521
                if inviteSuccNums >=needNum :#line:522
                    if rewardIndex >=i +1 :#line:523
                        time .sleep (1 )#line:524
                        continue #line:525
                    print (f"🎉恭喜已完成第{i + 1}档邀请，快去领奖吧！")#line:526
                    token =getToken (firstCk ,r )#line:527
                    activityCookie =getActivity (1 ,0 ,inviterCode ,3 )#line:528
                    setMixNick (token )#line:529
                    time .sleep (0.5 )#line:530
                    recordActPvUvdata (token )#line:531
                    time .sleep (0.5 )#line:532
                    if equityType =="JD_GOODS":#line:533
                        print (f"\t🎉🎉成功获得实物奖励,请尽快前往领取:{activityUrl}")#line:534
                    else :#line:535
                        receiveInviteJoinAward (token ,awardId )#line:536
                    rewardIndex +=1 #line:537
                    time .sleep (3 )#line:538
                    if i +1 ==len (needInviteNums ):#line:539
                        print ("🎉🎉🎉奖励全部领取完毕~")#line:540
                        sys .exit ()#line:541
        if num ==1 :#line:542
            inviterCode =setMixNick0 #line:543
            activityUrl =f"https://jinggeng-isv.isvjcloud.com/ql/front/showInviteJoin?id={ac_id}&user_id={user_id}&inviterNick={inviterCode}"#line:544
        time .sleep (3 )