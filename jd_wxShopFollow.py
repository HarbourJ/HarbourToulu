#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_wxShopFollow.py(关注店铺有礼-JK)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('关注店铺有礼-JK');
ActivityEntry: https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/activity?activityId=3d6dbfd9c8584be882f69cfad665ce8d
               变量 export jd_wxShopFollowId="活动🆔"
                   export jd_wxShopFollowRunNums="变量为需要运行账号数量" # 默认前12个账号
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
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:23
redis_port =os .environ .get ("redis_port")if os .environ .get ("redis_port")else "6379"#line:24
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:25
activityId =os .environ .get ("jd_wxShopFollowId")if os .environ .get ("jd_wxShopFollowId")else ""#line:26
runNums =os .environ .get ("jd_wxShopFollowRunNums")if os .environ .get ("jd_wxShopFollowRunNums")else 12 #line:27
if not activityId :#line:29
    print ("⚠️未发现有效活动变量,退出程序!")#line:30
    sys .exit ()#line:31
runNums =int (runNums )#line:33
if runNums ==12 :#line:34
    print ('🤖本次关注默认跑前12个账号,设置自定义变量:export jd_wxShopFollowRunNums="需要运行的ck数量"')#line:35
else :#line:36
    print (f'🤖本次运行前{runNums}个账号')#line:37
activityUrl =f"https://lzkj-isv.isvjd.com/wxShopFollowActivity/activity?activityId={activityId}"#line:39
def redis_conn ():#line:41
    try :#line:42
        import redis #line:43
        try :#line:44
            OO0OOOOOOOO0OO000 =redis .ConnectionPool (host =redis_url ,port =6379 ,decode_responses =True ,socket_connect_timeout =5 ,password =redis_pwd )#line:45
            OOOOOO0O0000O0O00 =redis .Redis (connection_pool =OO0OOOOOOOO0OO000 )#line:46
            OOOOOO0O0000O0O00 .get ('conn_test')#line:47
            print ('✅redis连接成功')#line:48
            return OOOOOO0O0000O0O00 #line:49
        except :#line:50
            print ("⚠️redis连接异常")#line:51
    except :#line:52
        print ("⚠️缺少redis依赖，请运行pip3 install redis")#line:53
        sys .exit ()#line:54
def getToken (OO0OO0OOOO00O00OO ,r =None ):#line:56
    O000OO0O0O0O000OO =f'{activityUrl.split("com/")[0]}com'#line:57
    try :#line:58
        O0000O00OO00O0OO0 =unquote_plus (re .compile (r'pt_pin=(.*?);').findall (OO0OO0OOOO00O00OO )[0 ])#line:59
    except :#line:60
        O0000O00OO00O0OO0 =OO0OO0OOOO00O00OO [:15 ]#line:61
    try :#line:62
        try :#line:63
            OO0OOO0OO0OOOO000 =r .get (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0000O00OO00O0OO0}')#line:64
        except Exception as O0OO0OO0000O0000O :#line:65
            OO0OOO0OO0OOOO000 =None #line:67
        if OO0OOO0OO0OOOO000 is not None :#line:68
            print (f"♻️获取缓存Token")#line:69
            return OO0OOO0OO0OOOO000 #line:70
        else :#line:71
            s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0OO0OOOO00O00OO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:82
            sign ({"url":f"{O000OO0O0O0O000OO}","id":""},'isvObfuscator')#line:83
            O000OO0OO00O00O00 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:84
            if O000OO0OO00O00O00 .status_code !=200 :#line:85
                print (O000OO0OO00O00O00 .status_code )#line:86
                return #line:87
            else :#line:88
                if "参数异常"in O000OO0OO00O00O00 .text :#line:89
                    print (O000OO0OO00O00O00 .text )#line:90
                    return #line:91
            OOO0O0O0000O000OO =O000OO0OO00O00O00 .json ()['token']#line:92
            try :#line:93
                if r .set (f'{activityUrl.split("https://")[1].split("-")[0]}_{O0000O00OO00O0OO0}',OOO0O0O0000O000OO ,ex =1800 ):#line:94
                    print ("✅Token缓存成功")#line:95
                else :#line:96
                    print ("❌Token缓存失败")#line:97
            except Exception as O0OO0OO0000O0000O :#line:98
                print (f"✅获取实时Token")#line:100
            return OOO0O0O0000O000OO #line:101
    except Exception as O0OO0OO0000O0000O :#line:102
        print (f"Token error: {str(O0OO0OO0000O0000O)}")#line:103
        return #line:104
def getJdTime ():#line:106
    O00000OOOO0O0O0O0 =int (round (time .time ()*1000 ))#line:107
    return O00000OOOO0O0O0O0 #line:108
def randomString (OOOO00OO000OO0OO0 ,flag =False ):#line:110
    O0O00O0000O0OO00O ="0123456789abcdef"#line:111
    if flag :O0O00O0000O0OO00O =O0O00O0000O0OO00O .upper ()#line:112
    OO00O00O000OO000O =[random .choice (O0O00O0000O0OO00O )for _O000O0OOOO0OO00OO in range (OOOO00OO000OO0OO0 )]#line:113
    return ''.join (OO00O00O000OO000O )#line:114
def refresh_cookies (OOOO00000O000O00O ):#line:116
    if OOOO00000O000O00O .cookies :#line:117
        O0OO0OOO0O0OOO0OO =OOOO00000O000O00O .cookies .get_dict ()#line:118
        OOO0O0OOOOO0OO00O =[(O0OOO0OO0OOO0O0OO +"="+O0OO0OOO0O0OOO0OO [O0OOO0OO0OOO0O0OO ])for O0OOO0OO0OOO0O0OO in O0OO0OOO0O0OOO0OO ]#line:119
        global activityCookie #line:120
        O0OOO0OOOO0O00OO0 =[OO00O000OO00O0OO0 for OO00O000OO00O0OO0 in activityCookie .split (';')if OO00O000OO00O0OO0 !='']#line:121
        for OO0OOOO00OO0OOOO0 in O0OOO0OOOO0O00OO0 :#line:122
            for O00OOO0O0O0O00000 in OOO0O0OOOOO0OO00O :#line:123
                if OO0OOOO00OO0OOOO0 .split ('=')[0 ]==O00OOO0O0O0O00000 .split ('=')[0 ]:#line:124
                    if OO0OOOO00OO0OOOO0 .split ('=')[1 ]!=O00OOO0O0O0O00000 .split ('=')[1 ]:#line:125
                        O0OOO0OOOO0O00OO0 .remove (OO0OOOO00OO0OOOO0 )#line:126
        activityCookie =''.join (sorted ([(OO0000O0OO00O0O0O +";")for OO0000O0OO00O0O0O in list (set (O0OOO0OOOO0O00OO0 +OOO0O0OOOOO0OO00O ))]))#line:127
def getActivity ():#line:129
    O0O00O0O00OO0OO0O =f"https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/activity?activityId={activityId}"#line:130
    OOOO000OO0O0O0000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:138
    O0O0O00000OOOO0O0 =requests .request ("GET",O0O00O0O00OO0OO0O ,headers =OOOO000OO0O0O0000 )#line:139
    if O0O0O00000OOOO0O0 .status_code ==200 :#line:140
        if O0O0O00000OOOO0O0 .cookies :#line:141
            OOO0O0000000O00O0 =O0O0O00000OOOO0O0 .cookies .get_dict ()#line:142
            OO00000OO0O00O000 =[(OO0O0OOO0O0OOO00O +"="+OOO0O0000000O00O0 [OO0O0OOO0O0OOO00O ])for OO0O0OOO0O0OOO00O in OOO0O0000000O00O0 ]#line:143
            OO0OO0OO000OOOOO0 =''.join (sorted ([(OO0O00O000OOOOO00 +";")for OO0O00O000OOOOO00 in OO00000OO0O00O000 ]))#line:144
        return OO0OO0OO000OOOOO0 #line:145
    else :#line:146
        print (O0O0O00000OOOO0O0 .status_code )#line:147
        print ("⚠️疑似ip黑了")#line:148
        sys .exit ()#line:149
def getSystemConfigForNew ():#line:151
    OOO00OO0O0OOOO0O0 ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"#line:152
    OOOOOOO000O0OO0O0 =f'activityId={activityId}&activityType=17'#line:153
    O00OO0OOO000O0O0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:166
    OOOOOOOOO0O0OOOO0 =requests .request ("POST",OOO00OO0O0OOOO0O0 ,headers =O00OO0OOO000O0O0O ,data =OOOOOOO000O0OO0O0 )#line:167
    refresh_cookies (OOOOOOOOO0O0OOOO0 )#line:168
def getSimpleActInfoVo ():#line:170
    O0OOOOO00O0O00O0O ="https://lzkj-isv.isvjcloud.com/customer/getSimpleActInfoVo"#line:171
    OOOOO0OO0O0O00O0O =f"activityId={activityId}"#line:172
    OO0OOOOOOOO0OOO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:185
    O00OO0O0OO00OO00O =requests .request ("POST",O0OOOOO00O0O00O0O ,headers =OO0OOOOOOOO0OOO00 ,data =OOOOO0OO0O0O00O0O )#line:186
    refresh_cookies (O00OO0O0OO00OO00O )#line:187
    O0O0OO00O00OOOOOO =O00OO0O0OO00OO00O .json ()#line:188
    if O0O0OO00O00OOOOOO ['result']:#line:189
        return O0O0OO00O00OOOOOO ['data']#line:190
def getMyPing (OO000O0O00000OO0O ):#line:192
    O00000O00O0O0O0OO ="https://lzkj-isv.isvjcloud.com/customer/getMyPing"#line:193
    OO0O0OO00O0OOO0O0 =f"userId={OO000O0O00000OO0O}&token={token}&fromType=APP"#line:194
    OO00000O000OOOOO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:207
    O00O0O000O00OO0OO =requests .request ("POST",O00000O00O0O0O0OO ,headers =OO00000O000OOOOO0 ,data =OO0O0OO00O0OOO0O0 )#line:208
    refresh_cookies (O00O0O000O00OO0OO )#line:209
    O00OO0OO0OO0OO0O0 =O00O0O000O00OO0OO .json ()#line:210
    if O00OO0OO0OO0OO0O0 ['result']:#line:211
        return O00OO0OO0OO0OO0O0 ['data']['nickname'],O00OO0OO0OO0OO0O0 ['data']['secretPin']#line:212
    else :#line:213
        print (f"⚠️{O00OO0OO0OO0OO0O0['errorMessage']}")#line:214
def accessLogWithAD (O0O0OOOOO0000OOO0 ,OO00O0000O000OOO0 ):#line:216
    O000OO0O0O0O000O0 ="https://lzkj-isv.isvjcloud.com/common/accessLogWithAD"#line:217
    OOO0OO0O0OOO0OO00 =f"venderId={O0O0OOOOO0000OOO0}&code=17&pin={quote_plus(OO00O0000O000OOO0)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource="#line:218
    O00000O0000OO000O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:231
    O0000O000O0OOO00O =requests .request ("POST",O000OO0O0O0O000O0 ,headers =O00000O0000OO000O ,data =OOO0OO0O0OOO0OO00 )#line:232
    refresh_cookies (O0000O000O0OOO00O )#line:233
def activityContentOnly (O0OO0O0OOO0OOO000 ):#line:235
    O0OOO0OOOOO0OO00O ="https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/activityContentOnly"#line:236
    O0O0O0O000O0OO0OO =f"activityId={activityId}&pin={quote_plus(O0OO0O0OOO0OOO000)}"#line:237
    OOOOOOO000O000O0O ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:250
    O0O0OO00O0O00O00O =requests .request ("POST",O0OOO0OOOOO0OO00O ,headers =OOOOOOO000O000O0O ,data =O0O0O0O000O0OO0OO )#line:251
    refresh_cookies (O0O0OO00O0O00O00O )#line:252
    OOO00O0OO0OOO0O00 =O0O0OO00O0O00O00O .json ()#line:253
    if OOO00O0OO0OOO0O00 ['result']:#line:254
        OOOOOOOOOO00O0OOO =OOO00O0OO0OOO0O00 ['data']['canJoin']#line:255
        O0O0OOOOOOO00OO0O =OOO00O0OO0OOO0O00 ['data']['drawContentVOs']#line:256
        O000OO0OOOOOO000O =O0O0OOOOOOO00OO0O [0 ]['name']#line:260
        O00OOOO00O0OO000O =O0O0OOOOOOO00OO0O [0 ]['hasSendPrizeNum']#line:261
        O0OOOO00OO0O0000O =O0O0OOOOOOO00OO0O [0 ]['prizeNum']#line:262
        OOOO0O0O00O0OO00O =OOO00O0OO0OOO0O00 ['data']['canDrawTimes']#line:263
        OO000000OOO0O0000 =OOO00O0OO0OOO0O00 ['data']['needFollow']#line:264
        OO0OOO00OOOO0OOO0 =OOO00O0OO0OOO0O00 ['data']['hasFollow']#line:265
        return O000OO0OOOOOO000O ,O00OOOO00O0OO000O ,O0OOOO00OO0O0000O ,OOOO0O0O00O0OO00O ,OO000000OOO0O0000 ,OO0OOO00OOOO0OOO0 #line:266
    else :#line:267
        print (f"⛈{OOO00O0OO0OOO0O00['errorMessage']}")#line:268
        sys .exit ()#line:269
def shopInfo ():#line:271
    OO00O00OO000OO000 ="https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/shopInfo"#line:272
    O0000000000O000OO =f"activityId={activityId}"#line:273
    OOOOOO00OO0O00OO0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:286
    O0OOOO00OO000O000 =requests .request ("POST",OO00O00OO000OO000 ,headers =OOOOOO00OO0O00OO0 ,data =O0000000000O000OO )#line:287
    refresh_cookies (O0OOOO00OO000O000 )#line:288
    OO0000O00O0000OOO =O0OOOO00OO000O000 .json ()#line:289
    if OO0000O00O0000OOO ['result']:#line:290
        OO00O0O0O0OOOO00O =OO0000O00O0000OOO ['data']['shopName']#line:291
        return OO00O0O0O0OOOO00O #line:292
    else :#line:293
        print (f"⛈{OO0000O00O0000OOO['errorMessage']}")#line:294
def getActMemberInfo (OOOO0000OO0O00OOO ,OO0O00O000O000000 ):#line:296
    OO000OOO00OOO0000 ="https://lzkj-isv.isvjcloud.com/wxCommonInfo/getActMemberInfo"#line:297
    OOO0OO00OOO0OOOO0 =f"venderId={OOOO0000OO0O00OOO}&activityId={activityId}&pin={quote_plus(OO0O00O000O000000)}"#line:298
    O00OOOO000O0OO0OO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:311
    O0O00000OO00OOOO0 =requests .request ("POST",OO000OOO00OOO0000 ,headers =O00OOOO000O0OO0OO ,data =OOO0OO00OOO0OOOO0 )#line:312
    refresh_cookies (O0O00000OO00OOOO0 )#line:313
    O0OO0O00OO0O0O000 =O0O00000OO00OOOO0 .json ()#line:314
    print (O0OO0O00OO0O0O000 )#line:315
    if O0OO0O00OO0O0O000 ['result']:#line:316
        O0O0O000O0O0O000O =O0OO0O00OO0O0O000 ['data']['openCard']#line:317
        return O0O0O000O0O0O000O #line:318
    else :#line:319
        print (f"⛈{O0OO0O00OO0O0O000['errorMessage']}")#line:320
def followShop (O0O00O000000000OO ):#line:322
    O0OOO0000OO00O00O ="https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/follow"#line:323
    OOOO000OOO0000O0O =f"activityId={activityId}&pin={quote_plus(O0O00O000000000OO)}"#line:324
    O00OOOOOOOOO0OO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:337
    OOO0OO00O0O0000OO =requests .request ("POST",O0OOO0000OO00O00O ,headers =O00OOOOOOOOO0OO00 ,data =OOOO000OOO0000O0O )#line:338
    refresh_cookies (OOO0OO00O0O0000OO )#line:339
    OOO0O00OO00O0OO00 =OOO0OO00O0O0000OO .json ()#line:340
    if OOO0O00OO00O0OO00 ['result']:#line:341
        pass #line:342
    else :#line:343
        print (f"⛈{OOO0O00OO00O0OO00['errorMessage']}")#line:344
        if "店铺会员"in OOO0O00OO00O0OO00 ['errorMessage']:#line:345
            return 99 #line:346
def getInfo ():#line:348
    O000O0OOO0O0000O0 =f"https://lzkj-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId={activityId}"#line:349
    O000O0O000OOO00O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':activityCookie }#line:360
    O0O000O0O0OOO00O0 =requests .request ("GET",O000O0OOO0O0000O0 ,headers =O000O0O000OOO00O0 )#line:361
    refresh_cookies (O0O000O0O0OOO00O0 )#line:362
def getPrize (O0OO0O0OO00O0000O ):#line:364
    OO0OO0OO0OOOOOO0O ="https://lzkj-isv.isvjcloud.com/wxShopFollowActivity/getPrize"#line:365
    OO0O0OOOOOO0OO0O0 =f"activityId={activityId}&pin={quote_plus(O0OO0O0OO00O0000O)}"#line:366
    OOOOOOO0OOOOOO000 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json','X-Requested-With':'XMLHttpRequest','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':ua ,'Connection':'keep-alive','Referer':activityUrl ,'Cookie':f'IsvToken={token};{activityCookie}'}#line:379
    OO000OOOOO000O000 =requests .request ("POST",OO0OO0OO0OOOOOO0O ,headers =OOOOOOO0OOOOOO000 ,data =OO0O0OOOOOO0OO0O0 )#line:380
    O0OOO0000OO0O0OOO =OO000OOOOO000O000 .json ()#line:381
    if O0OOO0000OO0O0OOO ['result']:#line:382
        O0O000OO00OO000OO =O0OOO0000OO0O0OOO ['data']#line:383
        if O0O000OO00OO000OO ['drawOk']:#line:384
            O00OOOO00O0000OOO =O0O000OO00OO000OO ['name']#line:385
            return O00OOOO00O0000OOO #line:386
        else :#line:387
            if O0O000OO00OO000OO ['canDrawTimes']>0 :#line:388
                return 9 #line:389
            else :#line:390
                return 99 #line:391
    else :#line:392
        print (f"⛈{O0OOO0000OO0O0OOO['errorMessage']}")#line:393
        if '奖品已发完'in O0OOO0000OO0O0OOO ['errorMessage']:#line:394
            sys .exit ()#line:395
        return O0OOO0000OO0O0OOO ['errorMessage']#line:396
def bindWithVender (OO0OO0OO0OO000000 ,O0OO00OO0OOO0000O ):#line:398
    try :#line:399
        s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OO0OO0OO0OO000000 ,'Host':'api.m.jd.com','Referer':'https://shopmember.m.jd.com/','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:410
        s .params ={'appid':'jd_shop_member','functionId':'bindWithVender','body':json .dumps ({'venderId':O0OO00OO0OOO0000O ,'shopId':O0OO00OO0OOO0000O ,'bindByVerifyCodeFlag':1 },separators =(',',':'))}#line:419
        O0OOO00OO00O000O0 =s .post ('https://api.m.jd.com/',verify =False ,timeout =30 ).json ()#line:420
        if O0OOO00OO00O000O0 ['success']:#line:421
            return O0OOO00OO00O000O0 ['message'],O0OOO00OO00O000O0 ['result']['giftInfo']#line:422
    except Exception as OOOO0OO0O0O000OO0 :#line:423
        print (OOOO0OO0O0O000OO0 )#line:424
if __name__ =='__main__':#line:427
    global msg #line:428
    msg =''#line:429
    r =redis_conn ()#line:430
    try :#line:431
        cks =getCk #line:432
        if not cks :#line:433
            sys .exit ()#line:434
    except :#line:435
        print ("未获取到有效COOKIE,退出程序！")#line:436
        sys .exit ()#line:437
    num =0 #line:438
    for cookie in cks [:runNums ]:#line:439
        num +=1 #line:440
        if num %6 ==0 :#line:441
            print ("⏰等待5s,休息一下")#line:442
            time .sleep (5 )#line:443
        global ua ,activityCookie ,token #line:444
        ua =userAgent ()#line:445
        try :#line:446
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:447
            pt_pin =unquote_plus (pt_pin )#line:448
        except IndexError :#line:449
            pt_pin =f'用户{num}'#line:450
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:451
        print (datetime .now ())#line:452
        token =getToken (cookie ,r )#line:454
        if token is None :#line:455
            print (f"⚠️获取Token失败！⏰等待2s")#line:456
            time .sleep (2 )#line:457
            continue #line:458
        time .sleep (0.2 )#line:459
        activityCookie =getActivity ()#line:460
        time .sleep (0.2 )#line:461
        getSystemConfigForNew ()#line:462
        time .sleep (0.2 )#line:463
        getSimAct =getSimpleActInfoVo ()#line:464
        venderId =getSimAct ['venderId']#line:465
        time .sleep (0.2 )#line:466
        getPin =getMyPing (venderId )#line:467
        if getPin is not None :#line:468
            nickname =getPin [0 ]#line:469
            secretPin =getPin [1 ]#line:470
            time .sleep (0.3 )#line:471
            accessLogWithAD (venderId ,secretPin )#line:472
            time .sleep (0.3 )#line:473
            actContent =activityContentOnly (secretPin )#line:474
            if not actContent :#line:476
                continue #line:477
            priceName =actContent [0 ]#line:478
            hasSendPrizeNum =actContent [1 ]#line:479
            prizeNum =actContent [2 ]#line:480
            canDrawTimes =actContent [3 ]#line:481
            needFollow =actContent [4 ]#line:482
            hasFollow =actContent [5 ]#line:483
            time .sleep (0.15 )#line:484
            shopName =shopInfo ()#line:485
            if num ==1 :#line:486
                print (f"✅开启{shopName}-关注店铺有礼活动")#line:487
                print (f"🎁奖品{priceName}\n")#line:488
                msg +=f'✅开启{shopName}-关注店铺有礼活动\n📝活动地址{activityUrl}\n🎁奖品{priceName}\n\n'#line:489
            print (f"🎁共{prizeNum}份, 剩余{prizeNum-hasSendPrizeNum}份")#line:490
            if hasSendPrizeNum ==prizeNum :#line:491
                print ("⛈礼品已领完")#line:492
                sys .exit ()#line:493
            if canDrawTimes ==0 :#line:494
                print ("🤖已参加过本活动")#line:495
                time .sleep (1.5 )#line:496
                continue #line:497
            time .sleep (0.2 )#line:498
            getInfo ()#line:499
            if needFollow :#line:500
                if not hasFollow :#line:501
                    FS =followShop (secretPin )#line:502
                    if FS ==99 :#line:503
                        time .sleep (0.2 )#line:504
                        open_result =bindWithVender (cookie ,venderId )#line:505
                        if open_result is not None :#line:506
                            if "火爆"in open_result [0 ]or "失败"in open_result [0 ]or "解绑"in open_result [0 ]:#line:507
                                print (f"⛈{open_result[0]}")#line:508
                                time .sleep (1.5 )#line:509
                                continue #line:510
                            if "加入店铺会员成功"in open_result [0 ]:#line:511
                                print (f"\t💳{shopName} {open_result[0]}")#line:512
                                if open_result [1 ]:#line:513
                                    print (f"\t🎁获得{','.join([O000000OOO00OO0O0['discountString'] + O000000OOO00OO0O0['prizeName'] for O000000OOO00OO0O0 in open_result[1]['giftList']])}")#line:514
                            time .sleep (0.2 )#line:515
                            followShop (secretPin )#line:516
            time .sleep (0.15 )#line:517
            for i in range (3 ):#line:518
                priceName =getPrize (secretPin )#line:519
                if priceName ==9 :#line:520
                    time .sleep (0.2 )#line:521
                    continue #line:522
                else :#line:523
                    break #line:524
            if "火爆"in str (priceName )or priceName ==99 or priceName is None :#line:525
                print (f"😭获得💨💨💨")#line:526
            else :#line:527
                print (f"🎉获得{priceName}")#line:528
                msg +=f'【账号{num}】{pt_pin} 🎉{priceName}\n'#line:529
        time .sleep (1.5 )#line:531
    title ="🗣消息提醒：关注店铺有礼-JK"#line:533
    msg =f"⏰{str(datetime.now())[:19]}\n"+msg #line:534
    send (title ,msg )