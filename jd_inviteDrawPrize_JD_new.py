#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
File: jd_inviteDrawPrize_JD.py(转赚邀好友抽奖提现JD新版)
Author: HarbourJ
Date: 2023/3/15 10:00
TG: https://t.me/HarbourToulu
cron: 30 0 1,12,21 * * *
new Env('转赚邀好友抽奖提现JD新版');
ActivityEntry: https://pro.m.jd.com/mall/active/B2Y13x641hwWfpsoRenCzfbz4jR/index.html?inviterId=Q2VzHk9dkShW66_of58y-g&channelType=0&femobile=femobile&activityChannel=jdapp
变量：export inviteDrawPin="车头pin"
     export apCashPageSize="提现的最大页数"
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

apCashPageSize = int(os.environ.get("apCashPageSize")) if os.environ.get("apCashPageSize") else 5 #line:22
linkIds =['wDNvX5t2N52cWEM8cLOa0g']#line:23
baseJdUrl ="https://api.m.jd.com/api"#line:24
activityUrl ="https://pro.m.jd.com/mall/active/B2Y13x641hwWfpsoRenCzfbz4jR/index.html"#line:25
def getJdTime ():#line:27
    OO00OO0OOO0O0O0OO =int (round (time .time ()*1000 ))#line:28
    return OO00OO0OOO0O0O0OO #line:29
def printf (OO00O00O0O000OOOO ,OOO00O0000OO0O000 ):#line:31
    try :#line:32
        OO00000O00O000OOO =re .compile (r'pt_pin=(.*?);').findall (OO00O00O0O000OOOO )[0 ]#line:33
        OO00000O00O000OOO =unquote_plus (OO00000O00O000OOO )#line:34
    except IndexError :#line:35
        OO00000O00O000OOO =re .compile (r'pin=(.*?);').findall (OO00O00O0O000OOOO )[0 ]#line:36
        OO00000O00O000OOO =unquote_plus (OO00000O00O000OOO )#line:37
    print (f"{str(datetime.now())[0:22]}->{OO00000O00O000OOO}->{OOO00O0000OO0O000}")#line:38
def base64Encode (OOO00OOO0OO0O00O0 ):#line:40
    O0O00OOOOO000OO0O =""#line:41
    OOO000OOO0OO00000 =[]#line:42
    O0OO0OO000OO00O00 =""#line:43
    OO0OOOO0O00O0OO00 ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:44
    for OO0O0O0O0O0OO0OOO in OOO00OOO0OO0O00O0 :#line:45
        O0O00OOOOO000OO0O +="{:08}".format (int (str (bin (ord (OO0O0O0O0O0OO0OOO ))).replace ("0b","")))#line:46
    for O0O00O000O00OO0OO in range (0 ,len (O0O00OOOOO000OO0O ),6 ):#line:47
        OOO000OOO0OO00000 .append ("{:<06}".format (O0O00OOOOO000OO0O [O0O00O000O00OO0OO :O0O00O000O00OO0OO +6 ]))#line:48
    for O0OOOO0OO0O0OOOOO in OOO000OOO0OO00000 :#line:49
        O0OO0OO000OO00O00 =O0OO0OO000OO00O00 +OO0OOOO0O00O0OO00 [int (O0OOOO0OO0O0OOOOO ,2 )]#line:50
    if len (O0OO0OO000OO00O00 )%4 ==2 :#line:51
        O0OO0OO000OO00O00 +="=="#line:52
    elif len (O0OO0OO000OO00O00 )%4 ==3 :#line:53
        O0OO0OO000OO00O00 +="="#line:54
    return O0OO0OO000OO00O00 #line:55
def userAgent ():#line:57
    import uuid #line:58
    OO0OOOOO0OOOOO0OO ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:73
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(OO0OOOOO0OOOOO0OO).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:74
def get_h5st_body (OO0O0000OO000OO0O ,O0OO00O0O0O00OOO0 ,O0OO0O00O0O0OO0OO ,OO00O0O0OOO000OOO ,OOOOOOOOOO000OO0O ,O000000OOO000O00O ):#line:76
    try :#line:77
        O0000OOO0O00OOOO0 =re .compile (r'pt_pin=(.*?);').findall (O0OO00O0O0O00OOO0 )[0 ]#line:78
        O0000OOO0O00OOOO0 =unquote_plus (O0000OOO0O00OOOO0 )#line:79
    except IndexError :#line:80
        O0000OOO0O00OOOO0 =re .compile (r'pin=(.*?);').findall (O0OO00O0O0O00OOO0 )[0 ]#line:81
        O0000OOO0O00OOOO0 =unquote_plus (O0000OOO0O00OOOO0 )#line:82
    OOO0O00O00O000O0O =OO0O0000OO000OO0O .split (";")[2 ]#line:83
    OOOOOOOOOO000OO0O ={"appId":OO00O0O0OOO000OOO ,"appid":"activities_platform","ua":OO0O0000OO000OO0O ,"pin":O0000OOO0O00OOOO0 ,"functionId":O0OO0O00O0O0OO0OO ,"body":OOOOOOOOOO000OO0O ,"clientVersion":OOO0O00O00O000O0O ,"client":"ios","version":O000000OOO000O00O ,"t":True }#line:95
    try :#line:96
        import base64 #line:97
        O0000OO000OO0O0O0 =["aHR0cDovLzEuOTQuMTY4Ljg0OjMwMDkvYXBpL2g1c3Q="]#line:98
        OO00OO00000OOOOO0 =random .choice (O0000OO000OO0O0O0 )#line:99
        O0O00O0O0O0O00O0O =json .dumps (OOOOOOOOOO000OO0O )#line:100
        O000OO0O0OOOOOO00 ={'Content-Type':'application/json'}#line:103
        OOO00O000O000OO00 =requests .request ("POST",base64 .b64decode (OO00OO00000OOOOO0 .encode ('utf-8')).decode ('utf-8'),headers =O000OO0O0OOOOOO00 ,timeout =10 ,data =O0O00O0O0O0O00O0O ).json ()#line:104
        if OOO00O000O000OO00 ['code']==200 :#line:105
            return OOO00O000O000OO00 ['data']#line:107
        else :#line:108
            printf (O0OO00O0O0O00OOO0 ,f"调用远程h5st接口失败1")#line:109
            return #line:110
    except Exception as O0O000O0O0OO00O00 :#line:111
        printf (O0OO00O0O0O00OOO0 ,f"调用远程h5st接口失败2:{O0O000O0O0OO00O00}")#line:112
        get_h5st_body (OO0O0000OO000OO0O ,O0OO00O0O0O00OOO0 ,O0OO0O00O0O0OO0OO ,OO00O0O0OOO000OOO ,OOOOOOOOOO000OO0O ,O000000OOO000O00O )#line:113
        return #line:114
def inviteFissionDrawPrize (OOOOO000O0000OOO0 ,O0OOOOOOOOO00O000 ,O00OOO0O0OO0O0000 ,OOO000OO000OOO000 ,OO00OO0OOO000OO00 ):#line:116
    OOOO00000000OO0O0 =get_h5st_body (OOOOO000O0000OOO0 ,O0OOOOOOOOO00O000 ,O00OOO0O0OO0O0000 ,OOO000OO000OOO000 ,OO00OO0OOO000OO00 ,"4.7")#line:117
    if not OOOO00000000OO0O0 :#line:118
        return #line:119
    O000O00O00O00O0O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OOOOO000O0000OOO0 ,'Cookie':O0OOOOOOOOO00O000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:131
    O00OO0O0000O0O0OO =requests .request ("POST",baseJdUrl ,headers =O000O00O00O00O0O0 ,data =OOOO00000000OO0O0 )#line:132
    if O00OO0O0000O0O0OO .status_code ==200 :#line:133
        try :#line:134
            O0000OOO000O0OO00 =O00OO0O0000O0O0OO .json ()#line:135
            if O0000OOO000O0OO00 ['data']:#line:136
                return O00OO0O0000O0O0OO .status_code ,O0000OOO000O0OO00 ['data']['prizeValue'],O0000OOO000O0OO00 ['data']['rewardType']#line:137
            else :#line:138
                return O00OO0O0000O0O0OO .status_code ,O00OO0O0000O0O0OO .text #line:139
        except Exception as OOOO0O0O0O00OOOOO :#line:140
            printf (O0OOOOOOOOO00O000 ,f"{O00OO0O0000O0O0OO.text}")#line:141
            exit ()#line:142
    else :#line:143
        printf (O0OOOOOOOOO00O000 ,f"{O00OO0O0000O0O0OO.status_code}")#line:144
        return O00OO0O0000O0O0OO .status_code ,O00OO0O0000O0O0OO .text #line:145
def inviteFissionReceive (OOO0O0O0000O00O0O ,OO0O000OOOOO00O0O ,OO0O0000O0OOOO0OO ,O0O0OO000OO0OO0O0 ,O00OO0O00O0000OOO ):#line:147
    OO0O00000O0O0OO0O =get_h5st_body (OOO0O0O0000O00O0O ,OO0O000OOOOO00O0O ,OO0O0000O0OOOO0OO ,O0O0OO000OO0OO0O0 ,O00OO0O00O0000OOO ,"4.7")#line:148
    if not OO0O00000O0O0OO0O :#line:149
        return #line:150
    OO0O00000O0O0OO0O =OO0O00000O0O0OO0O +"&loginType=2&loginWQBiz=wegame&&x-api-eid-token=&uuid=-1"#line:151
    O0O0OOO0O0OOO0O00 ={'Host':'api.m.jd.com','Accept':'application/json, text/plain, */*','x-rp-client':'h5_1.0.0','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded','User-Agent':OOO0O0O0000O00O0O ,'Cookie':OO0O000OOOOO00O0O ,'Origin':'https://pro.m.jd.com','x-referer-page':activityUrl ,'Referer':activityUrl }#line:164
    OOO00O0O0O000000O =requests .request ("POST",baseJdUrl +"?functionId=inviteFissionReceive",headers =O0O0OOO0O0OOO0O00 ,data =OO0O00000O0O0OO0O )#line:165
    if OOO00O0O0O000000O .status_code ==200 :#line:166
        O0OO00000OO0O000O =OOO00O0O0O000000O .json ()#line:167
        if O0OO00000OO0O000O ['data']:#line:168
            return O0OO00000OO0O000O ['data']#line:170
        else :#line:171
            printf (OO0O000OOOOO00O0O ,f"{OOO00O0O0O000000O.status_code} {O0OO00000OO0O000O}")#line:172
            return O0OO00000OO0O000O #line:173
def superRedBagList (OOO00OO000OOO00OO ,OO0OOOOOO0O0OOOO0 ,OO0O00O0OOOO0O0O0 ,O0O0OOO0O0O0OO0OO ,O0O0OO00OO00OO000 ):#line:175
    OOOOO00OO000O000O =get_h5st_body (OOO00OO000OOO00OO ,OO0OOOOOO0O0OOOO0 ,OO0O00O0OOOO0O0O0 ,O0O0OOO0O0O0OO0OO ,O0O0OO00OO00OO000 ,"4.7")#line:176
    if not OOOOO00OO000O000O :#line:177
        return #line:178
    OOOOO00OO000O000O =OOOOO00OO000O000O +"&loginType=2&loginWQBiz=wegame&&x-api-eid-token=&uuid=-1"#line:179
    O000OOO00O00OO0OO ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OOO00OO000OOO00OO ,'Cookie':OO0OOOOOO0O0OOOO0 ,'Host':'api.m.jd.com','Referer':activityUrl ,'X-Referer-Page':activityUrl ,'X-Rp-Client':'h5_1.0.0','Origin':'https://pro.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:193
    try :#line:194
        from curl_cffi import requests #line:195
    except ImportError as OOOOO0OOO0O000O0O :#line:196
        if "No module"in str (OOOOO0OOO0O000O0O ):#line:197
            os .system ("pip install curl_cffi")#line:198
        from curl_cffi import requests #line:199
    O00000OO00OO00OO0 =requests .request ("POST",baseJdUrl ,impersonate ="chrome124",headers =O000OOO00O00OO0OO ,data =OOOOO00OO000O000O )#line:200
    if O00000OO00OO00OO0 .status_code ==200 :#line:202
        OO00O0O000000OO00 =O00000OO00OO00OO0 .json ()#line:203
        try :#line:204
            if OO00O0O000000OO00 ['data']:#line:205
                return OO00O0O000000OO00 ['data']#line:206
            else :#line:207
                printf (OO0OOOOOO0O0OOOO0 ,f"{O00000OO00OO00OO0.status_code} {OO00O0O000000OO00}")#line:208
                printf (OO0OOOOOO0O0OOOO0 ,f"{O00000OO00OO00OO0.status_code} {OO00O0O000000OO00}")#line:209
                return O00000OO00OO00OO0 .text #line:210
        except Exception as OOOOO0OOO0O000O0O :#line:211
            printf (OO0OOOOOO0O0OOOO0 ,f"{O00000OO00OO00OO0.text}")#line:212
            exit ()#line:213
    else :#line:214
        printf (OO0OOOOOO0O0OOOO0 ,f"{O00000OO00OO00OO0.status_code}")#line:215
        if O00000OO00OO00OO0 .status_code ==403 :#line:216
            printf (OO0OOOOOO0O0OOOO0 ,"提现接口403 退出！")#line:217
            exit ()#line:218
def apCashWithDraw (O0O0OO00O0OOO0O0O ,OO0OOO0OOO0O00O00 ,OOOO00OOOO000O0OO ,O000OOOOO00OO0000 ,O0OO00O0OO0OO0OO0 ,OOOOO00O0OO00OO0O ):#line:220
    OOO0O000O000OOO0O ="https://api.m.jd.com/"#line:222
    O00000O0O000OO0O0 ={"linkId":linkId ,"channel":"1","businessSource":"NONE","base":{"id":OO0OOO0OOO0O00O00 ,"business":"fission","poolBaseId":OOOO00OOOO000O0OO ,"prizeGroupId":O000OOOOO00OO0000 ,"prizeBaseId":O0OO00O0OO0OO0OO0 ,"prizeType":4 ,"activityId":OOOOO00O0OO00OO0O }}#line:236
    OO00OOOO0O0O0O0OO =get_h5st_body (ua ,O0O0OO00O0OOO0O0O ,"apCashWithDraw","8c6ae",O00000O0O000OO0O0 ,"4.7")#line:237
    if not OO00OOOO0O0O0O0OO :#line:238
        return #line:239
    O0O000OO00OO00O0O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O0O0OO00O0OOO0O0O ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:251
    O0OO0O00O00O00OOO =requests .request ("POST",OOO0O000O000OOO0O ,headers =O0O000OO00OO00O0O ,data =OO00OOOO0O0O0O0OO )#line:252
    if O0OO0O00O00O00OOO .status_code ==200 :#line:253
        OO0OOO00OO0000OO0 =O0OO0O00O00O00OOO .json ()#line:254
        if OO0OOO00OO0000OO0 ['data']:#line:255
            return OO0OOO00OO0000OO0 ['data']['message']#line:256
        else :#line:257
            printf (O0O0OO00O0OOO0O0O ,f"{O0OO0O00O00O00OOO.status_code} {OO0OOO00OO0000OO0}")#line:258
def apRecompenseDrawPrize (OOOOOO000OO00O00O ,OOOOOO0OO0O0O0O00 ,O0OOOOOO00000O00O ,O000OO000O0OO0O0O ,OO0OO0O0000OO0OO0 ):#line:260
    OO000O0OOO000O0OO ="https://api.m.jd.com/"#line:261
    OO0O0OO00OOO00OO0 ={"linkId":linkId ,"drawRecordId":OOOOOO0OO0O0O0O00 ,"business":"fission","poolId":O0OOOOOO00000O00O ,"prizeGroupId":O000OO000O0OO0O0O ,"prizeId":OO0OO0O0000OO0OO0 ,}#line:268
    OOOOO0OOOO00OO0O0 =get_h5st_body (ua ,OOOOOO000OO00O00O ,"apRecompenseDrawPrize","8c6ae",OO0O0OO00OOO00OO0 ,"4.7")#line:269
    if not OOOOO0OOOO00OO0O0 :#line:270
        return #line:271
    O000000O0OOO0000O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OOOOOO000OO00O00O ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:283
    O0O0OOO000OO00OO0 =requests .request ("POST",OO000O0OOO000O0OO ,headers =O000000O0OOO0000O ,data =OOOOO0OOOO00OO0O0 )#line:284
    if O0O0OOO000OO00OO0 .status_code ==200 :#line:285
        OOO0O00O00O0OOOOO =O0O0OOO000OO00OO0 .json ()#line:286
        if OOO0O00O00O0OOOOO ['data']:#line:287
            return "兑换红包成功"#line:289
        else :#line:290
            printf (OOOOOO000OO00O00O ,f"{O0O0OOO000OO00OO0.status_code} {OOO0O00O00O0OOOOO}")#line:291
if __name__ =='__main__':#line:294
    try :#line:295
        cks =getCk #line:296
        if not cks :#line:297
            sys .exit ()#line:298
    except :#line:299
        print ("未获取到有效COOKIE,退出程序！")#line:300
        sys .exit ()#line:301
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:302
    if inviteDrawPin :#line:303
        cookie_ =[O0O00OO00O000O000 for O0O00OO00O000O000 in cks if inviteDrawPin in O0O00OO00O000O000 ]#line:304
        if cookie_ :#line:305
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:306
            cookie =cookie_ [0 ]#line:307
        else :#line:308
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:309
            sys .exit ()#line:310
    else :#line:311
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:312
        cookie =cks [0 ]#line:313
    ua =userAgent ()#line:314
    cash =[]#line:315
    successful =[]#line:316
    total =0 #line:317
    i =0 #line:318
    redpacket =[]#line:319
    for index ,linkId in enumerate (linkIds ,1 ):#line:321
        while True :#line:322
            try :#line:323
                info =inviteFissionDrawPrize (ua ,cookie ,"inviteFissionDrawPrize","c02c6",{"linkId":linkId })#line:324
                if "活动太火爆"in str (info ):#line:325
                    printf (cookie ,info )#line:326
                    time .sleep (3 )#line:327
                    continue #line:328
            except Exception as e :#line:329
                printf (cookie ,e )#line:330
                time .sleep (3 )#line:331
                continue #line:332
            if not info :#line:333
                time .sleep (3 )#line:334
                continue #line:335
            if not info [1 ]:#line:336
                time .sleep (10 )#line:337
                continue #line:338
            elif "抽奖次数已用完"in info [1 ]:#line:339
                printf (cookie ,f"{info[0]} ⚠️抽奖次数已用完")#line:340
                break #line:341
            elif "本场活动已结束"in info [1 ]:#line:342
                printf (cookie ,f"{info[0]} ⏰本场活动已结束了,快去重新开始吧")#line:343
                break #line:344
            else :#line:345
                if info :#line:346
                    total +=1 #line:347
                    if info [2 ]==1 :#line:348
                        printf (cookie ,f"{info[0]} 🎫获得{info[1]}优惠券")#line:349
                    elif info [2 ]==2 :#line:350
                        printf (cookie ,f"{info[0]} 🧧获得{info[1]}红包")#line:351
                        redpacket .append (info [1 ])#line:352
                    else :#line:353
                        printf (cookie ,f"{info[0]} 💵获得{info[1]}现金")#line:354
                        cash .append (info [1 ])#line:355
            # time .sleep (0.5 )#line:356
            # info =inviteFissionReceive (ua ,cookie ,"inviteFissionReceive","b8469",{"linkId":linkId })#line:358
            # if "火爆"in str (info ):#line:359
            #     printf (cookie ,f"{info['errMsg']}")#line:360
            #     time .sleep (3 )#line:361
            #     continue #line:362
            # amount_all =info ['amount']#line:363
            # totalAmount =info ['totalAmount']#line:364
            # leftAmount =info ['leftAmount']#line:365
            # if info ['receiveList']:#line:366
            #     msg ='💰领现金'#line:367
            #     amount =info ['receiveList'][0 ]['amount']#line:368
            #     printf (cookie ,f"{msg}{amount}, 进度{amount_all}/{totalAmount}")#line:369
            #     if str (leftAmount )=="0.00":#line:370
            #         break #line:371
            # else :#line:372
            #     msg ='❌提现金失败'#line:373
            #     printf (cookie ,f"{msg}")#line:374
            time .sleep (3 )#line:376
    print (f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(OO0OO0O00O000OO0O) for OO0OO0O00O000OO0O in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(OOO000OO00O0OO0OO) for OOO000OO00O0OO0OO in redpacket]))}元红包,开始提现****************\n")#line:378
    print (f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置apCashPageSize变量****************")#line:380
    cashSuccess =0 #line:381
    cashFail =0 #line:382
    for index ,linkId in enumerate (linkIds ,1 ):#line:383
        i =0 #line:384
        while True :#line:385
            print (f"\n开始获取第{i + 1}页奖励列表\n")#line:386
            body ={"pageNum":i ,"pageSize":400 ,"linkId":linkId ,"associateLinkId":"","business":"fission","prizeTypeLists":[7 ]}#line:387
            info =superRedBagList (ua ,cookie ,"superRedBagList","f2b1d",body )#line:388
            if not info :#line:389
                print ("等待10s重新获取")#line:390
                time .sleep (10 )#line:391
                continue #line:392
            i +=1 #line:393
            items =info ['items']#line:394
            if not items :#line:395
                printf (cookie ,"全部提现完成！")#line:396
                break #line:397
            for item in items :#line:398
                id =item ['id']#line:400
                amount =item ['amount']#line:401
                prizeType =item ['prizeType']#line:402
                state =item ['state']#line:403
                prizeConfigName =item ['prizeConfigName']#line:404
                prizeGroupId =item ['prizeGroupId']#line:405
                poolBaseId =item ['poolBaseId']#line:406
                prizeBaseId =item ['prizeBaseId']#line:407
                activityId =item ['activityId']#line:408
                if prizeType ==4 and state !=3 and state !=4 and state !=-1 :#line:409
                    cashInfo =apCashWithDraw (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId ,activityId )#line:410
                    if cashInfo :#line:411
                        printf (cookie ,f"{amount}现金 {cashInfo}")#line:412
                        if cashInfo =="提现中":#line:413
                            cashSuccess +=float (amount )#line:414
                        else :#line:415
                            cashFail +=float (amount )#line:416
                        if "上限"in cashInfo or "其他pin"in cashInfo or "其它pin"in cashInfo :#line:417
                            cashInfo =apRecompenseDrawPrize (cookie ,id ,poolBaseId ,prizeGroupId ,prizeBaseId )#line:418
                            printf (cookie ,f"{amount}现金 {cashInfo}")#line:419
                    time .sleep (10 )#line:420
                else :#line:421
                    continue #line:422
            time .sleep (3 )#line:424
            if i >=apCashPageSize :#line:426
                break #line:427
    print (f"\n****************提现结束,成功提现💵{round(cashSuccess, 2)}元现金,剩余待提现💵{round(cashFail, 2)}元现金****************")