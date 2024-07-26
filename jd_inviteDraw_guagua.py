#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDraw_guagua.py(夺金刮刮乐助力)
Author: HarbourJ
Date: 2024/7/26 10:00
TG: https://t.me/HarbourToulu
cron: 30 30 0,12,20 * * *
new Env('夺金刮刮乐助力');
ActivityEntry: https://pro.m.jd.com/mall/active/3pdfN7oPzb6if7pB8N8dMr4dV2ys/index.html
变量：export inviteDrawPin="车头pin"
"""

import time, requests, sys, re, threading
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
# http://api2.xkdaili.com/tools/XApi.ashx?apikey=&qty=1&format=txt&split=0&sign=
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
number_restrictions = 50

linkId ='1v8ROyHv8LXPs559oaclNA'#line:1
power_success =[]#line:2
power_failure =[]#line:3
not_login =[]#line:4
start =time .time ()#line:5
def printf (OOOO000OOOO000OOO ,O00O000O00OOO000O ):#line:7
    try :#line:8
        OOO000OOO0OOO0OOO =re .compile (r'pt_pin=(.*?);').findall (OOOO000OOOO000OOO )[0 ]#line:9
        OOO000OOO0OOO0OOO =unquote_plus (OOO000OOO0OOO0OOO )#line:10
    except IndexError :#line:11
        OOO000OOO0OOO0OOO =re .compile (r'pin=(.*?);').findall (OOOO000OOOO000OOO )[0 ]#line:12
        OOO000OOO0OOO0OOO =unquote_plus (OOO000OOO0OOO0OOO )#line:13
    print (f"{str(datetime.now())[0:22]}->{OOO000OOO0OOO0OOO}->{O00O000O00OOO000O}")#line:14
def list_of_groups (O0O0O00OO0OOOO0OO ,O00O0O0O000OO0000 ):#line:16
    O0OO0OO00OO0OOO00 =zip (*(iter (O0O0O00OO0OOOO0OO ),)*O00O0O0O000OO0000 )#line:17
    OO0OO0O000O00OOO0 =[list (OOO0000OO00000O00 )for OOO0000OO00000O00 in O0OO0OO00OO0OOO00 ]#line:18
    O00O00000O0O00O00 =len (O0O0O00OO0OOOO0OO )%O00O0O0O000OO0000 #line:19
    OO0OO0O000O00OOO0 .append (O0O0O00OO0OOOO0OO [-O00O00000O0O00O00 :])if O00O00000O0O00O00 !=0 else OO0OO0O000O00OOO0 #line:20
    return OO0OO0O000O00OOO0 #line:21
def get_proxy (O0OO00000O0O00OOO ):#line:23
    if "@"in O0OO00000O0O00OOO :#line:24
        _OO0OO00O0OOOO0O0O ={"http":f"http://{O0OO00000O0O00OOO.split('@')[0]}@{O0OO00000O0O00OOO.split('@')[1]}","https":f"http://{O0OO00000O0O00OOO.split('@')[0]}@{O0OO00000O0O00OOO.split('@')[1]}"}#line:26
    else :#line:27
        _OO0OO00O0OOOO0O0O ={"http://":f"http://{O0OO00000O0O00OOO.split(':')[0]}:{O0OO00000O0O00OOO.split(':')[1]}","https://":f"http://{O0OO00000O0O00OOO.split(':')[0]}:{O0OO00000O0O00OOO.split(':')[1]}"}#line:29
    return _OO0OO00O0OOOO0O0O #line:30
def get_proxies (O0OOO0OO0O000OOO0 ):#line:32
    try :#line:34
        O0OOO000O0OOOO0OO =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:35
    except :#line:36
        O0OOO000O0OOOO0OO =requests .get ("https://ifconfig.me/").text #line:37
    print (f"获取当前IP:{O0OOO000O0OOOO0OO}")#line:38
    if proxyType =="":#line:40
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:41
        return None #line:42
    elif proxyType =="1":#line:43
        print ("当前使用品易代理")#line:44
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={O0OOO000O0OOOO0OO}")#line:46
        if timeMode :#line:49
            if not pack :#line:51
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:52
                sys .exit ()#line:53
            OOOOO0000O0OOO0OO =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={O0OOO0OO0O000OOO0}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:54
        else :#line:55
            OOOOO0000O0OOO0OO =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={O0OOO0OO0O000OOO0}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1")#line:58
    elif proxyType =="2":#line:59
        print ("当前使用星空代理,1个ip一个店铺模式")#line:60
        OOOOO0000O0OOO0OO =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={O0OOO0OO0O000OOO0}&format=txt&split=2&sign={signxk}")#line:61
    elif proxyType =="3":#line:62
        print ("当前使用小象代理")#line:63
        OOOOO0000O0OOO0OO =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:64
    elif proxyType =="4":#line:65
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:66
        OOOOO0000O0OOO0OO =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={O0OOO0OO0O000OOO0}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:67
    elif proxyType =="5":#line:68
        time .sleep (1 )#line:69
        print ("当前使用51代理,1个ip一个店铺模式")#line:70
        OOOOO0000O0OOO0OO =requests .get (daili51 )#line:71
    elif proxyType =="6":#line:72
        print ("当前使用代理池工具")#line:73
        return [proxyPoolIp ]*O0OOO0OO0O000OOO0 #line:74
    else :#line:75
        print ("当前选择代理无效,默认使用本地ip")#line:76
        return None #line:77
    O000O00000O0OO000 =OOOOO0000O0OOO0OO .text #line:79
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',O000O00000O0OO000 )is None :#line:81
        print (O000O00000O0OO000 )#line:82
        return None #line:84
    O000O00000O0OO000 =O000O00000O0OO000 .split ('\r\n')#line:85
    O000O00000O0OO000 =[OO0000OO0OOO0OOO0 for OO0000OO0OOO0OOO0 in O000O00000O0OO000 if OO0000OO0OOO0OOO0 ]#line:86
    return O000O00000O0OO000 #line:88
def convert_ms_to_hours_minutes (O0OO0O0OOO0O00O0O ):#line:90
    O00OOO0OOOOOOOOOO =O0OO0O0OOO0O00O0O //1000 #line:91
    O0OOO0O0O0O0OOO00 ,O00OOO0OOOOOOOOOO =divmod (O00OOO0OOOOOOOOOO ,60 )#line:92
    OO0O00O0O0O0OO0O0 ,O0OOO0O0O0O0OOO00 =divmod (O0OOO0O0O0O0OOO00 ,60 )#line:93
    return f'{OO0O00O0O0O0OO0O0}h{O0OOO0O0O0O0OOO00}m'#line:94
def get_h5st_body (O00000OOOOO00O0O0 ,OOOOO00OOO000OO0O ,O0OOO0OOOO00OOO00 ,OO00OO00O00O0OOO0 ,O00O0OOO0000OO000 ):#line:96
    try :#line:97
        OOO000OOOO0OO0OO0 =re .compile (r'pt_pin=(.*?);').findall (OOOOO00OOO000OO0O )[0 ]#line:98
        OOO000OOOO0OO0OO0 =unquote_plus (OOO000OOOO0OO0OO0 )#line:99
    except IndexError :#line:100
        OOO000OOOO0OO0OO0 =re .compile (r'pin=(.*?);').findall (OOOOO00OOO000OO0O )[0 ]#line:101
        OOO000OOOO0OO0OO0 =unquote_plus (OOO000OOOO0OO0OO0 )#line:102
    OOO00O0O0OO0O0O00 =O00000OOOOO00O0O0 .split (";")[2 ]#line:103
    O00O0OOO0000OO000 ={"t":True ,"appId":OO00OO00O00O0OOO0 ,"appid":"activities_platform","ua":O00000OOOOO00O0O0 ,"pin":OOO000OOOO0OO0OO0 ,"functionId":O0OOO0OOOO00OOO00 ,"body":O00O0OOO0000OO000 ,"clientVersion":OOO00O0O0OO0O0O00 ,"client":"ios","version":"4.7"}#line:115
    try :#line:116
        import base64 #line:117
        OOOO0OO0O0OO0OO0O ="aHR0cDovLzEuMTQuMjA4LjE3ODozMDAzL2FwaS9oNXN0"#line:118
        OOO0O00OOOO000O0O =json .dumps (O00O0OOO0000OO000 )#line:119
        OO000OO00O0OO0O0O ={'Content-Type':'application/json'}#line:122
        O0O0O00OOO0O0O0O0 =requests .request ("POST",base64 .b64decode (OOOO0OO0O0OO0OO0O .encode ('utf-8')).decode ('utf-8'),headers =OO000OO00O0OO0O0O ,timeout =10 ,data =OOO0O00OOOO000O0O ).json ()#line:123
        if O0O0O00OOO0O0O0O0 ['code']==200 :#line:124
            return O0O0O00OOO0O0O0O0 ['data']#line:126
        else :#line:127
            printf (OOOOO00OOO000OO0O ,f"调用远程h5st接口失败1")#line:128
            return #line:129
    except Exception as OO0O00OO0O00O000O :#line:130
        printf (OOOOO00OOO000OO0O ,f"调用远程h5st接口失败2:{OO0O00OO0O00O000O}")#line:131
        get_h5st_body (O00000OOOOO00O0O0 ,OOOOO00OOO000OO0O ,O0OOO0OOOO00OOO00 ,OO00OO00O00O0OOO0 ,O00O0OOO0000OO000 )#line:132
        return #line:133
def H5API (OOO00000O0OOOO00O ,OO0000OOOO00O0OO0 ,OOOO0OO0O00000OOO ,O0OOOOO000OOOOOOO ,O00OOO000OOOO0O0O ,proxies =None ):#line:135
    O000O0O0000OO0O00 ="https://api.m.jd.com"#line:136
    O0O0OO00O0OOOO000 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":OO0000OOOO00O0OO0 ,"User-Agent":OOO00000O0OOOO00O ,}#line:148
    OOO00OO00OOOOO00O =get_h5st_body (OOO00000O0OOOO00O ,OO0000OOOO00O0OO0 ,OOOO0OO0O00000OOO ,O00OOO000OOOO0O0O ,O0OOOOO000OOOOOOO )#line:149
    if not OOO00OO00OOOOO00O :#line:150
        return #line:151
    O0OOOOO000OOOOOOO =OOO00OO00OOOOO00O #line:152
    try :#line:153
        O000O00OO0O00OOOO =requests .post (O000O0O0000OO0O00 ,headers =O0O0OO00O0OOOO000 ,data =O0OOOOO000OOOOOOO ,timeout =5 ,proxies =proxies )#line:154
    except Exception as OO0OOO00O0OOOOO00 :#line:155
        printf (OO0000OOOO00O0OO0 ,f"H5API Error:{str(OO0OOO00O0OOOOO00)}")#line:156
        return #line:157
    if O000O00OO0O00OOOO .status_code ==200 :#line:158
        return O000O00OO0O00OOOO #line:159
    else :#line:160
        printf (OO0000OOOO00O0OO0 ,O000O00OO0O00OOOO .status_code )#line:161
def Result (OOOO00OO0O0O00O0O ,O0O0O0OO000O0O0OO ,O0O000O0000O0O000 ,O0OO0OO0OO00O00O0 ):#line:163
    O0O0OOOO0O0O0O0O0 =H5API (OOOO00OO0O0O00O0O ,O0O0O0OO000O0O0OO ,"inviteFissionhelp",{"linkId":linkId,"isJdApp":True,"inviter":O0O000O0000O0O000,"clientFirstLaunchInfo":"","userFirstLaunchInfo":"","area":""},'c5389',O0OO0OO0OO00O00O0 )#line:170
    if not O0O0OOOO0O0O0O0O0 :#line:172
        return #line:173
    if int (O0O0OOOO0O0O0O0O0 .status_code )!=int (200 ):#line:174
        printf (O0O0O0OO000O0O0OO ,f'接口：{O0O0OOOO0O0O0O0O0.status_code}')#line:175
        return #line:176
    if int (O0O0OOOO0O0O0O0O0 .json ()['code'])==0 :#line:177
        if O0O0OOOO0O0O0O0O0 .json ()['data']['helpResult']==1 :#line:178
            O0O0OOO000OOO0O00 ='✅助力成功'#line:179
            power_success .append (O0O0O0OO000O0O0OO )#line:180
        elif O0O0OOOO0O0O0O0O0 .json ()['data']['helpResult']==2 :#line:181
            O0O0OOO000OOO0O00 ='❌火爆...助力失败'#line:182
            power_failure .append (O0O0O0OO000O0O0OO )#line:183
        elif O0O0OOOO0O0O0O0O0 .json ()['data']['helpResult']==3 :#line:184
            O0O0OOO000OOO0O00 ='❌已经助力别人'#line:185
            power_failure .append (O0O0O0OO000O0O0OO )#line:186
        elif O0O0OOOO0O0O0O0O0 .json ()['data']['helpResult']==4 :#line:187
            O0O0OOO000OOO0O00 ='❌助力次数用完了'#line:188
            power_failure .append (O0O0O0OO000O0O0OO )#line:189
        elif O0O0OOOO0O0O0O0O0 .json ()['data']['helpResult']==6 :#line:190
            O0O0OOO000OOO0O00 ='❌已经助力过了'#line:191
            power_failure .append (O0O0O0OO000O0O0OO )#line:192
        else :#line:193
            O0O0OOO000OOO0O00 ='❌未知状态'#line:194
            power_failure .append (O0O0O0OO000O0O0OO )#line:195
        printf (O0O0O0OO000O0O0OO ,f"{O0O0OOOO0O0O0O0O0.status_code}【guagua】助力-→{O0O0OOOO0O0O0O0O0.json()['data']['nickName']}|{O0O0OOOO0O0O0O0O0.json()['data']['helpResult']} {O0O0OOO000OOO0O00}")#line:196
    else :#line:197
        printf (O0O0O0OO000O0O0OO ,f"{O0O0OOOO0O0O0O0O0.json()['code']}  💔{O0O0OOOO0O0O0O0O0.json()['errMsg']}")#line:198
        not_login .append (O0O0O0OO000O0O0OO )#line:199
if __name__ =='__main__':#line:201
    try :#line:202
        cks =getCk #line:203
        if not cks :#line:204
            sys .exit ()#line:205
    except :#line:206
        print ("未获取到有效COOKIE,退出程序！")#line:207
        sys .exit ()#line:208
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:209
    if inviteDrawPin :#line:210
        cookie_ =[O00O00O00O0O0O0OO for O00O00O00O0O0O0OO in cks if inviteDrawPin in O00O00O00O0O0O0OO ]#line:211
        if cookie_ :#line:212
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:213
            cookie =cookie_ [0 ]#line:214
        else :#line:215
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:216
            sys .exit ()#line:217
    else :#line:218
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:219
        cookie =cks [0 ]#line:220
    inviter =remote_redis (f"inviteFissionBeforeHome",3 )#line:221
    ua =userAgent ()#line:222
    response =H5API (ua ,cookie ,"inviteFissionhelp",{"linkId":linkId,"isJdApp":True,"inviter":inviter,"clientFirstLaunchInfo":"","userFirstLaunchInfo":"","area":""},'c5389').json ()#line:223
    if response ['success']==False and response ['code']==1000 :#line:224
        printf (cookie ,f"{response['errMsg']}")#line:225
        sys .exit ()#line:226
    if response ['data']['helpResult']==1 :#line:227
        printf (cookie ,f'✅助力作者成功 谢谢你 你是个好人！！！')#line:228
    else :#line:229
        printf (cookie ,f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:230
    response =H5API (ua ,cookie ,'inviteFissionHome',{"linkId":linkId,"inviter":""},'eb67b').json ()#line:231
    printf (cookie ,f'【guagua】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 💰领现金进度{response["data"]["cashVo"]["amount"]}/{response["data"]["cashVo"]["totalAmount"]} ✅【助力码】:{response["data"]["inviter"]}')#line:232
    prizeNum2 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:233
    inviter =response ["data"]["inviter"]#line:234
    time .sleep (1 )#line:236
    new_cks =list_of_groups (cks ,threadsNum )[:]#line:237
    for i ,cookies in enumerate (new_cks ,1 ):#line:238
        print (f"\n##############并发第{i}组ck##############")#line:239
        threads =[]#line:240
        proxies =get_proxies (threadsNum )#line:241
        proxies =proxies if proxies else None #line:242
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:243
        for index ,cookie in enumerate (cookies ,1 ):#line:244
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,get_proxy (proxies [index -1 ])if proxies else None ))#line:245
            threads .append (thead_one )#line:246
            power_num =len (power_success )#line:247
            if power_num >=int (number_restrictions ):#line:248
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:249
                sys .exit ()#line:250
        for t in threads :#line:251
            t .start ()#line:252
        for t in threads :#line:253
            t .join ()#line:254
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')