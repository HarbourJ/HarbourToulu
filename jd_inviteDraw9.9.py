#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDraw9.9.py(京喜自营抽奖助力)
Author: HarbourJ
Date: 2024/3/27 00:00
TG: https://t.me/HarbourToulu
cron: 30 0 0,19,22 * * *
new Env('京喜自营抽奖助力');
ActivityEntry: 京东-9.9包邮日-1分钱京喜自营好礼
"""

import time, requests, sys, json, re, threading
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
number_restrictions = 10000

power_success = []
power_failure = []
not_login= []
start = time.time()

def printf (OOO0OOOO0O0OO0O0O ,O0OO0O0O000OOOO0O ):#line:1
    try :#line:2
        OO00OO000O00O0000 =re .compile (r'pt_pin=(.*?);').findall (OOO0OOOO0O0OO0O0O )[0 ]#line:3
        OO00OO000O00O0000 =unquote_plus (OO00OO000O00O0000 )#line:4
    except IndexError :#line:5
        OO00OO000O00O0000 =re .compile (r'pin=(.*?);').findall (OOO0OOOO0O0OO0O0O )[0 ]#line:6
        OO00OO000O00O0000 =unquote_plus (OO00OO000O00O0000 )#line:7
    print (f"{str(datetime.now())[0:22]}->{OO00OO000O00O0000}->{O0OO0O0O000OOOO0O}")#line:8
def list_of_groups (O0O0000O0O0000OOO ,O0000000O0000000O ):#line:10
    OO00O0OO00OOOO00O =zip (*(iter (O0O0000O0O0000OOO ),)*O0000000O0000000O )#line:11
    O0OOOO0OO0O000OO0 =[list (OOOO0O00O00O00O0O )for OOOO0O00O00O00O0O in OO00O0OO00OOOO00O ]#line:12
    OOO0OOO0000OO0OO0 =len (O0O0000O0O0000OOO )%O0000000O0000000O #line:13
    O0OOOO0OO0O000OO0 .append (O0O0000O0O0000OOO [-OOO0OOO0000OO0OO0 :])if OOO0OOO0000OO0OO0 !=0 else O0OOOO0OO0O000OO0 #line:14
    return O0OOOO0OO0O000OO0 #line:15
def get_proxies (O000OOO0O0OO00OOO ):#line:17
    try :#line:19
        O00000OO0O0O0OOOO =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:20
    except :#line:21
        O00000OO0O0O0OOOO =requests .get ("https://ifconfig.me/ip").text #line:22
    print (f"获取当前IP:{O00000OO0O0O0OOOO}")#line:23
    if proxyType =="":#line:25
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:26
        return None #line:27
    elif proxyType =="1":#line:28
        print ("当前使用品易代理")#line:29
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={O00000OO0O0O0OOOO}")#line:31
        if timeMode :#line:34
            if not pack :#line:36
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:37
                sys .exit ()#line:38
            OOO00OOOO00OO0O0O =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={O000OOO0O0OO00OOO}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:39
        else :#line:40
            OOO00OOOO00OO0O0O =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={O000OOO0O0OO00OOO}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")#line:42
    elif proxyType =="2":#line:43
        print ("当前使用星空代理,1个ip一个店铺模式")#line:44
        OOO00OOOO00OO0O0O =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={O000OOO0O0OO00OOO}&format=txt&split=2&sign={signxk}")#line:45
    elif proxyType =="3":#line:46
        print ("当前使用小象代理")#line:47
        OOO00OOOO00OO0O0O =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:48
    elif proxyType =="4":#line:49
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:50
        OOO00OOOO00OO0O0O =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={O000OOO0O0OO00OOO}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:51
    elif proxyType =="5":#line:52
        time .sleep (1 )#line:53
        print ("当前使用51代理,1个ip一个店铺模式")#line:54
        OOO00OOOO00OO0O0O =requests .get (daili51 )#line:55
    elif proxyType =="6":#line:56
        print ("当前使用代理池工具")#line:57
        return [proxyPoolIp ]*O000OOO0O0OO00OOO #line:58
    else :#line:59
        print ("当前选择代理无效,默认使用本地ip")#line:60
        return None #line:61
    OO0O00OOO000O0000 =OOO00OOOO00OO0O0O .text #line:63
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',OO0O00OOO000O0000 )is None :#line:65
        print (OO0O00OOO000O0000 )#line:66
        return None #line:68
    OO0O00OOO000O0000 =[O00OO000000O000OO .strip ()for O00OO000000O000OO in OO0O00OOO000O0000 .splitlines ()if O00OO000000O000OO .strip ()]#line:69
    OO0O00OOO000O0000 =[OOOOO0O0O0000O00O for OOOOO0O0O0000O00O in OO0O00OOO000O0000 if OOOOO0O0O0000O00O ]#line:70
    return OO0O00OOO000O0000 #line:73
def convert_ms_to_hours_minutes (OO0OO00OO000O0O00 ):#line:75
    O000OO0000000O00O =OO0OO00OO000O0O00 //1000 #line:76
    O0OO0OO00OO0OOOO0 ,O000OO0000000O00O =divmod (O000OO0000000O00O ,60 )#line:77
    O00000O0OO0OOOOOO ,O0OO0OO00OO0OOOO0 =divmod (O0OO0OO00OO0OOOO0 ,60 )#line:78
    return f'{O00000O0OO0OOOOOO}h{O0OO0OO00OO0OOOO0}m'#line:79
def get_h5st_body (O0O0O00O0O000O0OO ,O0OOO00O000OOOO00 ,O0O00000OO0O00000 ,OOOO0OO0O000000OO ,O00000OOOO0O0000O ):#line:81
    try :#line:82
        O0OO000OO00O0O00O =re .compile (r'pt_pin=(.*?);').findall (O0OOO00O000OOOO00 )[0 ]#line:83
        O0OO000OO00O0O00O =unquote_plus (O0OO000OO00O0O00O )#line:84
    except IndexError :#line:85
        O0OO000OO00O0O00O =re .compile (r'pin=(.*?);').findall (O0OOO00O000OOOO00 )[0 ]#line:86
        O0OO000OO00O0O00O =unquote_plus (O0OO000OO00O0O00O )#line:87
    OOOO000OOOO00O00O =O0O0O00O0O000O0OO .split (";")[2 ]#line:88
    O00000OOOO0O0000O ={"appId":OOOO0OO0O000000OO ,"appid":"signed_wh5","ua":O0O0O00O0O000O0OO ,"pin":O0OO000OO00O0O00O ,"functionId":O0O00000OO0O00000 ,"body":O00000OOOO0O0000O ,"clientVersion":"1.0.0","client":"wh5","version":"4.4"}#line:99
    try :#line:100
        import base64 #line:101
        OOOOO00OOO0O00000 ="aHR0cDovLzEuOTQuOC4yNDQ6MzAwMi9hcGkvaDVzdA=="#line:102
        O0OO00OO0OO00O0OO =json .dumps (O00000OOOO0O0000O )#line:103
        O0OOOOO00OOOOO00O ={'Content-Type':'application/json'}#line:106
        O00O0OO00O000OO0O =requests .request ("POST",base64 .b64decode (OOOOO00OOO0O00000 .encode ('utf-8')).decode ('utf-8'),headers =O0OOOOO00OOOOO00O ,timeout =10 ,data =O0OO00OO0OO00O0OO ).json ()#line:107
        if O00O0OO00O000OO0O ['code']==200 :#line:108
            return O00O0OO00O000OO0O ['data']#line:110
        else :#line:111
            printf (O0OOO00O000OOOO00 ,f"调用远程h5st接口失败1")#line:112
            return #line:113
    except Exception as OO0OO0OO0OOOO0OO0 :#line:114
        printf (O0OOO00O000OOOO00 ,f"调用远程h5st接口失败2:{OO0OO0OO0OOOO0OO0}")#line:115
        get_h5st_body (O0O0O00O0O000O0OO ,O0OOO00O000OOOO00 ,O0O00000OO0O00000 ,OOOO0OO0O000000OO ,O00000OOOO0O0000O )#line:116
        return #line:117
def H5API (OO0OO0O00OO00O000 ,OO00OO0O00OOOO0OO ,O00OOO0O000000OOO ,OO0000O0O0OO0000O ,O0O00OOO00OOO0O0O ,proxies =None ):#line:119
    O0OO0OO000OOOOO00 ="https://api.m.jd.com"#line:120
    O0000OO00O0000O00 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-CN,zh;q=0.9","Content-Type":"application/x-www-form-urlencoded","Referer":"https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html","Origin":"https://pro.m.jd.com","Cookie":OO00OO0O00OOOO0OO ,"User-Agent":OO0OO0O00OO00O000 ,"X-Referer-Page":"https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html","X-Rp-Client":"h5_1.0.0"}#line:132
    OOO0000OOOOOO00OO =get_h5st_body (OO0OO0O00OO00O000 ,OO00OO0O00OOOO0OO ,O00OOO0O000000OOO ,O0O00OOO00OOO0O0O ,OO0000O0O0OO0000O )#line:133
    if not OOO0000OOOOOO00OO :#line:134
        return #line:135
    OO0000O0O0OO0000O =OOO0000OOOOOO00OO +f"&uuid=&d_model=0-2-999&osVersion=17.3"#line:136
    try :#line:137
        OO00OOO0O00O0OOOO =requests .post (O0OO0OO000OOOOO00 ,headers =O0000OO00O0000O00 ,data =OO0000O0O0OO0000O ,timeout =5 ,proxies =proxies )#line:138
    except Exception as OO0OO0O000000OO0O :#line:139
        printf (OO00OO0O00OOOO0OO ,f"H5API Error:{str(OO0OO0O000000OO0O)}")#line:140
        return #line:141
    if OO00OOO0O00O0OOOO .status_code ==200 :#line:142
        return OO00OOO0O00O0OOOO #line:143
    else :#line:144
        printf (OO00OO0O00OOOO0OO ,OO00OOO0O00O0OOOO .status_code )#line:145
def gen_invite (OO000OO0O00O000O0 ,OO0OO000OOOO00OOO ,proxies =None ):#line:147
    OOO00O0OOOOOOOO0O ="https://api.m.jd.com"#line:148
    OO000OOO0OO0O0000 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-CN,zh;q=0.9","Content-Type":"application/x-www-form-urlencoded","Referer":"https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html","Origin":"https://pro.m.jd.com","Cookie":OO0OO000OOOO00OOO ,"User-Agent":OO000OO0O00O000O0 }#line:158
    O0O0OOO0OO0000OO0 ="functionId=jx_party_invite&appid=signed_wh5&body=%7B%22channel%22%3A%22jkl%22%7D"#line:159
    try :#line:160
        try :#line:161
            O00OO000O000O000O =requests .post (OOO00O0OOOOOOOO0O ,headers =OO000OOO0OO0O0000 ,data =O0O0OOO0OO0000OO0 ,timeout =5 ,proxies =proxies )#line:162
        except Exception as OO00OOOOOO00OOO0O :#line:163
            printf (OO0OO000OOOO00OOO ,f"gen_invite Error1:{str(OO00OOOOOO00OOO0O)}")#line:164
            return #line:165
        if O00OO000O000O000O .status_code ==200 :#line:166
            if "inviteCode"in O00OO000O000O000O .text :#line:167
                return O00OO000O000O000O .json ()["data"]["result"]["inviteCode"]#line:168
            elif "未登录"in O00OO000O000O000O .text :#line:169
                printf (OO0OO000OOOO00OOO ,"⚠️车头账号失效！请手动关闭程序！")#line:170
            else :#line:171
                printf (OO0OO000OOOO00OOO ,"⚠️疑似黑号,获取助力码失败！请手动关闭程序！")#line:172
        else :#line:173
            printf (OO0OO000OOOO00OOO ,O00OO000O000O000O .status_code )#line:174
    except Exception as OO00OOOOOO00OOO0O :#line:175
        printf (OO0OO000OOOO00OOO ,f"gen_invite Error2:{str(OO00OOOOOO00OOO0O)}")#line:176
        return #line:177
def genRandomString (i11i1i =32 ,Iilill ="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"):#line:179
    OOOOOOOO0O0000OO0 =len (Iilill )#line:180
    OO00000O00OO0O0O0 =""#line:181
    for OO0OOO0O00O0OO0O0 in range (i11i1i ):#line:182
        OO00000O00OO0O0O0 +=Iilill [random .randint (0 ,OOOOOOOO0O0000OO0 -1 )]#line:183
    return OO00000O00OO0O0O0 #line:184
def Result (OO00OO00OOO0O0OOO ,OO0OO0OO0000O0OO0 ,OOOOO00O0O0O00OOO ,O000OOOO0OOO0000O ):#line:186
    OOO00OO0000O00000 =genRandomString (300 ,"0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")#line:187
    OO0O0OOO0O00OO0OO =H5API (OO00OO00OOO0O0OOO ,OO0OO0OO0000O0OO0 ,"jx_party_assist",{"inviteCode":OOOOO00O0O0O00OOO ,"areaInfo":"","unpl":OOO00OO0000O00000 ,"qdPageId":"MO-J2011-1","mdClickId":"Babel_dev_other_11lotterystart"},'a525b',O000OOOO0OOO0000O )#line:188
    if not OO0O0OOO0O00OO0OO :#line:189
        return #line:190
    if int (OO0O0OOO0O00OO0OO .status_code )!=int (200 ):#line:191
        printf (OO0OO0OO0000O0OO0 ,f'接口：{OO0O0OOO0O00OO0OO.status_code}')#line:192
        return #line:193
    if int (OO0O0OOO0O00OO0OO .json ()['code'])==0 :#line:194
        if 'result'in OO0O0OOO0O00OO0OO .text :#line:195
            O000OOO00OOOOO0OO ='✅助力成功'#line:196
            power_success .append (OO0OO0OO0000O0OO0 )#line:197
        elif OO0O0OOO0O00OO0OO .json ()['data']['bizCode']==-9007 :#line:198
            O000OOO00OOOOO0OO ='❌火爆...助力失败'#line:199
            power_failure .append (OO0OO0OO0000O0OO0 )#line:200
        elif OO0O0OOO0O00OO0OO .json ()['data']['bizCode']==-9004 :#line:201
            O000OOO00OOOOO0OO ='❌不能给自己助力呦～'#line:202
            power_failure .append (OO0OO0OO0000O0OO0 )#line:203
        elif OO0O0OOO0O00OO0OO .json ()['data']['bizCode']==-102 :#line:204
            O000OOO00OOOOO0OO ='💔未登录'#line:205
            not_login .append (OO0OO0OO0000O0OO0 )#line:206
        elif OO0O0OOO0O00OO0OO .json ()['data']['bizCode']==-9010 :#line:207
            O000OOO00OOOOO0OO ='❌已经助力过了'#line:208
            power_failure .append (OO0OO0OO0000O0OO0 )#line:209
        else :#line:210
            O000OOO00OOOOO0OO =OO0O0OOO0O00OO0OO .json ()['data']['bizMsg']#line:211
            power_failure .append (OO0OO0OO0000O0OO0 )#line:212
        printf (OO0OO0OO0000O0OO0 ,f"{OO0O0OOO0O00OO0OO.status_code} 助力结果|{O000OOO00OOOOO0OO}")#line:213
    elif int (OO0O0OOO0O00OO0OO .json ()['code'])==405 :#line:214
        printf (OO0OO0OO0000O0OO0 ,f"{OO0O0OOO0O00OO0OO.json()['code']}  ❌{OO0O0OOO0O00OO0OO.json()['errMsg']}")#line:215
    else :#line:216
        printf (OO0OO0OO0000O0OO0 ,f"{OO0O0OOO0O00OO0OO.json()['code']}  💔{OO0O0OOO0O00OO0OO.json()['errMsg']}")#line:217
        not_login .append (OO0OO0OO0000O0OO0 )#line:218
if __name__ =='__main__':#line:220
    try :#line:221
        cks =getCk #line:222
        if not cks :#line:223
            sys .exit ()#line:224
    except :#line:225
        print ("未获取到有效COOKIE,退出程序！")#line:226
        sys .exit ()#line:227
    inviter =remote_redis (f"inviteFission99",3 )#line:228
    cookie =cks [0 ]#line:229
    ua =userAgent ()#line:230
    response =H5API (ua ,cookie ,"jx_party_assist",{"inviteCode":inviter ,"areaInfo":"","unpl":genRandomString (300 ,"0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"),"qdPageId":"MO-J2011-1","mdClickId":"Babel_dev_other_11lotterystart"},'a525b')#line:231
    if int (response .status_code )!=200 :#line:232
        printf (cookie ,f'接口：{response.status_code}')#line:233
        sys .exit ()#line:234
    if int (response .json ()['code'])==0 :#line:235
        if 'result'in response .text :#line:236
            printf (cookie ,f'✅助力作者成功 谢谢你 你是个好人！！！')#line:237
        else :#line:238
            printf (cookie ,f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:239
    else :#line:240
        printf (cookie ,f"{response.json()['code']}  💔{response.json()['errMsg']}")#line:241
    time .sleep (0.1 )#line:242
    inviteCode =gen_invite (ua ,cookie )#line:243
    if not inviteCode :#line:244
        inviter #line:245
    else :#line:246
        printf (cookie ,f'✅【助力码】:{inviteCode}')#line:247
        inviter =inviteCode #line:248
    new_cks =list_of_groups (cks ,threadsNum )[:]#line:249
    for i ,cookies in enumerate (new_cks ,1 ):#line:250
        print (f"\n##############并发第{i}组ck##############")#line:251
        threads =[]#line:252
        proxies =get_proxies (threadsNum )#line:253
        proxies =proxies if proxies else None #line:254
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:255
        for index ,cookie in enumerate (cookies ,1 ):#line:256
            cookie =cookie .split (';---')[0 ]+';'#line:257
            if proxies :#line:258
                if "@"in proxies [index -1 ]:#line:259
                    _O0O0000000OO0000O ={"http":f"http://{proxies[index-1].split('@')[0]}@{proxies[index-1].split('@')[1]}","https":f"https://{proxies[index-1].split('@')[0]}@{proxies[index-1].split('@')[1]}"}#line:260
                else :#line:261
                    _O0O0000000OO0000O ={"http":f"http://{proxies[index - 1].split(':')[0]}:{proxies[index - 1].split(':')[1]}","https":f"https://{proxies[index - 1].split(':')[0]}:{proxies[index - 1].split(':')[1]}"}#line:263
            else :#line:264
                _O0O0000000OO0000O =None #line:265
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,_O0O0000000OO0000O ))#line:266
            threads .append (thead_one )#line:267
            power_num =len (power_success )#line:268
            if power_num >=int (number_restrictions ):#line:269
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:270
                sys .exit ()#line:271
        for t in threads :#line:272
            t .start ()#line:273
        for t in threads :#line:274
            t .join ()#line:275
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')