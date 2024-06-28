#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDrawPdd_new.py(转赚邀好友抽现金助力JD新版)
Author: HarbourJ
Date: 2023/3/15 10:00
TG: https://t.me/HarbourToulu
cron: 30 30 0,12,20 * * *
new Env('转赚邀好友抽现金助力JD新版');
ActivityEntry: 京东-天天赚红包-转赚红包 https://pro.m.jd.com/mall/active/B2Y13x641hwWfpsoRenCzfbz4jR/index.html?inviterId=Q2VzHk9dkShW66_of58y-g&channelType=0&femobile=femobile&activityChannel=jdapp
变量：export inviteDrawPin="车头pin"
"""

import time, requests, sys, re, threading, os, json, random, base64
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
    sys.exit()

# 代理参数默认为本地ip,参数proxyType="";
# 品易代理,参数proxyType="1"; 时长(包月/包日)套餐timeMode改为True,并填写pack参数;流量套餐timeMode为False

proxyType = ""  # 留空默认本地ip，1-品易，2-星空，3-小象，4-携趣，5-51代理，6-代理池
# 这里填写品易代理参数
neek = ""
appkey = ""
timeMode = False  # 时长(包月/包日)套餐改为True;流量套餐为False
pack = ""  # timeMode=True时需要设置pack参数,在提取链接中获取pack
# 这里填写星空代理参数
apikey = ""
signxk = ""
# 这里填写小象代理参数
appKey = ""
appSecret = ""
# 这里填写携趣代理参数
uid = ""
vkey = ""
# 这里填写51代理提取链接
daili51 = ""
# 这里填写代理池地址，如 192.168.31.12:8081
proxyPoolIp = ""
# 并发数量
threadsNum = 1
# 限制最大邀请数量
number_restrictions = 2000

# linkIds = ['3orGfh1YkwNLksxOcN8zWQ', 'Wvzc_VpNTlSkiQdHT8r7QA']
linkIds = ['wDNvX5t2N52cWEM8cLOa0g']
power_success = []
power_failure = []
not_login= []
start = time.time()

def printf (OO00O0O0OO0000OOO ,O0O0OOO0OO000OOOO ):#line:1
    try :#line:2
        O0O0O00O0O000OOO0 =re .compile (r'pt_pin=(.*?);').findall (OO00O0O0OO0000OOO )[0 ]#line:3
        O0O0O00O0O000OOO0 =unquote_plus (O0O0O00O0O000OOO0 )#line:4
    except IndexError :#line:5
        O0O0O00O0O000OOO0 =re .compile (r'pin=(.*?);').findall (OO00O0O0OO0000OOO )[0 ]#line:6
        O0O0O00O0O000OOO0 =unquote_plus (O0O0O00O0O000OOO0 )#line:7
    print (f"{str(datetime.now())[0:22]}->{O0O0O00O0O000OOO0}->{O0O0OOO0OO000OOOO}")#line:8
def list_of_groups (OOO00000O0000OOOO ,O0O00000OOO0O0O00 ):#line:10
    OO0OO00OOOO0OO0OO =zip (*(iter (OOO00000O0000OOOO ),)*O0O00000OOO0O0O00 )#line:11
    O0000OOOO00000O00 =[list (O0O0OO00O0000O00O )for O0O0OO00O0000O00O in OO0OO00OOOO0OO0OO ]#line:12
    OO0OO0O000O000O00 =len (OOO00000O0000OOOO )%O0O00000OOO0O0O00 #line:13
    O0000OOOO00000O00 .append (OOO00000O0000OOOO [-OO0OO0O000O000O00 :])if OO0OO0O000O000O00 !=0 else O0000OOOO00000O00 #line:14
    return O0000OOOO00000O00 #line:15
def get_proxies (OOOO0OO000O00OOO0 ):#line:17
    try :#line:19
        O00OOO0OO0O00OOOO =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:20
    except :#line:21
        O00OOO0OO0O00OOOO =requests .get ("https://ifconfig.me/ip").text #line:22
    print (f"获取当前IP:{O00OOO0OO0O00OOOO}")#line:23
    if proxyType =="":#line:25
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:26
        return None #line:27
    elif proxyType =="1":#line:28
        print ("当前使用品易代理")#line:29
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={O00OOO0OO0O00OOOO}")#line:31
        if timeMode :#line:33
            if not pack :#line:35
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:36
                sys .exit ()#line:37
            OO0O00O00OOO0O0OO =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={OOOO0OO000O00OOO0}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:38
        else :#line:39
            OO0O00O00OOO0O0OO =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={OOOO0OO000O00OOO0}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1")#line:42
    elif proxyType =="2":#line:43
        print ("当前使用星空代理,1个ip一个店铺模式")#line:44
        OO0O00O00OOO0O0OO =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={OOOO0OO000O00OOO0}&format=txt&split=2&sign={signxk}")#line:45
    elif proxyType =="3":#line:46
        print ("当前使用小象代理")#line:47
        OO0O00O00OOO0O0OO =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:48
    elif proxyType =="4":#line:49
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:50
        OO0O00O00OOO0O0OO =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={OOOO0OO000O00OOO0}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:51
    elif proxyType =="5":#line:52
        time .sleep (1 )#line:53
        print ("当前使用51代理,1个ip一个店铺模式")#line:54
        OO0O00O00OOO0O0OO =requests .get (daili51 )#line:55
    elif proxyType =="6":#line:56
        print ("当前使用代理池工具")#line:57
        return [proxyPoolIp ]*OOOO0OO000O00OOO0 #line:58
    else :#line:59
        print ("当前选择代理无效,默认使用本地ip")#line:60
        return None #line:61
    OOO0OO0OO0OO0000O =OO0O00O00OOO0O0OO .text #line:63
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',OOO0OO0OO0OO0000O )is None :#line:65
        print (OOO0OO0OO0OO0000O )#line:66
        return None #line:68
    OOO0OO0OO0OO0000O =OOO0OO0OO0OO0000O .split ('\r\n')#line:69
    OOO0OO0OO0OO0000O =[O000OOO0000O0000O for O000OOO0000O0000O in OOO0OO0OO0OO0000O if O000OOO0000O0000O ]#line:70
    return OOO0OO0OO0OO0000O #line:72
def get_proxy (O0O00000O0000OOO0 ):#line:74
    if proxies :#line:75
        if "@"in O0O00000O0000OOO0 :#line:76
            _OO0O0OOO00000OO0O ={"http":f"http://{O0O00000O0000OOO0.split('@')[0]}@{O0O00000O0000OOO0.split('@')[1]}","https":f"https://{O0O00000O0000OOO0.split('@')[0]}@{O0O00000O0000OOO0.split('@')[1]}"}#line:78
        else :#line:79
            _OO0O0OOO00000OO0O ={"http":f"http://{O0O00000O0000OOO0.split(':')[0]}:{O0O00000O0000OOO0.split(':')[1]}","https":f"https://{O0O00000O0000OOO0.split(':')[0]}:{O0O00000O0000OOO0.split(':')[1]}"}#line:81
    else :#line:82
        _OO0O0OOO00000OO0O =None #line:83
    return _OO0O0OOO00000OO0O #line:84
def convert_ms_to_hours_minutes (O0OO00O0OO00000OO ):#line:86
    O00OOOOOOOO0O0O0O =O0OO00O0OO00000OO //1000 #line:87
    O0OO00O0000O0000O ,O00OOOOOOOO0O0O0O =divmod (O00OOOOOOOO0O0O0O ,60 )#line:88
    O0OOO0OOOO00OOOO0 ,O0OO00O0000O0000O =divmod (O0OO00O0000O0000O ,60 )#line:89
    return f'{O0OOO0OOOO00OOOO0}h{O0OO00O0000O0000O}m'#line:90
def get_h5st_body (OO0OOO0OOOOO0O0O0 ,OOOOOOO0OO0OOO0OO ,O00O00OO00O0OO000 ,OO0O0O00000OOO000 ,O0O0OOO0000OOOO00 ):#line:92
    try :#line:93
        OO0OO0O00O0OO000O =re .compile (r'pt_pin=(.*?);').findall (OOOOOOO0OO0OOO0OO )[0 ]#line:94
        OO0OO0O00O0OO000O =unquote_plus (OO0OO0O00O0OO000O )#line:95
    except IndexError :#line:96
        OO0OO0O00O0OO000O =re .compile (r'pin=(.*?);').findall (OOOOOOO0OO0OOO0OO )[0 ]#line:97
        OO0OO0O00O0OO000O =unquote_plus (OO0OO0O00O0OO000O )#line:98
    OO0000OO0O0OO0000 =OO0OOO0OOOOO0O0O0 .split (";")[2 ]#line:99
    O0O0OOO0000OOOO00 ={"appId":OO0O0O00000OOO000 ,"appid":"activities_platform","ua":OO0OOO0OOOOO0O0O0 ,"pin":OO0OO0O00O0OO000O ,"functionId":O00O00OO00O0OO000 ,"body":O0O0OOO0000OOOO00 ,"clientVersion":OO0000OO0O0OO0000 ,"client":"ios","version":"4.7"}#line:110
    try :#line:111
        O00OO0OO00O0O000O =json .dumps (O0O0OOO0000OOOO00 )#line:112
        O0OO0OOO0OOO00000 ={'Content-Type':'application/json'}#line:115
        OOOO0OO0OOO0O0O0O = ["aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAzL2FwaS9oNXN0"]  # line:116
        O000O0OOOOO00O0O0 =random .choice (OOOO0OO0OOO0O0O0O )#line:117
        OOOOO00OOO0OO0000 =requests .request ("POST",base64 .b64decode (O000O0OOOOO00O0O0 .encode ('utf-8')).decode ('utf-8'),headers =O0OO0OOO0OOO00000 ,timeout =10 ,data =O00OO0OO00O0O000O ).json ()#line:118
        if OOOOO00OOO0OO0000 ['code']==200 :#line:119
            return OOOOO00OOO0OO0000 ['data']#line:120
        else :#line:121
            printf (OOOOOOO0OO0OOO0OO ,f"调用远程h5st接口失败1")#line:122
            return #line:123
    except Exception as OO000OO0OO0OO0OO0 :#line:124
        printf (OOOOOOO0OO0OOO0OO ,f"调用远程h5st接口失败2:{OO000OO0OO0OO0OO0}")#line:125
        get_h5st_body (OO0OOO0OOOOO0O0O0 ,OOOOOOO0OO0OOO0OO ,O00O00OO00O0OO000 ,OO0O0O00000OOO000 ,O0O0OOO0000OOOO00 )#line:126
        return #line:127
def H5API (O00OO0O0O0O00O00O ,O00OO000OO000O0O0 ,O00O0O0OO00OOOOO0 ,O0OO000O00000O0OO ,OO0OO0O0O0OO0OO0O ,proxies =None ):#line:129
    OO0O0O00O0OOOO0OO ="https://api.m.jd.com"#line:130
    OOO0000OOOOO00O00 ={"Accept":"application/json, text/plain, */*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Referer":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","X-Referer-Page":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","Origin":"https://pro.m.jd.com","x-rp-client":"h5_1.0.0","Cookie":O00OO000OO000O0O0 ,"User-Agent":O00OO0O0O0O00O00O }#line:143
    O00O0000OOOO0O0O0 =get_h5st_body (O00OO0O0O0O00O00O ,O00OO000OO000O0O0 ,O00O0O0OO00OOOOO0 ,OO0OO0O0O0OO0OO0O ,O0OO000O00000O0OO )#line:144
    if not O00O0000OOOO0O0O0 :#line:145
        return #line:146
    O0OO000O00000O0OO =O00O0000OOOO0O0O0 #line:147
    try :#line:148
        O00OO00O00O0000OO =requests .post (OO0O0O00O0OOOO0OO ,headers =OOO0000OOOOO00O00 ,data =O0OO000O00000O0OO ,timeout =10 ,proxies =proxies )#line:149
    except Exception as O000OOO000O00O000 :#line:150
        printf (O00OO000OO000O0O0 ,f"H5API Error:{str(O000OOO000O00O000)}")#line:151
        return #line:152
    if O00OO00O00O0000OO .status_code ==200 :#line:153
        return O00OO00O00O0000OO #line:154
    else :#line:155
        printf (O00OO000OO000O0O0 ,O00OO00O00O0000OO .status_code )#line:156
def Result (O0OO0O000O0000000 ,OO0OOOO0OO0OO0O00 ,OOO0OOO000O0O00O0 ,OO00OO0000OOO0O0O ):#line:158
    for O0OO0O0000O0000OO ,O0O000OOO0000OOO0 in enumerate (linkIds ,1 ):#line:159
        OO0OOO0000OO0OOOO =H5API (O0OO0O000O0000000 ,OO0OOOO0OO0OO0O00 ,"inviteFissionhelp",{'linkId':O0O000OOO0000OOO0 ,"isJdApp":True ,'inviter':OOO0OOO000O0O00O0 },'c5389',OO00OO0000OOO0O0O )#line:160
        if not OO0OOO0000OO0OOOO :#line:161
            return #line:162
        if int (OO0OOO0000OO0OOOO .status_code )!=int (200 ):#line:163
            printf (OO0OOOO0OO0OO0O00 ,f'接口：{OO0OOO0000OO0OOOO.status_code}')#line:164
            return #line:165
        if int (OO0OOO0000OO0OOOO .json ()['code'])==0 :#line:166
            if OO0OOO0000OO0OOOO .json ()['data']['helpResult']==1 :#line:167
                O0OOO0OO0O0OO00O0 ='✅助力成功'#line:168
                power_success .append (OO0OOOO0OO0OO0O00 )#line:169
            elif OO0OOO0000OO0OOOO .json ()['data']['helpResult']==2 :#line:170
                O0OOO0OO0O0OO00O0 ='❌火爆...助力失败'#line:171
                power_failure .append (OO0OOOO0OO0OO0O00 )#line:172
            elif OO0OOO0000OO0OOOO .json ()['data']['helpResult']==3 :#line:173
                O0OOO0OO0O0OO00O0 ='❌已经助力别人'#line:174
                power_failure .append (OO0OOOO0OO0OO0O00 )#line:175
            elif OO0OOO0000OO0OOOO .json ()['data']['helpResult']==4 :#line:176
                O0OOO0OO0O0OO00O0 ='❌助力次数用完了'#line:177
                power_failure .append (OO0OOOO0OO0OO0O00 )#line:178
            elif OO0OOO0000OO0OOOO .json ()['data']['helpResult']==6 :#line:179
                O0OOO0OO0O0OO00O0 ='❌已经助力过了'#line:180
                power_failure .append (OO0OOOO0OO0OO0O00 )#line:181
            else :#line:182
                O0OOO0OO0O0OO00O0 ='❌未知状态'#line:183
                power_failure .append (OO0OOOO0OO0OO0O00 )#line:184
            if O0OO0O0000O0000OO ==1 :#line:185
                O0O0OO000OO0O000O ="JD"#line:186
            else :#line:187
                O0O0OO000OO0O000O ="JX"#line:188
            printf (OO0OOOO0OO0OO0O00 ,f"{OO0OOO0000OO0OOOO.status_code}【{O0O0OO000OO0O000O}】助力-→{OO0OOO0000OO0OOOO.json()['data']['nickName']}|{OO0OOO0000OO0OOOO.json()['data']['helpResult']} {O0OOO0OO0O0OO00O0}")#line:189
        else :#line:190
            printf (OO0OOOO0OO0OO0O00 ,f"{OO0OOO0000OO0OOOO.json()['code']}  💔{OO0OOO0000OO0OOOO.json()['errMsg']}")#line:191
            not_login .append (OO0OOOO0OO0OO0O00 )#line:192
if __name__ =='__main__':#line:194
    try :#line:195
        cks =getCk #line:196
        if not cks :#line:197
            sys .exit ()#line:198
    except :#line:199
        print ("未获取到有效COOKIE,退出程序！")#line:200
        sys .exit ()#line:201
    inviter =remote_redis (f"inviteFissionBeforeHome",3 )#line:202
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:203
    if inviteDrawPin :#line:204
        cookie_ =[O000000OOOO0O0O0O for O000000OOOO0O0O0O in cks if inviteDrawPin in O000000OOOO0O0O0O ]#line:205
        if cookie_ :#line:206
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:207
            cookie =cookie_ [0 ]#line:208
        else :#line:209
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:210
    else :#line:211
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:212
        cookie =cks [0 ]#line:213
    ua =userAgent ()#line:214
    for index ,linkId in enumerate (linkIds ,1 ):#line:215
        response =H5API (ua ,cookie ,"inviteFissionBeforeHome",{'linkId':linkId ,"isJdApp":True ,'inviter':inviter },'02f8d').json ()#line:216
        if response ['success']==False and response ['code']==1000 :#line:217
            printf (cookie ,f"{response['errMsg']}")#line:218
            sys .exit ()#line:219
        time.sleep(0.1)
        response = H5API(ua, cookie, "inviteFissionhelp", {'linkId':linkId, "isJdApp":True, 'inviter':inviter, "clientFirstLaunchInfo":"", "userFirstLaunchInfo":""}, 'c5389')
        if int(response.status_code) != 200:
            printf(cookie, f'接口：{response.status_code}')
            sys.exit()
        if int(response.json()['code']) == 0:
            if response.json()['data']['helpResult'] == 1:  # line:220
                printf(cookie, f'✅助力作者成功 谢谢你 你是个好人！！！')  # line:221
            else:  # line:222
                printf(cookie, f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')  # line:223
        else:
            printf(cookie, f"{response.json()['code']}  💔{response.json()['errMsg']}")
        response =H5API (ua ,cookie ,'inviteFissionHome',{'linkId':linkId ,"inviter":""},'eb67b').json ()#line:224
        if index ==1 :#line:225
            printf (cookie ,f'【JD】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')#line:226
            prizeNum1 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:227
        else :#line:228
            printf (cookie ,f'【JX】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')#line:229
            prizeNum2 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:230
        inviter =response ["data"]["inviter"]#line:231
    time .sleep (1 )#line:233
    new_cks =list_of_groups (cks ,threadsNum )[:]#line:234
    for i ,cookies in enumerate (new_cks ,1 ):#line:235
        print (f"\n##############并发第{i}组ck##############")#line:236
        threads =[]#line:237
        proxies =get_proxies (threadsNum )#line:238
        proxies =proxies if proxies else None #line:239
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:240
        for index ,cookie in enumerate (cookies ,1 ):#line:241
            _O0OOO0OO0O0OOO000 =get_proxy (proxies [index -1 ])if proxies else None #line:242
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,_O0OOO0OO0O0OOO000 ))#line:243
            threads .append (thead_one )#line:244
            power_num =len (power_success )#line:245
            if power_num >=int (number_restrictions ):#line:246
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:247
                sys .exit ()#line:248
        for t in threads :#line:249
            t .start ()#line:250
            time .sleep (1 )#line:251
        for t in threads :#line:252
            t .join ()#line:253
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')