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

import time, requests, sys, re, os, json, random
from urllib.parse import quote_plus, unquote_plus, quote
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    from jd_sign import *
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")
    sys.exit()
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

apCashPageSize = 20  # 提现的最大页数，可根据实际情况修改
linkIds = ['Wvzc_VpNTlSkiQdHT8r7QA']
activityUrl = "https://prodev.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html"


def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def printf(cookie, T):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    print(f"{str(datetime.now())[0:22]}->{pt_pin}->{T}")

def base64Encode (OOOOO00O0O0000OOO ):#line:1
    O00O00OOOO000O0O0 =""#line:2
    O00000OOO0OOO0OOO =[]#line:3
    OO00O0OO0OOOOOO00 =""#line:4
    O00O0OOO0000OO0O0 ='KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'#line:5
    for OO0O0OOOO00OOO0OO in OOOOO00O0O0000OOO :#line:6
        O00O00OOOO000O0O0 +="{:08}".format (int (str (bin (ord (OO0O0OOOO00OOO0OO ))).replace ("0b","")))#line:7
    for O00O0OOOOO0O0O00O in range (0 ,len (O00O00OOOO000O0O0 ),6 ):#line:8
        O00000OOO0OOO0OOO .append ("{:<06}".format (O00O00OOOO000O0O0 [O00O0OOOOO0O0O00O :O00O0OOOOO0O0O00O +6 ]))#line:9
    for O0000OO0000OOO000 in O00000OOO0OOO0OOO :#line:10
        OO00O0OO0OOOOOO00 =OO00O0OO0OOOOOO00 +O00O0OOO0000OO0O0 [int (O0000OO0000OOO000 ,2 )]#line:11
    if len (OO00O0OO0OOOOOO00 )%4 ==2 :#line:12
        OO00O0OO0OOOOOO00 +="=="#line:13
    elif len (OO00O0OO0OOOOOO00 )%4 ==3 :#line:14
        OO00O0OO0OOOOOO00 +="="#line:15
    return OO00O0OO0OOOOOO00 #line:16
def userAgent ():#line:18
    import uuid #line:19
    O0O0O00O0O0OO0O00 ={"ciphertype":5 ,"cipher":{"ud":base64Encode (''.join (random .sample ('0123456789abcdef0123456789abcdef0123456789abcdef',40 ))),"sv":"CJSkDy42","iad":base64Encode (str (uuid .uuid1 (uuid .getnode ())).upper ())},"ts":int (time .time ()),"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1 }#line:34
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(O0O0O00O0O0OO0O00).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"#line:35
def get_h5st_body (OO0O000OOO0OO00O0 ,OO00OOOO0O00OO0O0 ,OOOOO0OOOOOOOOOO0 ,OO0O000OOOOO0O0OO ,O000OOOOOO0OO0OO0 ):#line:37
    try :#line:38
        OOOOO0OOOO00OO0O0 =re .compile (r'pt_pin=(.*?);').findall (OO00OOOO0O00OO0O0 )[0 ]#line:39
        OOOOO0OOOO00OO0O0 =unquote_plus (OOOOO0OOOO00OO0O0 )#line:40
    except IndexError :#line:41
        OOOOO0OOOO00OO0O0 =re .compile (r'pin=(.*?);').findall (OO00OOOO0O00OO0O0 )[0 ]#line:42
        OOOOO0OOOO00OO0O0 =unquote_plus (OOOOO0OOOO00OO0O0 )#line:43
    O0OOO00OOOO00O0O0 =OO0O000OOO0OO00O0 .split (";")[2 ]#line:44
    O000OOOOOO0OO0OO0 ={"appId":OO0O000OOOOO0O0OO ,"appid":"activities_platform","ua":OO0O000OOO0OO00O0 ,"pin":OOOOO0OOOO00OO0O0 ,"functionId":OOOOO0OOOOOOOOOO0 ,"body":O000OOOOOO0OO0OO0 ,"expand":{"url":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","og":"https://pro.m.jd.com"},"clientVersion":O0OOO00OOOO00O0O0 ,"version":"4.1"}#line:58
    try :#line:59
        import base64
        O000OOO0OOO0O00O0 = ["aHR0cDovLzEuOTQuOC4yNDQ6MzAwMS9hcGkvaDVzdA==","aHR0cDovL2hhcmJvdXJqLmNmOjMwMDEvYXBpL2g1c3Q=","aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAxL2FwaS9oNXN0"] #line:60
        O000OOO0OOO0O00O0 = random.choice(O000OOO0OOO0O00O0)
        O0OO000O0OOO0OO00 =json .dumps (O000OOOOOO0OO0OO0 )#line:61
        OOO00O0000000OOOO ={'Content-Type':'application/json'}#line:64
        O0OO00OO00OO0O00O =requests .request ("POST",base64 .b64decode (O000OOO0OOO0O00O0 .encode ('utf-8')).decode ('utf-8') ,headers =OOO00O0000000OOOO ,timeout =10 ,data =O0OO000O0OOO0OO00 ).json ()#line:65
        if O0OO00OO00OO0O00O ['code']==200 :#line:66
            return O0OO00OO00OO0O00O ['data']#line:68
        else :#line:69
            printf (OO00OOOO0O00OO0O0 ,f"调用远程h5st接口失败1")#line:70
            return #line:71
    except Exception as OO00OOO0O000OOO0O :#line:72
        printf (OO00OOOO0O00OO0O0 ,f"调用远程h5st接口失败2:{OO00OOO0O000OOO0O}")#line:73
        get_h5st_body (OO0O000OOO0OO00O0 ,OO00OOOO0O00OO0O0 ,OOOOO0OOOOOOOOOO0 ,OO0O000OOOOO0O0OO ,O000OOOOOO0OO0OO0 )#line:74
        return #line:75
def inviteFissionDrawPrize (OOOO0O00O0O0O000O ,O00O00OO0O0000O00 ,O0000OOOOO0OOOO0O ,O000OOOO00000OOOO ,O0O0OO0OOO0000000 ):#line:77
    O0OO0OOO00O000OO0 ="https://api.m.jd.com/api"#line:78
    O000O0O00O000OOOO =get_h5st_body (OOOO0O00O0O0O000O ,O00O00OO0O0000O00 ,O0000OOOOO0OOOO0O ,O000OOOO00000OOOO ,O0O0OO0OOO0000000 )#line:79
    if not O000O0O00O000OOOO :#line:80
        return #line:81
    OO00OO0O00O0OO000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OOOO0O00O0O0O000O ,'Cookie':O00O00OO0O0000O00 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:93
    OO0OO00O0O0OO000O =requests .request ("POST",O0OO0OOO00O000OO0 ,headers =OO00OO0O00O0OO000 ,data =O000O0O00O000OOOO )#line:94
    if OO0OO00O0O0OO000O .status_code ==200 :#line:95
        OOOO0O00OO0OOOO00 =OO0OO00O0O0OO000O .json ()#line:96
        if OOOO0O00OO0OOOO00 ['data']:#line:97
            return OO0OO00O0O0OO000O .status_code ,OOOO0O00OO0OOOO00 ['data']['prizeValue'],OOOO0O00OO0OOOO00 ['data']['rewardType']#line:98
        else :#line:99
            return OO0OO00O0O0OO000O .status_code ,OO0OO00O0O0OO000O .text #line:100
    else :#line:101
        printf (O00O00OO0O0000O00 ,f"{OO0OO00O0O0OO000O.status_code}")#line:102
        return OO0OO00O0O0OO000O .status_code ,OO0OO00O0O0OO000O .text #line:103
def inviteFissionReceive (OO00O00OOOOOOO0OO ,OOO00OOOOOOOOO0OO ,O00OOO0OO0OOOO0O0 ,O0OO000O000OO0O00 ,O0O0O0O000O0O0O00 ):#line:105
    OO0OOO00O0OO00OOO ="https://api.m.jd.com/api"#line:106
    O00O000OO0000000O =get_h5st_body (OO00O00OOOOOOO0OO ,OOO00OOOOOOOOO0OO ,O00OOO0OO0OOOO0O0 ,O0OO000O000OO0O00 ,O0O0O0O000O0O0O00 )#line:107
    if not O00O000OO0000000O :#line:108
        return #line:109
    OOOOOO000O0000000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OO00O00OOOOOOO0OO ,'Cookie':OOO00OOOOOOOOO0OO ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:121
    OO0O000O0O0000000 =requests .request ("POST",OO0OOO00O0OO00OOO ,headers =OOOOOO000O0000000 ,data =O00O000OO0000000O )#line:122
    if OO0O000O0O0000000 .status_code ==200 :#line:123
        O000OO000O00O0000 =OO0O000O0O0000000 .json ()#line:124
        if O000OO000O00O0000 ['data']:#line:125
            printf (OOO00OOOOOOOOO0OO ,f"{OO0O000O0O0000000.status_code} {O000OO000O00O0000['data']}")#line:126
            return O000OO000O00O0000 ['data']#line:127
        else :#line:128
            printf (OOO00OOOOOOOOO0OO ,f"{OO0O000O0O0000000.status_code} {O000OO000O00O0000}")#line:129
            return O000OO000O00O0000 #line:130
def superRedBagList (O0OO0O000O00O00OO ,OOOO0OOO0000O00O0 ,O00OOOOO0O0OO0OOO ,O0O0O00O0OO00O00O ,O000O00O000OOO000 ):#line:132
    OO0OOOOO00000O0O0 ="https://api.m.jd.com/api"#line:133
    OO0O00OO0O0O00O0O =get_h5st_body (O0OO0O000O00O00OO ,OOOO0OOO0000O00O0 ,O00OOOOO0O0OO0OOO ,O0O0O00O0OO00O00O ,O000O00O000OOO000 )#line:134
    if not OO0O00OO0O0O00O0O :#line:135
        return #line:136
    OOOOO00O0O0OOO000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O0OO0O000O00O00OO ,'Cookie':OOOO0OOO0000O00O0 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:148
    O0000O0OO0O00OOOO =requests .request ("POST",OO0OOOOO00000O0O0 ,headers =OOOOO00O0O0OOO000 ,data =OO0O00OO0O0O00O0O )#line:149
    if O0000O0OO0O00OOOO .status_code ==200 :#line:150
        O0000OOOO0O0O0OOO =O0000O0OO0O00OOOO .json ()#line:151
        if O0000OOOO0O0O0OOO ['data']:#line:152
            return O0000OOOO0O0O0OOO ['data']#line:153
        else :#line:154
            printf (OOOO0OOO0000O00O0 ,f"{O0000O0OO0O00OOOO.status_code} {O0000OOOO0O0O0OOO}")#line:155
            return O0000O0OO0O00OOOO .text #line:156
    else :#line:157
        printf (OOOO0OOO0000O00O0 ,f"{O0000O0OO0O00OOOO.status_code}")#line:158
def apCashWithDraw (O0OO0O0OOOOOOO000 ,O0000O0000O0O0OO0 ,O0O0000OO00000O0O ,OO0000O0OOOOOO000 ,O0OOOO0O0O000O0OO ):#line:160
    OOOO0OO00OO000O0O ="https://api.m.jd.com/"#line:161
    OO0OOOOOO00OOOOO0 ={"linkId":linkId ,"businessSource":"NONE","base":{"id":O0000O0000O0O0OO0 ,"business":"fission","poolBaseId":O0O0000OO00000O0O ,"prizeGroupId":OO0000O0OOOOOO000 ,"prizeBaseId":O0OOOO0O0O000O0OO ,"prizeType":4 }}#line:173
    OOO0O000OO000OO0O =get_h5st_body (ua ,O0OO0O0OOOOOOO000 ,"apCashWithDraw","8c6ae",OO0OOOOOO00OOOOO0 )#line:174
    if not OOO0O000OO000OO0O :#line:175
        return #line:176
    OO0OOOOO00000OO00 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':O0OO0O0OOOOOOO000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:188
    O000O0000O0OO00O0 =requests .request ("POST",OOOO0OO00OO000O0O ,headers =OO0OOOOO00000OO00 ,data =OOO0O000OO000OO0O )#line:189
    if O000O0000O0OO00O0 .status_code ==200 :#line:190
        O0O00000O0OOO0OO0 =O000O0000O0OO00O0 .json ()#line:191
        if O0O00000O0OOO0OO0 ['data']:#line:192
            return O0O00000O0OOO0OO0 ['data']['message']#line:193
        else :#line:194
            printf (O0OO0O0OOOOOOO000 ,f"{O000O0000O0OO00O0.status_code} {O0O00000O0OOO0OO0}")#line:195
def apRecompenseDrawPrize (OOO00O0OO0O000000 ,OO00O00OOO000OOO0 ,OOOOOOO000OOOO0OO ,O0OO000O00000O0OO ,OO00OO0O00O0O0OOO ):#line:197
    O0OO000OO00OO000O ="https://api.m.jd.com/"#line:198
    OOO00O0O00O0O0O0O ={"linkId":linkId ,"drawRecordId":OO00O00OOO000OOO0 ,"business":"fission","poolId":OOOOOOO000OOOO0OO ,"prizeGroupId":O0OO000O00000O0OO ,"prizeId":OO00OO0O00O0O0OOO ,}#line:205
    O0OO00OO000000O00 =get_h5st_body (ua ,OOO00O0OO0O000000 ,"apRecompenseDrawPrize","8c6ae",OOO00O0O00O0O0O0O )#line:206
    if not O0OO00OO000000O00 :#line:207
        return #line:208
    O00O0O0O00O000000 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':ua ,'Cookie':OOO00O0OO0O000000 ,'Host':'api.m.jd.com','Referer':activityUrl ,'Origin':'https://prodev.m.jd.com','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:220
    OO00O0OOO0OOOOO00 =requests .request ("POST",O0OO000OO00OO000O ,headers =O00O0O0O00O000000 ,data =O0OO00OO000000O00 )#line:221
    if OO00O0OOO0OOOOO00 .status_code ==200 :#line:222
        OOO0OOOO000O00OOO =OO00O0OOO0OOOOO00 .json ()#line:223
        if OOO0OOOO000O00OOO ['data']:#line:224
            return "兑换红包成功"#line:226
        else :#line:227
            printf (OOO00O0OO0O000000 ,f"{OO00O0OOO0OOOOO00.status_code} {OOO0OOOO000O00OOO}")


if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()

    inviteDrawPin = os.environ.get("inviteDrawPin") if os.environ.get("inviteDrawPin") else ""
    if inviteDrawPin:
        cookie_ = [ck for ck in cks if inviteDrawPin in ck]
        if cookie_:
            print(f"当前使用【{inviteDrawPin}】作为车头！")
            cookie = cookie_[0]
        else:
            print(f"未发现【{inviteDrawPin}】车头CK,退出程序！")
            sys.exit()
    else:
        print("未设置inviteDrawPin车头,默认CK1作为车头")
        cookie = cks[0]
    ua = userAgent()
    cash = []
    successful = []
    total = 0
    i = 0
    redpacket = []

    for index, linkId in enumerate(linkIds, 1):
        while True:
            try:
                info = inviteFissionDrawPrize(ua, cookie, "inviteFissionDrawPrize", "c02c6", {"linkId":linkId})
                if "活动太火爆" in str(info):
                    printf(cookie, info)
                    time.sleep(0.2)
                    continue
            except Exception as e:
                printf(cookie, e)
                continue
            if not info:
                continue
            if not info[1]:
                printf(cookie, f"{info[0]} ⚠️抽奖结果为{info[1]}")
                continue
            elif "抽奖次数已用完" in info[1]:
                printf(cookie, f"{info[0]} ⚠️抽奖次数已用完")
                break
            elif "本场活动已结束" in info[1]:
                printf(cookie, f"{info[0]} ⏰本场活动已结束了,快去重新开始吧")
                break
            else:
                if info:
                    total += 1
                    if info[2] == 1:
                        printf(cookie, f"{info[0]} 🎫获得{info[1]}优惠券")
                    elif info[2] == 2:
                        printf(cookie, f"{info[0]} 🧧获得{info[1]}红包")
                        redpacket.append(info[1])
                    else:
                        printf(cookie, f"{info[0]} 💵获得{info[1]}现金")
                        cash.append(info[1])

    print(f"\n****************抽奖结束,共抽奖{total}次,💵获得:{'{:.2f}'.format(sum([float(x) for x in cash]))}元现金,🧧获得:{'{:.2f}'.format(sum([float(x) for x in redpacket]))}元红包,开始提现****************\n")

    print(f"****************最大提现页数apCashPageSize设置为{apCashPageSize},请根据实际情况设置****************")
    for index, linkId in enumerate(linkIds, 1):
        i = 0
        while True:
            print(f"\n开始获取第{i + 1}页奖励列表\n")
            body = {"pageNum": i, "pageSize": 20, "linkId": linkId, "business": "fission"}
            info = superRedBagList(ua, cookie, "superRedBagList", "f2b1d", body)
            if not info:
                print("等待10s重新获取")
                time.sleep(10)
                continue
            i += 1
            items = info['items']
            if not items:
                printf(cookie, "全部提现完成！")
                break
            for item in items:
                # printf(cookie, item)
                id = item['id']
                amount = item['amount']
                prizeType = item['prizeType']
                state = item['state']
                prizeConfigName = item['prizeConfigName']
                prizeGroupId = item['prizeGroupId']
                poolBaseId = item['poolBaseId']
                prizeBaseId = item['prizeBaseId']
                if prizeType == 4 and state != 3 and state != 4:
                    cashInfo = apCashWithDraw(cookie, id, poolBaseId, prizeGroupId, prizeBaseId)
                    if cashInfo:
                        printf(cookie, f"{amount}现金 {cashInfo}")
                        if "上限" in cashInfo or "其他pin" in cashInfo or "其它pin" in cashInfo:
                            cashInfo = apRecompenseDrawPrize(cookie, id, poolBaseId, prizeGroupId, prizeBaseId)
                            printf(cookie, f"{amount}现金 {cashInfo}")
                    time.sleep(2)
                else:
                    continue

            time.sleep(1)

            if i >= apCashPageSize:
                break