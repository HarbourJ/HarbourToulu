#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDraw_nhj.py(年货节抽现金助力)
Author: HarbourJ
Date: 2024/1/17 00:00
TG: https://t.me/HarbourToulu
cron: 30 0 1,21 * * *
new Env('年货节抽现金助力');
ActivityEntry: https://pro.m.jd.com/mall/active/3WijvBWPdCirCBr72TzkyiPhgdxJ/index.html
变量：export inviteDrawPin="车头pin"
"""

import time ,requests ,sys ,re ,threading #line:15
from functools import partial #line:16
print =partial (print ,flush =True )#line:17
import warnings #line:18
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:19
try :#line:20
    from jd_sign import *#line:21
except ImportError as e :#line:22
    print (e )#line:23
    if "No module"in str (e ):#line:24
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")#line:25
    sys .exit ()#line:26
try :#line:27
    from jdCookie import get_cookies #line:28
    getCk =get_cookies ()#line:29
except :#line:30
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:31
    sys .exit ()#line:32
proxyType =""#line:37
neek =""#line:39
appkey =""#line:40
timeMode =False #line:41
pack =""#line:42
apikey =""#line:44
signxk =""#line:45
appKey =""#line:47
appSecret =""#line:48
uid =""#line:50
vkey =""#line:51
daili51 =""#line:53
proxyPoolIp =""#line:55
threadsNum =1 #line:58
number_restrictions =2000 #line:60
linkId ='gXqgDf0q9SKwNHnD4_ZokQ'#line:62
power_success =[]#line:63
power_failure =[]#line:64
not_login =[]#line:65
start =time .time ()#line:66
def printf (OO00OOOO00O0O00OO ,OOO0O0O00OOO00O00 ):#line:68
    try :#line:69
        O0OOOOOO00O0O00OO =re .compile (r'pt_pin=(.*?);').findall (OO00OOOO00O0O00OO )[0 ]#line:70
        O0OOOOOO00O0O00OO =unquote_plus (O0OOOOOO00O0O00OO )#line:71
    except IndexError :#line:72
        O0OOOOOO00O0O00OO =re .compile (r'pin=(.*?);').findall (OO00OOOO00O0O00OO )[0 ]#line:73
        O0OOOOOO00O0O00OO =unquote_plus (O0OOOOOO00O0O00OO )#line:74
    print (f"{str(datetime.now())[0:22]}->{O0OOOOOO00O0O00OO}->{OOO0O0O00OOO00O00}")#line:75
def list_of_groups (O0000O000O0OOOO00 ,O000O00OO000OO0O0 ):#line:77
    O0OO00OOOOOOO0000 =zip (*(iter (O0000O000O0OOOO00 ),)*O000O00OO000OO0O0 )#line:78
    OO000000O0OOO000O =[list (OO0OO00O000OO0O0O )for OO0OO00O000OO0O0O in O0OO00OOOOOOO0000 ]#line:79
    O00OO0OO0OO0O0OO0 =len (O0000O000O0OOOO00 )%O000O00OO000OO0O0 #line:80
    OO000000O0OOO000O .append (O0000O000O0OOOO00 [-O00OO0OO0OO0O0OO0 :])if O00OO0OO0OO0O0OO0 !=0 else OO000000O0OOO000O #line:81
    return OO000000O0OOO000O #line:82
def get_proxies (O000O0000O0OOO00O ):#line:84
    try :#line:86
        O00OO00OO00OOO0O0 =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:87
    except :#line:88
        O00OO00OO00OOO0O0 =requests .get ("https://ifconfig.me/").text #line:89
    print (f"获取当前IP:{O00OO00OO00OOO0O0}")#line:90
    if proxyType =="":#line:92
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:93
        return None #line:94
    elif proxyType =="1":#line:95
        print ("当前使用品易代理")#line:96
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={O00OO00OO00OOO0O0}")#line:98
        if timeMode :#line:101
            if not pack :#line:103
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:104
                sys .exit ()#line:105
            OOOOOOO00OO000000 =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={O000O0000O0OOO00O}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:106
        else :#line:107
            OOOOOOO00OO000000 =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={O000O0000O0OOO00O}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")#line:109
    elif proxyType =="2":#line:110
        print ("当前使用星空代理,1个ip一个店铺模式")#line:111
        OOOOOOO00OO000000 =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={O000O0000O0OOO00O}&format=txt&split=2&sign={signxk}")#line:112
    elif proxyType =="3":#line:113
        print ("当前使用小象代理")#line:114
        OOOOOOO00OO000000 =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:115
    elif proxyType =="4":#line:116
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:117
        OOOOOOO00OO000000 =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={O000O0000O0OOO00O}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:118
    elif proxyType =="5":#line:119
        time .sleep (1 )#line:120
        print ("当前使用51代理,1个ip一个店铺模式")#line:121
        OOOOOOO00OO000000 =requests .get (daili51 )#line:122
    elif proxyType =="6":#line:123
        print ("当前使用代理池工具")#line:124
        return [proxyPoolIp ]*O000O0000O0OOO00O #line:125
    else :#line:126
        print ("当前选择代理无效,默认使用本地ip")#line:127
        return None #line:128
    OOO000O0O0OOOO0OO =OOOOOOO00OO000000 .text #line:130
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',OOO000O0O0OOOO0OO )is None :#line:132
        print (OOO000O0O0OOOO0OO )#line:133
        return None #line:135
    OOO000O0O0OOOO0OO =OOO000O0O0OOOO0OO .split ('\r\n')#line:136
    OOO000O0O0OOOO0OO =[OOO00OOOO0OO000O0 for OOO00OOOO0OO000O0 in OOO000O0O0OOOO0OO if OOO00OOOO0OO000O0 ]#line:137
    return OOO000O0O0OOOO0OO #line:139
def convert_ms_to_hours_minutes (O00O00OO00O0O00O0 ):#line:141
    O00O0000O0OOO00OO =O00O00OO00O0O00O0 //1000 #line:142
    O000O0OO0000O00O0 ,O00O0000O0OOO00OO =divmod (O00O0000O0OOO00OO ,60 )#line:143
    OO00O0OOO0O0OOO0O ,O000O0OO0000O00O0 =divmod (O000O0OO0000O00O0 ,60 )#line:144
    return f'{OO00O0OOO0O0OOO0O}h{O000O0OO0000O00O0}m'#line:145
def get_h5st_body (OO0000O00O00000OO ,OO0000OO00OOO0O0O ,OOOOO00OOO0OOO0OO ,OOO0OO00OO0OO0OO0 ,O0O00O0000OOOOO0O ):#line:147
    try :#line:148
        OO0O0OOOOOOOOO0OO =re .compile (r'pt_pin=(.*?);').findall (OO0000OO00OOO0O0O )[0 ]#line:149
        OO0O0OOOOOOOOO0OO =unquote_plus (OO0O0OOOOOOOOO0OO )#line:150
    except IndexError :#line:151
        OO0O0OOOOOOOOO0OO =re .compile (r'pin=(.*?);').findall (OO0000OO00OOO0O0O )[0 ]#line:152
        OO0O0OOOOOOOOO0OO =unquote_plus (OO0O0OOOOOOOOO0OO )#line:153
    O0OO00OO0OO0OO00O =OO0000O00O00000OO .split (";")[2 ]#line:154
    O0O00O0000OOOOO0O ={"appId":OOO0OO00OO0OO0OO0 ,"appid":"activities_platform","ua":OO0000O00O00000OO ,"pin":OO0O0OOOOOOOOO0OO ,"functionId":OOOOO00OOO0OOO0OO ,"body":O0O00O0000OOOOO0O ,"expand":{"url":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","og":"https://pro.m.jd.com"},"clientVersion":O0OO00OO0OO0OO00O ,"version":"4.1"}#line:168
    try :#line:169
        import base64 #line:170
        OOO00O0OOO0OOO0OO ="aHR0cDovLzEyMS4zNy4yMDcuMTk1OjMwMDEvYXBpL2g1c3Q="#line:171
        O0000O0O00O0O0OO0 =json .dumps (O0O00O0000OOOOO0O )#line:172
        O0OOO0OO00O0OO00O ={'Content-Type':'application/json'}#line:175
        OO0OOO0OOOOO00000 =requests .request ("POST",base64 .b64decode (OOO00O0OOO0OOO0OO .encode ('utf-8')).decode ('utf-8'),headers =O0OOO0OO00O0OO00O ,timeout =10 ,data =O0000O0O00O0O0OO0 ).json ()#line:176
        if OO0OOO0OOOOO00000 ['code']==200 :#line:177
            return OO0OOO0OOOOO00000 ['data']#line:179
        else :#line:180
            printf (OO0000OO00OOO0O0O ,f"调用远程h5st接口失败1")#line:181
            return #line:182
    except Exception as O000O0000OO0OOOOO :#line:183
        printf (OO0000OO00OOO0O0O ,f"调用远程h5st接口失败2:{O000O0000OO0OOOOO}")#line:184
        get_h5st_body (OO0000O00O00000OO ,OO0000OO00OOO0O0O ,OOOOO00OOO0OOO0OO ,OOO0OO00OO0OO0OO0 ,O0O00O0000OOOOO0O )#line:185
        return #line:186
def H5API (O000O0OO00O000000 ,O000O00OOOO0000OO ,OOO0O0O0O0OO0O000 ,OO0OOO0OO0OOO0O00 ,O00O0OOO0000000O0 ,proxies =None ):#line:188
    OOO0OOO00O000O000 ="https://api.m.jd.com"#line:189
    O0OO0000OO0OOOO0O ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":O000O00OOOO0000OO ,"User-Agent":O000O0OO00O000000 ,}#line:201
    O0O0O00OO0000OO0O =get_h5st_body (O000O0OO00O000000 ,O000O00OOOO0000OO ,OOO0O0O0O0OO0O000 ,O00O0OOO0000000O0 ,OO0OOO0OO0OOO0O00 )#line:202
    if not O0O0O00OO0000OO0O :#line:203
        return #line:204
    OO0OOO0OO0OOO0O00 =O0O0O00OO0000OO0O #line:205
    try :#line:206
        O0000O000O000O000 =requests .post (OOO0OOO00O000O000 ,headers =O0OO0000OO0OOOO0O ,data =OO0OOO0OO0OOO0O00 ,timeout =5 ,proxies =proxies )#line:207
    except Exception as OOO000OOO0000OO00 :#line:208
        printf (O000O00OOOO0000OO ,f"H5API Error:{str(OOO000OOO0000OO00)}")#line:209
        return #line:210
    if O0000O000O000O000 .status_code ==200 :#line:211
        return O0000O000O000O000 #line:212
    else :#line:213
        printf (O000O00OOOO0000OO ,O0000O000O000O000 .status_code )#line:214
def Result (OOO00000O0OO0O0OO ,OOOO000OO0OO00OO0 ,O00OO000O00O000O0 ,OO00OOO0O0OO000O0 ):#line:216
    if "wskey"in OOOO000OO0OO00OO0 :#line:217
        from wskey import nt_wskey #line:218
        O0O00O0000000O0O0 =nt_wskey (OOOO000OO0OO00OO0 )#line:219
        OOOO000OO0OO00OO0 =O0O00O0000000O0O0 if O0O00O0000000O0O0 else OOOO000OO0OO00OO0 #line:220
    if OOOO000OO0OO00OO0 [-1 ]!=";":#line:221
        OOOO000OO0OO00OO0 +=";"#line:222
    O000O0OOOO00000OO =H5API (OOO00000O0OO0O0OO ,OOOO000OO0OO00OO0 ,"inviteFissionhelp",{'linkId':linkId ,"isJdApp":True ,'inviter':O00OO000O00O000O0 ,"clientFirstLaunchInfo":"","userFirstLaunchInfo":""},'c5389',OO00OOO0O0OO000O0 )#line:223
    if not O000O0OOOO00000OO :#line:225
        return #line:226
    if int (O000O0OOOO00000OO .status_code )!=int (200 ):#line:227
        printf (OOOO000OO0OO00OO0 ,f'接口：{O000O0OOOO00000OO.status_code}')#line:228
        return #line:229
    if int (O000O0OOOO00000OO .json ()['code'])==0 :#line:230
        if O000O0OOOO00000OO .json ()['data']['helpResult']==1 :#line:231
            OO00OO00OOOOOOOO0 ='✅助力成功'#line:232
            power_success .append (OOOO000OO0OO00OO0 )#line:233
        elif O000O0OOOO00000OO .json ()['data']['helpResult']==2 :#line:234
            OO00OO00OOOOOOOO0 ='❌火爆...助力失败'#line:235
            power_failure .append (OOOO000OO0OO00OO0 )#line:236
        elif O000O0OOOO00000OO .json ()['data']['helpResult']==3 :#line:237
            OO00OO00OOOOOOOO0 ='❌已经助力别人'#line:238
            power_failure .append (OOOO000OO0OO00OO0 )#line:239
        elif O000O0OOOO00000OO .json ()['data']['helpResult']==4 :#line:240
            OO00OO00OOOOOOOO0 ='❌助力次数用完了'#line:241
            power_failure .append (OOOO000OO0OO00OO0 )#line:242
        elif O000O0OOOO00000OO .json ()['data']['helpResult']==6 :#line:243
            OO00OO00OOOOOOOO0 ='❌已经助力过了'#line:244
            power_failure .append (OOOO000OO0OO00OO0 )#line:245
        else :#line:246
            OO00OO00OOOOOOOO0 ='❌未知状态'#line:247
            power_failure .append (OOOO000OO0OO00OO0 )#line:248
        printf (OOOO000OO0OO00OO0 ,f"{O000O0OOOO00000OO.status_code}【JDPDD】助力-→{O000O0OOOO00000OO.json()['data']['nickName']}|{O000O0OOOO00000OO.json()['data']['helpResult']} {OO00OO00OOOOOOOO0}")#line:249
    else :#line:250
        printf (OOOO000OO0OO00OO0 ,f"{O000O0OOOO00000OO.json()['code']}  💔{O000O0OOOO00000OO.json()['errMsg']}")#line:251
        not_login .append (OOOO000OO0OO00OO0 )#line:252
if __name__ =='__main__':#line:254
    try :#line:255
        cks =getCk #line:256
        if not cks :#line:257
            sys .exit ()#line:258
    except :#line:259
        print ("未获取到有效COOKIE,退出程序！")#line:260
        sys .exit ()#line:261
    inviter =remote_redis (f"inviteFissionhelp",3 )#line:262
    cookie =cks [0 ]#line:263
    ua =userAgent ()#line:264
    response =H5API (ua ,cookie ,"inviteFissionhelp",{'linkId':linkId ,"isJdApp":True ,'inviter':inviter ,"clientFirstLaunchInfo":"","userFirstLaunchInfo":""},'c5389').json ()#line:265
    printf (cookie ,response )#line:266
    if response ['success']==False and response ['code']==1000 :#line:267
        printf (cookie ,f"{response['errMsg']}")#line:268
        sys .exit ()#line:269
    if response ['data']['helpResult']==1 :#line:270
        printf (cookie ,f'✅助力作者成功 谢谢你 你是个好人！！！')#line:271
    else :#line:272
        printf (cookie ,f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:273
    response =H5API (ua ,cookie ,'inviteFissionHome',{'linkId':linkId ,"inviter":""},'eb67b').json ()#line:274
    printf (cookie ,f'【JDPDD】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 💰领现金进度{response["data"]["cashVo"]["amount"]}/{response["data"]["cashVo"]["totalAmount"]} ✅【助力码】:{response["data"]["inviter"]}')#line:275
    prizeNum2 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:277
    inviter =response ["data"]["inviter"]#line:278
    time .sleep (1 )#line:280
    new_cks =list_of_groups (cks ,threadsNum )[:]#line:281
    for i ,cookies in enumerate (new_cks ,1 ):#line:282
        print (f"\n##############并发第{i}组ck##############")#line:283
        threads =[]#line:284
        proxies =get_proxies (threadsNum )#line:285
        proxies =proxies if proxies else None #line:286
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:287
        for index ,cookie in enumerate (cookies ,1 ):#line:288
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,{"http":f"http://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}","https":f"https://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}"}if proxies else None ))#line:289
            threads .append (thead_one )#line:290
            power_num =len (power_success )#line:291
            if power_num >=int (number_restrictions ):#line:293
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:294
                sys .exit ()#line:295
        for t in threads :#line:296
            t .start ()#line:297
            time .sleep (0.05 )#line:298
        for t in threads :#line:299
            t .join ()#line:300
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')