#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDrawPrize_JX.py(邀好友抽现金抽奖JX)
Author: HarbourJ
Date: 2023/3/15 10:00
TG: https://t.me/HarbourToulu
cron: 30 0 1,21 * * *
new Env('邀好友抽现金抽奖JX');
ActivityEntry: https://prodev.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html
变量：export inviteDrawPin="车头pin"
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from urllib .parse import quote_plus ,unquote_plus ,quote #line:2
from functools import partial #line:3
print =partial (print ,flush =True )#line:4
import warnings #line:5
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:6
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
apCashPageSize =20 #line:22
linkIds =['Wvzc_VpNTlSkiQdHT8r7QA']#line:23
activityUrl ="https://prodev.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html"#line:24
def getJdTime ():#line:27
    OO00OO0OO0O0000O0 =int (round (time .time ()*1000 ))#line:28
    return OO00OO0OO0O0000O0 #line:29
def printf (OOOOO000O00O0O00O ,O00O000000O0O0OOO ):#line:31
    try :#line:32
        O00OOO0O0O000O0OO =re .compile (r'pt_pin=(.*?);').findall (OOOOO000O00O0O00O )[0 ]#line:33
        O00OOO0O0O000O0OO =unquote_plus (O00OOO0O0O000O0OO )#line:34
    except IndexError :#line:35
        O00OOO0O0O000O0OO =re .compile (r'pin=(.*?);').findall (OOOOO000O00O0O00O )[0 ]#line:36
        O00OOO0O0O000O0OO =unquote_plus (O00OOO0O0O000O0OO )#line:37
    print (f"{str(datetime.now())[0:22]}->{O00OOO0O0O000O0OO}->{O00O000000O0O0OOO}")#line:38
def base64Encode (OOO0OOO0O0OOO00OO ):#line:40
    OO00O000OO0O0OOOO =""#line:41
    OOOOO0OO00000OO00 =[]#line:42
    O00O00OOO0O0OOO0O =""#line:43
    OO00000O0O0OO0000 ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:44
    for O00OO0OO0O000000O in OOO0OOO0O0OOO00OO :#line:45
        OO00O000OO0O0OOOO +="{:08}".format (int (str (bin (ord (O00OO0OO0O000000O ))).replace ("0b","")))#line:46
    for O0000OOOOO000OO00 in range (0 ,len (OO00O000OO0O0OOOO ),6 ):#line:47
        OOOOO0OO00000OO00 .append ("{:<06}".format (OO00O000OO0O0OOOO [O0000OOOOO000OO00 :O0000OOOOO000OO00 +6 ]))#line:48
    for O0OOOOO00O000O0OO in OOOOO0OO00000OO00 :#line:49
        O00O00OOO0O0OOO0O =O00O00OOO0O0OOO0O +OO00000O0O0OO0000 [int (O0OOOOO00O000O0OO ,2 )]#line:50
    if len (O00O00OOO0O0OOO0O )%4 ==2 :#line:51
        O00O00OOO0O0OOO0O +="=="#line:52
    elif len (O00O00OOO0O0OOO0O )%4 ==3 :#line:53
        O00O00OOO0O0OOO0O +="="#line:54
    return O00O00OOO0O0OOO0O #line:55
def userAgent ():#line:56
    import uuid #line:57
    OO000OOOO0OO0O0OO ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:58
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(OO000OOOO0OO0O0OO).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:59
def get_h5st_body (O00O00O0O00O000OO ,O000OO0OOOO0O0O00 ,OOOOO0OO0O0OOOO00 ,O0OO00OO0000O00OO ,OOO0O0O0OOOO00O0O ):#line:60
    try :#line:61
        OOOO00000OOO00000 =re .compile (r'pt_pin=(.*?);').findall (O000OO0OOOO0O0O00 )[0 ]#line:62
        OOOO00000OOO00000 =unquote_plus (OOOO00000OOO00000 )#line:63
    except IndexError :#line:64
        OOOO00000OOO00000 =re .compile (r'pin=(.*?);').findall (O000OO0OOOO0O0O00 )[0 ]#line:65
        OOOO00000OOO00000 =unquote_plus (OOOO00000OOO00000 )#line:66
    O0OO0OO0000OOOOO0 =O00O00O0O00O000OO .split (";")[2 ]#line:67
    OOO0O0O0OOOO00O0O ={"appId":O0OO00OO0000O00OO ,"appid":"activities_platform","ua":O00O00O0O00O000OO ,"pin":OOOO00000OOO00000 ,"functionId":OOOOO0OO0O0OOOO00 ,"body":OOO0O0O0OOOO00O0O ,"expand":{"url":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","og":"https://pro.m.jd.com"},"clientVersion":O0OO0OO0000OOOOO0 ,"version":"4.7"}#line:68
    try :#line:69
        import base64 #line:70
        O0OO000OO0OO000O0 =["aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAzL2FwaS9oNXN0"]#line:71
        O0OO000OO0OO000O0 =random .choice (O0OO000OO0OO000O0 )#line:72
        O000OOOO00O0OOOOO =json .dumps (OOO0O0O0OOOO00O0O )#line:73
        OOOO0O0OO0OOO000O ={'Content-Type':'application/json'}#line:74
        O0O00OOO000000O0O =requests .request ("POST",base64 .b64decode (O0OO000OO0OO000O0 .encode ('utf-8')).decode ('utf-8'),headers =OOOO0O0OO0OOO000O ,timeout =10 ,data =O000OOOO00O0OOOOO ).json ()#line:75
        if O0O00OOO000000O0O ['code']==200 :#line:76
            return O0O00OOO000000O0O ['data']#line:77
        else :#line:78
            printf (O000OO0OOOO0O0O00 ,f"调用远程h5st接口失败1")#line:79
            return #line:80
    except Exception as OO0O0OO0OOOOOOO00 :#line:81
        printf (O000OO0OOOO0O0O00 ,f"调用远程h5st接口失败2:{OO0O0OO0OOOOOOO00}")#line:82
        get_h5st_body (O00O00O0O00O000OO ,O000OO0OOOO0O0O00 ,OOOOO0OO0O0OOOO00 ,O0OO00OO0000O00OO ,OOO0O0O0OOOO00O0O )#line:83
        return #line:84
def inviteFissionDrawPrize (O00OO0O0OO0OOO000 ,O0O0OO000000OOOO0 ,OOOOO0OO0OOO0OOO0 ,OOO0OO0OO0O00OO0O ,OOO0O0OO0O0OO0OOO ):#line:85
    O0000000OOOO0OO00 ="https://api.m.jd.com/api"#line:86
    O00OO00O0O0000O00 =get_h5st_body (O00OO0O0OO0OOO000 ,O0O0OO000000OOOO0 ,OOOOO0OO0OOO0OOO0 ,OOO0OO0OO0O00OO0O ,OOO0O0OO0O0OO0OOO )#line:87
    if not O00OO00O0O0000O00 :#line:88
        return #line:89
    O0OOOOOOO0O0O0000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O00OO0O0OO0OOO000 ,'Cookie':O0O0OO000000OOOO0 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:90
    OOO0O00O000OOO0O0 =requests .request ("POST",O0000000OOOO0OO00 ,headers =O0OOOOOOO0O0O0000 ,data =O00OO00O0O0000O00 )#line:91
    if OOO0O00O000OOO0O0 .status_code ==200 :#line:92
        OOO0000OOO0O0OOO0 =OOO0O00O000OOO0O0 .json ()#line:93
        if OOO0000OOO0O0OOO0 ['data']:#line:94
            return OOO0O00O000OOO0O0 .status_code ,OOO0000OOO0O0OOO0 ['data']['prizeValue'],OOO0000OOO0O0OOO0 ['data']['rewardType']#line:95
        else :#line:96
            return OOO0O00O000OOO0O0 .status_code ,OOO0O00O000OOO0O0 .text #line:97
    else :#line:98
        printf (O0O0OO000000OOOO0 ,f"{OOO0O00O000OOO0O0.status_code}")#line:99
        return OOO0O00O000OOO0O0 .status_code ,OOO0O00O000OOO0O0 .text #line:100
def inviteFissionReceive (O0OO000O00OOO0O00 ,O000O00OO00OO0000 ,O0O00OOO0OOO00O00 ,OOOOOOOO0OOO000OO ,OO000O0OOO0000O0O ):#line:101
    OOOOOO0O00O0OO00O ="https://api.m.jd.com/api"#line:102
    O0OO00O0OOO0OO000 =get_h5st_body (O0OO000O00OOO0O00 ,O000O00OO00OO0000 ,O0O00OOO0OOO00O00 ,OOOOOOOO0OOO000OO ,OO000O0OOO0000O0O )#line:103
    if not O0OO00O0OOO0OO000 :#line:104
        return #line:105
    OOOO00O0OOO0O00O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0OO000O00OOO0O00 ,'Cookie':O000O00OO00OO0000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:106
    O00O000OO0OOO0000 =requests .request ("POST",OOOOOO0O00O0OO00O ,headers =OOOO00O0OOO0O00O0 ,data =O0OO00O0OOO0OO000 )#line:107
    if O00O000OO0OOO0000 .status_code ==200 :#line:108
        O00000OO0O0O0000O =O00O000OO0OOO0000 .json ()#line:109
        if O00000OO0O0O0000O ['data']:#line:110
            printf (O000O00OO00OO0000 ,f"{O00O000OO0OOO0000.status_code} {O00000OO0O0O0000O['data']}")#line:111
            return O00000OO0O0O0000O ['data']#line:112
        else :#line:113
            printf (O000O00OO00OO0000 ,f"{O00O000OO0OOO0000.status_code} {O00000OO0O0O0000O}")#line:114
            return O00000OO0O0O0000O #line:115
def superRedBagList (O0OO00O000OOO00O0 ,O0O0O00000000OO00 ,O0O00O0000OO0O0OO ,OOOO0OOO0O0000O00 ,O00000O00OO0000O0 ):#line:116
    OO000000OOO000O0O ="https://api.m.jd.com/api"#line:117
    O0OO0O00O0000OOO0 =get_h5st_body (O0OO00O000OOO00O0 ,O0O0O00000000OO00 ,O0O00O0000OO0O0OO ,OOOO0OOO0O0000O00 ,O00000O00OO0000O0 )#line:118
    if not O0OO0O00O0000OOO0 :#line:119
        return #line:120
    O0O00OOO0O00OOOOO ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0OO00O000OOO00O0 ,'Cookie':O0O0O00000000OO00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:121
    O0O00OOOO0OOO00O0 =requests .request ("POST",OO000000OOO000O0O ,headers =O0O00OOO0O00OOOOO ,data =O0OO0O00O0000OOO0 )#line:122
    if O0O00OOOO0OOO00O0 .status_code ==200 :#line:123
        OOO000O0O0OO0O00O =O0O00OOOO0OOO00O0 .json ()#line:124
        if OOO000O0O0OO0O00O ['data']:#line:125
            return OOO000O0O0OO0O00O ['data']#line:126
        else :#line:127
            printf (O0O0O00000000OO00 ,f"{O0O00OOOO0OOO00O0.status_code} {OOO000O0O0OO0O00O}")#line:128
            return O0O00OOOO0OOO00O0 .text #line:129
    else :#line:130
        printf (O0O0O00000000OO00 ,f"{O0O00OOOO0OOO00O0.status_code}")#line:131
def apCashWithDraw (O0OOO0OO0000OOO00 ,O0OOO0O0O0OOO0OOO ,OO000O0O0000O0000 ,OO0O0OOOOOO0OOO00 ,OOO00OO00OOOO0OOO ):#line:132
    OOO00OO0000000O0O ="https://api.m.jd.com/"#line:133
    OOO00OO0O0OOO0000 ={"linkId":linkId ,"businessSource":"NONE","base":{"id":O0OOO0O0O0OOO0OOO ,"business":"fission","poolBaseId":OO000O0O0000O0000 ,"prizeGroupId":OO0O0OOOOOO0OOO00 ,"prizeBaseId":OOO00OO00OOOO0OOO ,"prizeType":4 }}#line:134
    OO00O000OOO0000OO =get_h5st_body (ua ,O0OOO0OO0000OOO00 ,"apCashWithDraw","8c6ae",OOO00OO0O0OOO0000 )#line:135
    if not OO00O000OOO0000OO :#line:136
        return #line:137
    OO0O000O0O00OO000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O0OOO0OO0000OOO00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:138
    O0O0O000O00O0000O =requests .request ("POST",OOO00OO0000000O0O ,headers =OO0O000O0O00OO000 ,data =OO00O000OOO0000OO )#line:139
    if O0O0O000O00O0000O .status_code ==200 :#line:140
        OOOO0OOOO0O0OO0O0 =O0O0O000O00O0000O .json ()#line:141
        if OOOO0OOOO0O0OO0O0 ['data']:#line:142
            return OOOO0OOOO0O0OO0O0 ['data']['message']#line:143
        else :#line:144
            printf (O0OOO0OO0000OOO00 ,f"{O0O0O000O00O0000O.status_code} {OOOO0OOOO0O0OO0O0}")#line:145
def apRecompenseDrawPrize (O00000OO0OOO0O0OO ,O0000OO0OO0OOOOO0 ,OO000000O0OO0000O ,O000OOOOOOOO000O0 ,O0OOOO0OO0OOOO0O0 ):#line:146
    O00OOOO0OOO0O0O00 ="https://api.m.jd.com/"#line:147
    OO0OO00OOOO0O000O ={"linkId":linkId ,"drawRecordId":O0000OO0OO0OOOOO0 ,"business":"fission","poolId":OO000000O0OO0000O ,"prizeGroupId":O000OOOOOOOO000O0 ,"prizeId":O0OOOO0OO0OOOO0O0 ,}#line:148
    O00OOOOO0OOO0000O =get_h5st_body (ua ,O00000OO0OOO0O0OO ,"apRecompenseDrawPrize","8c6ae",OO0OO00OOOO0O000O )#line:149
    if not O00OOOOO0OOO0000O :#line:150
        return #line:151
    OO00O0O0OO0O0OO0O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O00000OO0OOO0O0OO ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:152
    O0OOO0OO000O0OO0O =requests .request ("POST",O00OOOO0OOO0O0O00 ,headers =OO00O0O0OO0O0OO0O ,data =O00OOOOO0OOO0000O )#line:153
    if O0OOO0OO000O0OO0O .status_code ==200 :#line:154
        O00O0000O000OOOOO =O0OOO0OO000O0OO0O .json ()#line:155
        if O00O0000O000OOOOO ['data']:#line:156
            return "兑换红包成功"#line:157
        else :#line:158
            printf (O00000OO0OOO0O0OO ,f"{O0OOO0OO000O0OO0O.status_code} {O00O0000O000OOOOO}")#line:159
if __name__ =='__main__':#line:162
    try :#line:163
        cks =getCk #line:164
        if not cks :#line:165
            sys .exit ()#line:166
    except :#line:167
        print ("未获取到有效COOKIE,退出程序！")#line:168
        sys .exit ()#line:169
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:171
    if inviteDrawPin :#line:172
        cookie_ =[O0OO0O0OOOOOOOO00 for O0OO0O0OOOOOOOO00 in cks if inviteDrawPin in O0OO0O0OOOOOOOO00 ]#line:173
        if cookie_ :#line:174
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:175
            cookie =cookie_ [0 ]#line:176
        else :#line:177
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:178
            sys .exit ()#line:179
    else :#line:180
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:181
        cookie =cks [0 ]#line:182
    ua =userAgent ()#line:183
    cash =[]#line:184
    successful =[]#line:185
    total =0 #line:186
    i =0 #line:187
    redpacket =[]#line:188
    for index ,linkId in enumerate (linkIds ,1 ):#line:190
        while True :#line:191
            try :#line:192
                info =inviteFissionDrawPrize (ua ,cookie ,"inviteFissionDrawPrize","c02c6",{"linkId":linkId })#line:193
                if "活动太火爆"in str (info ):#line:194
                    printf (cookie ,info )#line:195
                    time .sleep (0.2 )#line:196
                    continue #line:197
            except Exception as e :#line:198
                printf (cookie ,e )#line:199
                continue #line:200
            if not info :#line:201
                continue #line:202
            if not info [1 ]:#line:203
                printf (cookie ,f"{info[0]} ⚠️抽奖结果为{info[1]}")#line:204
                continue #line:205
            elif "抽奖次数已用完"in info [1 ]:#line:206
                printf (cookie ,f"{info[0]} ⚠️抽奖次数已用完")#line:207
                break #line:208
            elif "本场活动已结束"in info [1 ]:#line:209
                printf (cookie ,f"{info[0]} ⏰本场活动已结束了,快去重新开始吧")#line:210
                break #line:211
            else :#line:212
                if info :#line:213
                    total +=1 #line:214
                    if info [2 ]==1 :#line:215
                        printf (cookie ,f"{info[0]} 🎫获得{info[1]}优惠券")#line:216
                    elif info [2 ]==2 :#line:217
                        printf (cookie ,f"{info[0]} 🧧获得{info[1]}红包")#line:218
                        redpacket .append (info [1 ])#line:219
                    else :#line:220
                        printf (cookie ,f"{info[0]} 💵获得{info[1]}现金")#line:221
                        cash .append (info [1 ])#line:222
    print (f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(O00OO0OOOO0O0O0OO) for O00OO0OOOO0O0O0OO in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(O0000000O0OOOOO00) for O0000000O0OOOOO00 in redpacket]))}元红包,开始提现****************\n")#line:224
    print (f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置****************")#line:226
    for index ,linkId in enumerate (linkIds ,1 ):#line:227
        i =0 #line:228
        while True :#line:229
            print (f"\n开始获取第{i + 1}页奖励列表\n")#line:230
            body ={"pageNum":i ,"pageSize":20 ,"linkId":linkId ,"business":"fission"}#line:231
            info =superRedBagList (ua ,cookie ,"superRedBagList","f2b1d",body )#line:232
            if not info :#line:233
                print ("等待10s重新获取")#line:234
                time .sleep (10 )#line:235
                continue #line:236
            i +=1 #line:237
            items =info ['items']#line:238
            if not items :#line:239
                printf (cookie ,"全部提现完成！")#line:240
                break #line:241
            for item in items :#line:242
                id =item ['id']#line:244
                amount =item ['amount']#line:245
                prizeType =item ['prizeType']#line:246
                state =item ['state']#line:247
                prizeConfigName =item ['prizeConfigName']#line:248
                prizeGroupId =item ['prizeGroupId']#line:249
                poolBaseId =item ['poolBaseId']#line:250
                prizeBaseId =item ['prizeBaseId']#line:251
                if prizeType ==4 and state !=3 and state !=4 :#line:252
                    cashInfo =apCashWithDraw (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:253
                    if cashInfo :#line:254
                        printf (cookie ,f"{amount}现金 {cashInfo}")#line:255
                        if "上限"in cashInfo or "其他pin"in cashInfo or "其它pin"in cashInfo :#line:256
                            cashInfo =apRecompenseDrawPrize (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:257
                            printf (cookie ,f"{amount}现金 {cashInfo}")#line:258
                    time .sleep (2 )#line:259
                else :#line:260
                    continue #line:261
            time .sleep (1 )#line:263
            if i >=apCashPageSize :#line:265
                break