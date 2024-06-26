#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDrawPrize_JD.py(转赚邀好友抽现金抽奖JD新版)
Author: HarbourJ
Date: 2023/3/15 10:00
TG: https://t.me/HarbourToulu
cron: 30 0 1,12,21 * * *
new Env('转赚邀好友抽现金抽奖JD新版');
ActivityEntry: https://pro.m.jd.com/mall/active/B2Y13x641hwWfpsoRenCzfbz4jR/index.html?inviterId=Q2VzHk9dkShW66_of58y-g&channelType=0&femobile=femobile&activityChannel=jdapp
变量：export inviteDrawPin="车头pin"
"""

import time ,requests ,sys ,re ,os ,json ,random, base64 #line:1
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
linkIds =['wDNvX5t2N52cWEM8cLOa0g']#line:23
activityUrl ="https://pro.m.jd.com/mall/active/B2Y13x641hwWfpsoRenCzfbz4jR/index.html"#line:24
def getJdTime ():#line:27
    O00OO0OO000OOOO00 =int (round (time .time ()*1000 ))#line:28
    return O00OO0OO000OOOO00 #line:29
def printf (OOO0000000000000O ,OOO00OO0O00OO00O0 ):#line:31
    try :#line:32
        OO00OO00OOOO0O000 =re .compile (r'pt_pin=(.*?);').findall (OOO0000000000000O )[0 ]#line:33
        OO00OO00OOOO0O000 =unquote_plus (OO00OO00OOOO0O000 )#line:34
    except IndexError :#line:35
        OO00OO00OOOO0O000 =re .compile (r'pin=(.*?);').findall (OOO0000000000000O )[0 ]#line:36
        OO00OO00OOOO0O000 =unquote_plus (OO00OO00OOOO0O000 )#line:37
    print (f"{str(datetime.now())[0:22]}->{OO00OO00OOOO0O000}->{OOO00OO0O00OO00O0}")#line:38
def base64Encode (O0000OOO0000O0O00 ):#line:40
    OOOO0OO000OOO000O =""#line:41
    O000O0OO00O00OO0O =[]#line:42
    O0O0OOOOOOOOO00O0 =""#line:43
    O0OO0OO0O0OO0OO0O ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:44
    for OOOO0O0O0O0000O00 in O0000OOO0000O0O00 :#line:45
        OOOO0OO000OOO000O +="{:08}".format (int (str (bin (ord (OOOO0O0O0O0000O00 ))).replace ("0b","")))#line:46
    for OOO0O0OO0O000OOOO in range (0 ,len (OOOO0OO000OOO000O ),6 ):#line:47
        O000O0OO00O00OO0O .append ("{:<06}".format (OOOO0OO000OOO000O [OOO0O0OO0O000OOOO :OOO0O0OO0O000OOOO +6 ]))#line:48
    for O0000OOOO0000O000 in O000O0OO00O00OO0O :#line:49
        O0O0OOOOOOOOO00O0 =O0O0OOOOOOOOO00O0 +O0OO0OO0O0OO0OO0O [int (O0000OOOO0000O000 ,2 )]#line:50
    if len (O0O0OOOOOOOOO00O0 )%4 ==2 :#line:51
        O0O0OOOOOOOOO00O0 +="=="#line:52
    elif len (O0O0OOOOOOOOO00O0 )%4 ==3 :#line:53
        O0O0OOOOOOOOO00O0 +="="#line:54
    return O0O0OOOOOOOOO00O0 #line:55
def userAgent ():#line:56
    import uuid #line:57
    OO0OO00O0OO0O000O ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:58
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(OO0OO00O0OO0O000O).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:59
def get_h5st_body (O00O00O0OO00OO0O0 ,OOOOOO0OOOOOOO0O0 ,O0O00OO0OOOOO0OOO ,O0O0OO00O0O0O00OO ,O0O00O0O0O00OO000 ):#line:60
    try :#line:61
        OOO0OOOO0OOO0OO00 =re .compile (r'pt_pin=(.*?);').findall (OOOOOO0OOOOOOO0O0 )[0 ]#line:62
        OOO0OOOO0OOO0OO00 =unquote_plus (OOO0OOOO0OOO0OO00 )#line:63
    except IndexError :#line:64
        OOO0OOOO0OOO0OO00 =re .compile (r'pin=(.*?);').findall (OOOOOO0OOOOOOO0O0 )[0 ]#line:65
        OOO0OOOO0OOO0OO00 =unquote_plus (OOO0OOOO0OOO0OO00 )#line:66
    OO0OOOOOO0O0O0000 =O00O00O0OO00OO0O0 .split (";")[2 ]#line:67
    O0O00O0O0O00OO000 ={"appId":O0O0OO00O0O0O00OO ,"appid":"activities_platform","ua":O00O00O0OO00OO0O0 ,"pin":OOO0OOOO0OOO0OO00 ,"functionId":O0O00OO0OOOOO0OOO ,"body":O0O00O0O0O00OO000 ,"clientVersion":OO0OOOOOO0O0O0000 , "client":"ios", "version":"4.4"}#line:68
    try :#line:69
        OOO0OOOO000O0O00O = ["aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAzL2FwaS9oNXN0"]#line:71
        OOO0OOOO000O0O00O =random .choice (OOO0OOOO000O0O00O )#line:72
        OO00000O0O000O00O =json .dumps (O0O00O0O0O00OO000 )#line:73
        OO0000000O0OO00O0 ={'Content-Type':'application/json'}#line:74
        O0O0OO0O0O0OO0O0O =requests .request ("POST",base64 .b64decode (OOO0OOOO000O0O00O .encode ('utf-8')).decode ('utf-8'),headers =OO0000000O0OO00O0 ,timeout =10 ,data =OO00000O0O000O00O ).json ()#line:75
        if O0O0OO0O0O0OO0O0O ['code']==200 :#line:76
            return O0O0OO0O0O0OO0O0O ['data']#line:77
        else :#line:78
            printf (OOOOOO0OOOOOOO0O0 ,f"调用远程h5st接口失败1")#line:79
            return #line:80
    except Exception as OO00OO0O0O000O00O :#line:81
        printf (OOOOOO0OOOOOOO0O0 ,f"调用远程h5st接口失败2:{OO00OO0O0O000O00O}")#line:82
        get_h5st_body (O00O00O0OO00OO0O0 ,OOOOOO0OOOOOOO0O0 ,O0O00OO0OOOOO0OOO ,O0O0OO00O0O0O00OO ,O0O00O0O0O00OO000 )#line:83
        return #line:84
def inviteFissionDrawPrize (O00O0OO0OO00O0O0O ,OO00O0OOO00000000 ,OO0O0OO00OO0O0OO0 ,O00O0O0O0O0OOO00O ,OO0O000000000OOOO ):#line:85
    O0O0O0O00OO0OOOO0 ="https://api.m.jd.com/api"#line:86
    O000OOOOOOO0OOO0O =get_h5st_body (O00O0OO0OO00O0O0O ,OO00O0OOO00000000 ,OO0O0OO00OO0O0OO0 ,O00O0O0O0O0OOO00O ,OO0O000000000OOOO )#line:87
    if not O000OOOOOOO0OOO0O :#line:88
        return #line:89
    OOOO0O0O0000O0000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O00O0OO0OO00O0O0O ,'Cookie':OO00O0OOO00000000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:90
    OOOO0000OO0O00O00 =requests .request ("POST",O0O0O0O00OO0OOOO0 ,headers =OOOO0O0O0000O0000 ,data =O000OOOOOOO0OOO0O )#line:91
    if OOOO0000OO0O00O00 .status_code ==200 :#line:92
        OOO0000O00OO0OO0O =OOOO0000OO0O00O00 .json ()#line:93
        if OOO0000O00OO0OO0O ['data']:#line:94
            return OOOO0000OO0O00O00 .status_code ,OOO0000O00OO0OO0O ['data']['prizeValue'],OOO0000O00OO0OO0O ['data']['rewardType']#line:95
        else :#line:96
            return OOOO0000OO0O00O00 .status_code ,OOOO0000OO0O00O00 .text #line:97
    else :#line:98
        printf (OO00O0OOO00000000 ,f"{OOOO0000OO0O00O00.status_code}")#line:99
        return OOOO0000OO0O00O00 .status_code ,OOOO0000OO0O00O00 .text #line:100
def inviteFissionReceive (O00OOO00000O00000 ,OOOOOO0OO0O000OOO ,OOO000O00O0O0OOO0 ,O00O0OOOO00000O00 ,O00000OO0OO0OOO0O ):#line:101
    O0OO0O0OO00OOOO00 ="https://api.m.jd.com/api"#line:102
    OOOO00OO0O0OO00O0 =get_h5st_body (O00OOO00000O00000 ,OOOOOO0OO0O000OOO ,OOO000O00O0O0OOO0 ,O00O0OOOO00000O00 ,O00000OO0OO0OOO0O )#line:103
    if not OOOO00OO0O0OO00O0 :#line:104
        return #line:105
    O0OOO0OOO0OO0OOOO ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O00OOO00000O00000 ,'Cookie':OOOOOO0OO0O000OOO ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:106
    O0OOOO0O0O00O00OO =requests .request ("POST",O0OO0O0OO00OOOO00 ,headers =O0OOO0OOO0OO0OOOO ,data =OOOO00OO0O0OO00O0 )#line:107
    if O0OOOO0O0O00O00OO .status_code ==200 :#line:108
        O00OO000OOOOOOOOO =O0OOOO0O0O00O00OO .json ()#line:109
        if O00OO000OOOOOOOOO ['data']:#line:110
            printf (OOOOOO0OO0O000OOO ,f"{O0OOOO0O0O00O00OO.status_code} {O00OO000OOOOOOOOO['data']}")#line:111
            return O00OO000OOOOOOOOO ['data']#line:112
        else :#line:113
            printf (OOOOOO0OO0O000OOO ,f"{O0OOOO0O0O00O00OO.status_code} {O00OO000OOOOOOOOO}")#line:114
            return O00OO000OOOOOOOOO #line:115
def superRedBagList (OOO00OO000OO00OOO ,OOO0OO000O0OOOOOO ,OO0O0O00O00000OO0 ,O0O00O00O0O0O0O0O ,OO0OOOOO0OOOO0O0O ):#line:116
    OO00O0O0O0OOOO00O ="https://api.m.jd.com/api"#line:117
    O0O0OO00OO0O0000O =get_h5st_body (OOO00OO000OO00OOO ,OOO0OO000O0OOOOOO ,OO0O0O00O00000OO0 ,O0O00O00O0O0O0O0O ,OO0OOOOO0OOOO0O0O )#line:118
    if not O0O0OO00OO0O0000O :#line:119
        return #line:120
    O000O0OOOOOO00OO0 ={"Accept":"application/json, text/plain, */*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Referer":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","X-Referer-Page":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","Origin":"https://pro.m.jd.com","x-rp-client":"h5_1.0.0","Cookie":OOO0OO000O0OOOOOO ,"User-Agent":OOO00OO000OO00OOO }#line:121
    OO0O0O0000O0O0OO0 =requests .request ("POST",OO00O0O0O0OOOO00O ,headers =O000O0OOOOOO00OO0 ,data =O0O0OO00OO0O0000O )#line:122
    if OO0O0O0000O0O0OO0 .status_code ==200 :#line:123
        O000000O0O0OO000O =OO0O0O0000O0O0OO0 .json ()#line:124
        if O000000O0O0OO000O ['data']:#line:125
            return O000000O0O0OO000O ['data']#line:126
        else :#line:127
            printf (OOO0OO000O0OOOOOO ,f"{OO0O0O0000O0O0OO0.status_code} {O000000O0O0OO000O}")#line:128
            return OO0O0O0000O0O0OO0 .text #line:129
    else :#line:130
        printf (OOO0OO000O0OOOOOO ,f"{OO0O0O0000O0O0OO0.status_code}")#line:131
        if OO0O0O0000O0O0OO0 .status_code == 403:
            printf(OOO0OO000O0OOOOOO, "提现接口403,退出！建议换ip后重试~")
            exit()
def apCashWithDraw (OO0OOOOO000OO00OO ,OO0O0O0O0O00O0000 ,OOOOOO0000O0OO00O ,OO0OO00O0O000OOO0 ,OOOOO0000OO000O0O ,activityId):#line:132
    OOOO000O0OOO0OO00 ="https://api.m.jd.com/"#line:133
    O0O0000OOOOO0OOOO ={"linkId":linkId ,"channel":"1","businessSource":"NONE","base":{"id":OO0O0O0O0O00O0000 ,"business":"fission","poolBaseId":OOOOOO0000O0OO00O ,"prizeGroupId":OO0OO00O0O000OOO0 ,"prizeBaseId":OOOOO0000OO000O0O ,"prizeType":4 ,"activityId":activityId}}#line:134
    OOOO000O00O0OO000 =get_h5st_body (ua ,OO0OOOOO000OO00OO ,"apCashWithDraw","8c6ae",O0O0000OOOOO0OOOO )#line:135
    if not OOOO000O00O0OO000 :#line:136
        return #line:137
    O0OO00O0OOOO0OOOO ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OO0OOOOO000OO00OO ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:138
    O0O0O0OOOO0OOO0OO =requests .request ("POST",OOOO000O0OOO0OO00 ,headers =O0OO00O0OOOO0OOOO ,data =OOOO000O00O0OO000 )#line:139
    if O0O0O0OOOO0OOO0OO .status_code ==200 :#line:140
        OOO00OOO00000OO00 =O0O0O0OOOO0OOO0OO .json ()#line:141
        if OOO00OOO00000OO00 ['data']:#line:142
            return OOO00OOO00000OO00 ['data']['message']#line:143
        else :#line:144
            printf (OO0OOOOO000OO00OO ,f"{O0O0O0OOOO0OOO0OO.status_code} {OOO00OOO00000OO00}")#line:145
def apRecompenseDrawPrize (OOOOO00000OOO0OO0 ,OO00O0O0O0O0000O0 ,O0OO0OO0000O00O0O ,OOOO0000000OO0O00 ,O0O0OOO000O0O000O ):#line:146
    O0O0O0000OOO0000O ="https://api.m.jd.com/"#line:147
    OOO00O0OOOOO0O0O0 ={"linkId":linkId ,"drawRecordId":OO00O0O0O0O0000O0 ,"business":"fission","poolId":O0OO0OO0000O00O0O ,"prizeGroupId":OOOO0000000OO0O00 ,"prizeId":O0O0OOO000O0O000O ,}#line:148
    OOOOO0O0O0OO00O00 =get_h5st_body (ua ,OOOOO00000OOO0OO0 ,"apRecompenseDrawPrize","8c6ae",OOO00O0OOOOO0O0O0 )#line:149
    if not OOOOO0O0O0OO00O00 :#line:150
        return #line:151
    O0OOOO0OO0O00000O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OOOOO00000OOO0OO0 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:152
    O00O0000O000OOOOO =requests .request ("POST",O0O0O0000OOO0000O ,headers =O0OOOO0OO0O00000O ,data =OOOOO0O0O0OO00O00 )#line:153
    if O00O0000O000OOOOO .status_code ==200 :#line:154
        O0OO0000OOO0OO000 =O00O0000O000OOOOO .json ()#line:155
        if O0OO0000OOO0OO000 ['data']:#line:156
            return "兑换红包成功"#line:157
        else :#line:158
            printf (OOOOO00000OOO0OO0 ,f"{O00O0000O000OOOOO.status_code} {O0OO0000OOO0OO000}")#line:159
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
        cookie_ =[OO00OOO00OOO0000O for OO00OOO00OOO0000O in cks if inviteDrawPin in OO00OOO00OOO0000O ]#line:173
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
            time .sleep (1.5 )#line:237
    print (f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(O00OO000OO0000OOO) for O00OO000OO0000OOO in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(OOO000000OO0OOO00) for OOO000000OO0OOO00 in redpacket]))}元红包,开始提现****************\n")#line:240
    print (f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置****************")#line:242
    for index ,linkId in enumerate (linkIds ,1 ):#line:243
        i =0 #line:244
        while True :#line:245
            print (f"\n开始获取第{i + 1}页奖励列表\n")#line:246
            body ={"pageNum":i ,"pageSize":400 ,"linkId":linkId ,"associateLinkId":"","business":"fission","prizeTypeLists":[7]}#line:247
            info =superRedBagList (ua ,cookie ,"superRedBagList","f2b1d",body )#line:248
            if not info :#line:249
                print ("等待10s重新获取")#line:250
                time .sleep (10 )#line:251
                continue #line:252
            i +=1 #line:253
            items =info ['items']#line:254
            if not items :#line:255
                printf (cookie ,"全部提现完成！")#line:256
                break #line:257
            for item in items :#line:258
                id =item ['id']#line:260
                amount =item ['amount']#line:261
                prizeType =item ['prizeType']#line:262
                state =item ['state']#line:263
                prizeConfigName =item ['prizeConfigName']#line:264
                prizeGroupId =item ['prizeGroupId']#line:265
                poolBaseId =item ['poolBaseId']#line:266
                prizeBaseId =item ['prizeBaseId']#line:267
                activityId =item ['activityId']#line:268
                if prizeType == 4 and state != 3 and state != 4 and state != -1 :#line:268
                    cashInfo =apCashWithDraw (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId ,activityId)#line:269
                    if cashInfo :#line:270
                        printf (cookie ,f"{amount}现金 {cashInfo}")#line:271
                        if "上限"in cashInfo or "其他pin"in cashInfo or "其它pin"in cashInfo :#line:272
                            cashInfo =apRecompenseDrawPrize (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:273
                            printf (cookie ,f"{amount}现金 {cashInfo}")#line:274
                    time .sleep (2 )#line:275
                else :#line:276
                    continue #line:277
            time .sleep (1 )#line:279
            if i >=apCashPageSize :#line:281
                break