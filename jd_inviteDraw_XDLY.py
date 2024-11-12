#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: jd_inviteDraw_XDLY.py(东东心动乐园抽奖助力)
Author: HarbourJ
Date: 2024/10/17 10:00
TG: https://t.me/HarbourToulu
cron: 5 0 0,11,20 * * *
new Env('东东心动乐园抽奖助力');
ActivityEntry: 京东-玩一玩-东东心动乐园
变量：export inviteDrawPin="车头pin"
"""

import time, requests, sys, re, threading, json
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
# http://api2.xkdaili.com/tools/XApi.ashx?apikey=XKFAD17D8BF85B3F0129&qty=1&format=txt&split=0&sign=ab86534e2ad195135e8cf719a23a5a49
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
number_restrictions = 20
# 检测ck有效性
ischeck = False
linkId = 'BDhyBiZZFd5l3BkNVMqzZg'
power_success = []
power_failure = []
not_login= []
start = time.time()

def printf (OO00OO0O00OO00O00 ,O00OOO0O00O000000 ):#line:1
    try :#line:2
        O000OOO0O000OOOOO =re .compile (r'pt_pin=(.*?);').findall (OO00OO0O00OO00O00 )[0 ]#line:3
        O000OOO0O000OOOOO =unquote_plus (O000OOO0O000OOOOO )#line:4
    except IndexError :#line:5
        O000OOO0O000OOOOO =re .compile (r'pin=(.*?);').findall (OO00OO0O00OO00O00 )[0 ]#line:6
        O000OOO0O000OOOOO =unquote_plus (O000OOO0O000OOOOO )#line:7
    print (f"{str(datetime.now())[0:22]}->{O000OOO0O000OOOOO}->{O00OOO0O00O000000}")#line:8
def list_of_groups (O00OO00O00O0OO00O ,O0000OOOO00000OO0 ):#line:10
    OOOOO0O00000000OO =zip (*(iter (O00OO00O00O0OO00O ),)*O0000OOOO00000OO0 )#line:11
    OO00O000OO0000000 =[list (OO000OO0OOO00000O )for OO000OO0OOO00000O in OOOOO0O00000000OO ]#line:12
    OO000O000OOO000OO =len (O00OO00O00O0OO00O )%O0000OOOO00000OO0 #line:13
    OO00O000OO0000000 .append (O00OO00O00O0OO00O [-OO000O000OOO000OO :])if OO000O000OOO000OO !=0 else OO00O000OO0000000 #line:14
    return OO00O000OO0000000 #line:15
def get_proxies (OOOO00O000OOO0000 ):#line:17
    if proxyType =="":#line:19
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:20
        return None #line:21
    elif proxyType =="1":#line:22
        try :#line:24
            O0O0O00OO0000OO00 =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:25
        except :#line:26
            O0O0O00OO0000OO00 =requests .get ("https://ifconfig.me/").text #line:27
        print (f"获取当前IP:{O0O0O00OO0000OO00}")#line:28
        print ("当前使用品易代理")#line:29
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={O0O0O00OO0000OO00}")#line:31
        if timeMode :#line:34
            if not pack :#line:36
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:37
                sys .exit ()#line:38
            OOOO0000000OO0O0O =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={OOOO00O000OOO0000}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:39
        else :#line:40
            OOOO0000000OO0O0O =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={OOOO00O000OOO0000}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1")#line:43
    elif proxyType =="2":#line:44
        print ("当前使用星空代理,1个ip一个店铺模式")#line:45
        OOOO0000000OO0O0O =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={OOOO00O000OOO0000}&format=txt&split=2&sign={signxk}")#line:46
    elif proxyType =="3":#line:47
        print ("当前使用小象代理")#line:48
        OOOO0000000OO0O0O =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:49
    elif proxyType =="4":#line:50
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:51
        OOOO0000000OO0O0O =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={OOOO00O000OOO0000}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:52
    elif proxyType =="5":#line:53
        time .sleep (1 )#line:54
        print ("当前使用51代理,1个ip一个店铺模式")#line:55
        OOOO0000000OO0O0O =requests .get (daili51 )#line:56
    elif proxyType =="6":#line:57
        print ("当前使用代理池工具")#line:58
        return [proxyPoolIp ]*OOOO00O000OOO0000 #line:59
    else :#line:60
        print ("当前选择代理无效,默认使用本地ip")#line:61
        return None #line:62
    OOO00000O00O00OOO =OOOO0000000OO0O0O .text #line:64
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',OOO00000O00O00OOO )is None :#line:66
        print (OOO00000O00O00OOO )#line:67
        return None #line:69
    OOO00000O00O00OOO =OOO00000O00O00OOO .split ('\r\n')#line:70
    OOO00000O00O00OOO =[O00O0OOOO00OOOO00 for O00O0OOOO00OOOO00 in OOO00000O00O00OOO if O00O0OOOO00OOOO00 ]#line:71
    return OOO00000O00O00OOO #line:73
def get_proxy (OOOO0OOOOO0O0OO00 ):#line:75
    if "@"in OOOO0OOOOO0O0OO00 :#line:76
        _O0O0000OOOOO0O0O0 ={"http":f"http://{OOOO0OOOOO0O0OO00.split('@')[0]}@{OOOO0OOOOO0O0OO00.split('@')[1]}","https":f"http://{OOOO0OOOOO0O0OO00.split('@')[0]}@{OOOO0OOOOO0O0OO00.split('@')[1]}"}#line:78
    else :#line:79
        _O0O0000OOOOO0O0O0 ={"http":f"http://{OOOO0OOOOO0O0OO00.split(':')[0]}:{OOOO0OOOOO0O0OO00.split(':')[1]}","https":f"http://{OOOO0OOOOO0O0OO00.split(':')[0]}:{OOOO0OOOOO0O0OO00.split(':')[1]}"}#line:83
    return _O0O0000OOOOO0O0O0 #line:85
def check (OO0OOO0O0O0OO0O0O ,O00OO00000000OOO0 ,OOO0O0O000000OOO0 ):#line:87
    try :#line:88
        O000O0OOO00000O0O ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:89
        O00OOO0000O00000O ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":O00OO00000000OOO0 ,"User-Agent":OO0OOO0O0O0OO0O0O ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:99
        OOO0OOO00O00O0OO0 =requests .get (url =O000O0OOO00000O0O ,headers =O00OOO0000O00000O ,timeout =2 ,proxies =OOO0O0O000000OOO0 ).text #line:100
        O00OO000OOOOOO00O =json .loads (OOO0OOO00O00O0OO0 )#line:101
        if O00OO000OOOOOO00O ['retcode']=='1001':#line:102
            OO0O000OOO0OOOOO0 ="⚠️当前ck已失效，请检查"#line:103
            printf (O00OO00000000OOO0 ,OO0O000OOO0OOOOO0 )#line:104
            return {'code':1001 ,'data':OO0O000OOO0OOOOO0 }#line:105
        elif O00OO000OOOOOO00O ['retcode']=='0'and 'userInfo'in O00OO000OOOOOO00O ['data']:#line:106
            O000000OO0OOO0OOO =O00OO000OOOOOO00O ['data']['userInfo']['baseInfo']['nickname']#line:107
            printf (O00OO00000000OOO0 ,f"发现有效ck {O000000OO0OOO0OOO}")#line:108
            return {'code':200 ,'name':O000000OO0OOO0OOO ,'ck':O00OO00000000OOO0 }#line:111
    except Exception as OO0O00OO0OOOOO0OO :#line:112
        printf (O00OO00000000OOO0 ,OO0O00OO0OOOOO0OO )#line:113
        return {'code':0 ,'data':OO0O00OO0OOOOO0OO }#line:114
def convert_ms_to_hours_minutes (OO00OOOO0O00O000O ):#line:117
    O0O0OO0OOOO00O0OO =OO00OOOO0O00O000O //1000 #line:118
    OO00OO00O0OO00O0O ,O0O0OO0OOOO00O0OO =divmod (O0O0OO0OOOO00O0OO ,60 )#line:119
    O00OOO0OO000OOOO0 ,OO00OO00O0OO00O0O =divmod (OO00OO00O0OO00O0O ,60 )#line:120
    return f'{O00OOO0OO000OOOO0}h{OO00OO00O0OO00O0O}m'#line:121
def get_h5st_body (O00O0O0OO0O00OO0O ,O00O000O000O000O0 ,OO0O00OO00OOOO00O ,OOO00OOOOOOOO0O0O ,OO0O0OO00O0O000O0 ):#line:123
    try :#line:124
        OO0OOOO0OO0O000O0 =re .compile (r'pt_pin=(.*?);').findall (O00O000O000O000O0 )[0 ]#line:125
        OO0OOOO0OO0O000O0 =unquote_plus (OO0OOOO0OO0O000O0 )#line:126
    except IndexError :#line:127
        OO0OOOO0OO0O000O0 =re .compile (r'pin=(.*?);').findall (O00O000O000O000O0 )[0 ]#line:128
        OO0OOOO0OO0O000O0 =unquote_plus (OO0OOOO0OO0O000O0 )#line:129
    O0OOOOO0OOOOO0O0O =O00O0O0OO0O00OO0O .split (";")[2 ]#line:130
    OO0O0OO00O0O000O0 ={"t":True ,"appId":OOO00OOOOOOOO0O0O ,"appid":"activities_platform","ua":O00O0O0OO0O00OO0O ,"pin":OO0OOOO0OO0O000O0 ,"functionId":OO0O00OO00OOOO00O ,"body":OO0O0OO00O0O000O0 ,"clientVersion":O0OOOOO0OOOOO0O0O ,"client":"ios","version":"4.8"}#line:142
    try :#line:143
        import base64 #line:144
        O0O0OOOOOO00OO000 ="aHR0cHM6Ly9oYXJib3Vyai5jZi9hcGkvaDVzdA=="#line:145
        O0O00000O00000O0O =json .dumps (OO0O0OO00O0O000O0 )#line:146
        O0OOOO0O0O00O0O00 ={'Content-Type':'application/json'}#line:149
        OOOOO0000000O0OOO =requests .request ("POST",base64 .b64decode (O0O0OOOOOO00OO000 .encode ('utf-8')).decode ('utf-8'),headers =O0OOOO0O0O00O0O00 ,timeout =10 ,data =O0O00000O00000O0O ).json ()#line:150
        if OOOOO0000000O0OOO ['code']==200 :#line:151
            return OOOOO0000000O0OOO ['data']#line:153
        else :#line:154
            printf (O00O000O000O000O0 ,f"调用远程h5st接口失败1")#line:155
            return #line:156
    except Exception as O00OOO0OOO000000O :#line:157
        printf (O00O000O000O000O0 ,f"调用远程h5st接口失败2:{O00OOO0OOO000000O}")#line:158
        get_h5st_body (O00O0O0OO0O00OO0O ,O00O000O000O000O0 ,OO0O00OO00OOOO00O ,OOO00OOOOOOOO0O0O ,OO0O0OO00O0O000O0 )#line:159
        return #line:160
def H5API (OO00000O0O0OO0O0O ,OOOO000OOOO0O0OO0 ,O0OO0O0OO00000O0O ,O0O000OO00O0O000O ,O000O0O0O0O00OOOO ,proxies =None ):#line:162
    OO0O0000OO0000O00 ="https://api.m.jd.com"#line:163
    O00OO0OO0OOOOO0O0 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":OOOO000OOOO0O0OO0 ,"User-Agent":OO00000O0O0OO0O0O ,}#line:175
    O00O00OOO00OO00O0 =get_h5st_body (OO00000O0O0OO0O0O ,OOOO000OOOO0O0OO0 ,O0OO0O0OO00000O0O ,O000O0O0O0O00OOOO ,O0O000OO00O0O000O )#line:176
    if not O00O00OOO00OO00O0 :#line:177
        return #line:178
    O0O000OO00O0O000O =O00O00OOO00OO00O0 #line:179
    try :#line:180
        OOO000OO00000O000 =requests .post (OO0O0000OO0000O00 ,headers =O00OO0OO0OOOOO0O0 ,data =O0O000OO00O0O000O ,timeout =5 ,proxies =proxies )#line:181
    except Exception as OOOO00OOOO0O0OO0O :#line:182
        printf (OOOO000OOOO0O0OO0 ,f"H5API Error:{str(OOOO00OOOO0O0OO0O)}")#line:183
        return #line:184
    if OOO000OO00000O000 .status_code ==200 :#line:185
        return OOO000OO00000O000 #line:186
    else :#line:187
        printf (OOOO000OOOO0O0OO0 ,OOO000OO00000O000 .status_code )#line:188
def Result (O0O000O00OO00OOO0 ,O0OOO00OOOO00OO00 ,O0O0O0O000O000000 ,O0O00O0O0OO0000O0 ):#line:190
    if O0OOO00OOOO00OO00 [-1 ]!=";":#line:191
        O0OOO00OOOO00OO00 +=";"#line:192
    if ischeck :#line:193
        if check (O0O000O00OO00OOO0 ,O0OOO00OOOO00OO00 ,O0O00O0O0OO0000O0 )["code"]==1001 :#line:194
            return #line:195
    OOO000OO0O0O0O000 =H5API (O0O000O00OO00OOO0 ,O0OOO00OOOO00OO00 ,"drawFissionhelp",{"envType":1 ,"linkId":linkId ,"isJdApp":True ,"inviter":O0O0O0O000O000000 ,"clientFirstLaunchInfo":"","userFirstLaunchInfo":"","area":""},'19eff',O0O00O0O0OO0000O0 )#line:196
    if not OOO000OO0O0O0O000 :#line:198
        return #line:199
    if int (OOO000OO0O0O0O000 .status_code )!=int (200 ):#line:200
        printf (O0OOO00OOOO00OO00 ,f'接口：{OOO000OO0O0O0O000.status_code}')#line:201
        return #line:202
    if int (OOO000OO0O0O0O000 .json ()['code'])==0 :#line:203
        if OOO000OO0O0O0O000 .json ()['data']['helpResult']==1 :#line:204
            OO0OO0OOO00O00OO0 ='✅助力成功'#line:205
            power_success .append (O0OOO00OOOO00OO00 )#line:206
        elif OOO000OO0O0O0O000 .json ()['data']['helpResult']==2 :#line:207
            OO0OO0OOO00O00OO0 ='❌火爆...助力失败'#line:208
            power_failure .append (O0OOO00OOOO00OO00 )#line:209
        elif OOO000OO0O0O0O000 .json ()['data']['helpResult']==3 :#line:210
            OO0OO0OOO00O00OO0 ='❌已经助力别人'#line:211
            power_failure .append (O0OOO00OOOO00OO00 )#line:212
        elif OOO000OO0O0O0O000 .json ()['data']['helpResult']==4 :#line:213
            OO0OO0OOO00O00OO0 ='❌助力次数用完了'#line:214
            power_failure .append (O0OOO00OOOO00OO00 )#line:215
        elif OOO000OO0O0O0O000 .json ()['data']['helpResult']==6 :#line:216
            OO0OO0OOO00O00OO0 ='❌已经助力过了'#line:217
            power_failure .append (O0OOO00OOOO00OO00 )#line:218
        else :#line:219
            OO0OO0OOO00O00OO0 ='❌未知状态'#line:220
            power_failure .append (O0OOO00OOOO00OO00 )#line:221
        if "助力成功"in OO0OO0OOO00O00OO0 :#line:222
            printf (O0OOO00OOOO00OO00 ,f"{OOO000OO0O0O0O000.status_code}【XDLY】助力-→{OOO000OO0O0O0O000.json()['data']['nickName']}|{OOO000OO0O0O0O000.json()['data']['helpResult']} {OO0OO0OOO00O00OO0} 🧑‍🤝‍🧑{len(power_success)}")#line:224
        else :#line:225
            printf (O0OOO00OOOO00OO00 ,f"{OOO000OO0O0O0O000.status_code}【XDLY】助力-→{OOO000OO0O0O0O000.json()['data']['nickName']}|{OOO000OO0O0O0O000.json()['data']['helpResult']} {OO0OO0OOO00O00OO0}")#line:226
    else :#line:227
        printf (O0OOO00OOOO00OO00 ,f"{OOO000OO0O0O0O000.json()['code']}  💔{OOO000OO0O0O0O000.json()['errMsg']}")#line:228
        not_login .append (O0OOO00OOOO00OO00 )#line:229
if __name__ =='__main__':#line:231
    try :#line:232
        cks =getCk #line:233
        if not cks :#line:234
            sys .exit ()#line:235
    except :#line:236
        print ("未获取到有效COOKIE,退出程序！")#line:237
        sys .exit ()#line:238
    inviter =remote_redis (f"inviteFissionBeforeHome",3 )#line:239
    cookie =cks [0 ]#line:240
    ua =userAgent ()#line:241
    response =H5API (ua ,cookie ,"drawFissionhelp",{"envType":1 ,"linkId":linkId ,"isJdApp":True ,"inviter":inviter ,"clientFirstLaunchInfo":"","userFirstLaunchInfo":"","area":""},'19eff').json ()#line:247
    if response ['success']==False and response ['code']==1000 :#line:248
        printf (cookie ,f"{response['errMsg']}")#line:249
        sys .exit ()#line:250
    if response ['data']['helpResult']==1 :#line:252
        printf (cookie ,f'✅助力作者成功 谢谢你 你是个好人！！！')#line:253
    else :#line:254
        printf (cookie ,f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:255
    response =H5API (ua ,cookie ,'drawFissionHome',{"envType":1 ,"linkId":linkId ,"inviter":"","sceneRestoreSkuId":"","sideType":""},'40393').json ()#line:256
    printf (cookie ,f'【XDLY】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 💰领现金进度{response["data"]["cashVo"]["amount"]}/{response["data"]["cashVo"]["totalAmount"]} ✅【助力码】:{response["data"]["inviter"]}')#line:257
    prizeNum2 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:258
    inviter =response ["data"]["inviter"]#line:259
    new_cks =list_of_groups (cks ,threadsNum )[::-1 ]#line:262
    for i ,cookies in enumerate (new_cks ,1 ):#line:263
        print (f"\n##############并发第{i}组ck##############")#line:264
        threads =[]#line:265
        proxies =get_proxies (threadsNum )#line:266
        proxies =proxies if proxies else None #line:267
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:268
        for index ,cookie in enumerate (cookies ,1 ):#line:269
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,get_proxy (proxies [index -1 ])if proxies else None ))#line:270
            threads .append (thead_one )#line:271
            power_num =len (power_success )#line:272
            if power_num >=int (number_restrictions ):#line:273
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:274
                sys .exit ()#line:275
        for t in threads :#line:276
            t .start ()#line:277
        for t in threads :#line:278
            t .join ()#line:279
        time .sleep (5 )#line:280
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')