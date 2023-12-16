#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDraw.py(邀好友抽现金助力)
Author: HarbourJ
Date: 2023/3/15 10:00
TG: https://t.me/HarbourToulu
cron: 30 0 0,20 * * *
new Env('邀好友抽现金助力');
ActivityEntry: https://prodev.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html
变量：export inviteDrawPin="车头pin"
"""

import time ,requests ,sys ,re ,threading ,os ,random #line:1
from functools import partial #line:2
print =partial (print ,flush =True )#line:3
import warnings #line:4
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:5
try :#line:6
    from jd_sign import *#line:7
except ImportError as e :#line:8
    print (e )#line:9
    if "No module"in str (e ):#line:10
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")#line:11
    sys .exit ()#line:12
try :#line:13
    from jdCookie import get_cookies #line:14
    getCk =get_cookies ()#line:15
except :#line:16
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:17
    sys .exit ()#line:18
proxyType =""#line:23
neek =""#line:25
appkey =""#line:26
timeMode =False #line:27
pack =""#line:28
apikey =""#line:30
signxk =""#line:31
appKey =""#line:33
appSecret =""#line:34
uid =""#line:36
vkey =""#line:37
daili51 =""#line:39
proxyPoolIp =""#line:41
threadsNum =1 #line:43
number_restrictions =5000 #line:45
linkIds =['Wvzc_VpNTlSkiQdHT8r7QA','3orGfh1YkwNLksxOcN8zWQ']#line:47
power_success =[]#line:48
power_failure =[]#line:49
not_login =[]#line:50
start =time .time ()#line:51
def printf (OOOOO0000OO0OOOOO ,O0O00O0O000OOOOO0 ):#line:53
    try :#line:54
        O0OO0O0O00000OO0O =re .compile (r'pt_pin=(.*?);').findall (OOOOO0000OO0OOOOO )[0 ]#line:55
        O0OO0O0O00000OO0O =unquote_plus (O0OO0O0O00000OO0O )#line:56
    except IndexError :#line:57
        O0OO0O0O00000OO0O =re .compile (r'pin=(.*?);').findall (OOOOO0000OO0OOOOO )[0 ]#line:58
        O0OO0O0O00000OO0O =unquote_plus (O0OO0O0O00000OO0O )#line:59
    print (f"{str(datetime.now())[0:22]}->{O0OO0O0O00000OO0O}->{O0O00O0O000OOOOO0}")#line:60
def list_of_groups (OOOOO00OO0O0O0O0O ,OO0O0OOOOO0OOO00O ):#line:62
    O0OOO0O0OOOOOOO00 =zip (*(iter (OOOOO00OO0O0O0O0O ),)*OO0O0OOOOO0OOO00O )#line:63
    OOOO00OOO00O0O0OO =[list (O00000O0O00000000 )for O00000O0O00000000 in O0OOO0O0OOOOOOO00 ]#line:64
    OOO0OOOO0OO0O00OO =len (OOOOO00OO0O0O0O0O )%OO0O0OOOOO0OOO00O #line:65
    OOOO00OOO00O0O0OO .append (OOOOO00OO0O0O0O0O [-OOO0OOOO0OO0O00OO :])if OOO0OOOO0OO0O00OO !=0 else OOOO00OOO00O0O0OO #line:66
    return OOOO00OOO00O0O0OO #line:67
def get_proxies (O0O000OOOO00O00O0 ):#line:69
    try :#line:71
        OOOOOO0OOOOOOOOO0 =requests .get ("https://pycn.yapi.py.cn/get_client_ip").json ()["ret_data"]#line:72
    except :#line:73
        OOOOOO0OOOOOOOOO0 =requests .get ("https://ifconfig.me/").text #line:74
    print (f"获取当前IP:{OOOOOO0OOOOOOOOO0}")#line:75
    if proxyType =="":#line:77
        print ('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')#line:78
        return None #line:79
    elif proxyType =="1":#line:80
        print ("当前使用品易代理")#line:81
        requests .get (f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={OOOOOO0OOOOOOOOO0}")#line:83
        if timeMode :#line:86
            if not pack :#line:88
                print (f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")#line:89
                sys .exit ()#line:90
            OO000000O0OOO0000 =requests .get (f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={O0O000OOOO00O00O0}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")#line:91
        else :#line:92
            OO000000O0OOO0000 =requests .get (f"http://zltiqu.pyhttp.taolop.com/getip?count={O0O000OOOO00O00O0}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")#line:94
    elif proxyType =="2":#line:95
        print ("当前使用星空代理,1个ip一个店铺模式")#line:96
        OO000000O0OOO0000 =requests .get (f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={O0O000OOOO00O00O0}&format=txt&split=2&sign={signxk}")#line:97
    elif proxyType =="3":#line:98
        print ("当前使用小象代理")#line:99
        OO000000O0OOO0000 =requests .get (f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")#line:100
    elif proxyType =="4":#line:101
        print ("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")#line:102
        OO000000O0OOO0000 =requests .get (f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={O0O000OOOO00O00O0}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")#line:103
    elif proxyType =="5":#line:104
        time .sleep (1 )#line:105
        print ("当前使用51代理,1个ip一个店铺模式")#line:106
        OO000000O0OOO0000 =requests .get (daili51 )#line:107
    elif proxyType =="6":#line:108
        print ("当前使用代理池工具")#line:109
        return [proxyPoolIp ]*O0O000OOOO00O00O0 #line:110
    else :#line:111
        print ("当前选择代理无效,默认使用本地ip")#line:112
        return None #line:113
    OOOOO000O0OO00O00 =OO000000O0OOO0000 .text #line:115
    if re .match (r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',OOOOO000O0OO00O00 )is None :#line:117
        print (OOOOO000O0OO00O00 )#line:118
        return None #line:120
    OOOOO000O0OO00O00 =OOOOO000O0OO00O00 .split ('\r\n')#line:121
    OOOOO000O0OO00O00 =[OOO0OOO0000OOOO0O for OOO0OOO0000OOOO0O in OOOOO000O0OO00O00 if OOO0OOO0000OOOO0O ]#line:122
    return OOOOO000O0OO00O00 #line:124
def convert_ms_to_hours_minutes (O00OOOO0O00OOO00O ):#line:126
    O00OO0O00000O00OO =O00OOOO0O00OOO00O //1000 #line:127
    OO0000O000O0O000O ,O00OO0O00000O00OO =divmod (O00OO0O00000O00OO ,60 )#line:128
    OOOO00O0O00000O0O ,OO0000O000O0O000O =divmod (OO0000O000O0O000O ,60 )#line:129
    return f'{OOOO00O0O00000O0O}h{OO0000O000O0O000O}m'#line:130
def get_h5st_body (O0OOO000OO000OO0O ,O0000O0OOOO0OO000 ,O000OOO00OO0O0OO0 ,O0O0O0O0000O0OOO0 ,OO00OO0OO000OOOOO ):#line:132
    try :#line:133
        OO000OOO000OOO0O0 =re .compile (r'pt_pin=(.*?);').findall (O0000O0OOOO0OO000 )[0 ]#line:134
        OO000OOO000OOO0O0 =unquote_plus (OO000OOO000OOO0O0 )#line:135
    except IndexError :#line:136
        OO000OOO000OOO0O0 =re .compile (r'pin=(.*?);').findall (O0000O0OOOO0OO000 )[0 ]#line:137
        OO000OOO000OOO0O0 =unquote_plus (OO000OOO000OOO0O0 )#line:138
    O0000000O0OO0OO0O =O0OOO000OO000OO0O .split (";")[2 ]#line:139
    OO00OO0OO000OOOOO ={"appId":O0O0O0O0000O0OOO0 ,"appid":"activities_platform","ua":O0OOO000OO000OO0O ,"pin":OO000OOO000OOO0O0 ,"functionId":O000OOO00OO0O0OO0 ,"body":OO00OO0OO000OOOOO ,"expand":{"url":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","og":"https://pro.m.jd.com"},"clientVersion":O0000000O0OO0OO0O ,"version":"4.1"}#line:140
    try :#line:141
        import base64 #line:142
        OO00O0O0O00O00O0O =["aHR0cDovLzEuOTQuOC4yNDQ6MzAwMS9hcGkvaDVzdA==","aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAxL2FwaS9oNXN0","aHR0cDovLzEuMTQuMjA4LjE3ODozMDAxL2FwaS9oNXN0"]#line:143
        OO00O0O0O00O00O0O =random .choice (OO00O0O0O00O00O0O )#line:144
        O00000OO0OOO0O0O0 =json .dumps (OO00OO0OO000OOOOO )#line:145
        OO0O0OO0OOOO0OO00 ={'Content-Type':'application/json'}#line:146
        OOO000OOOOO0O0OOO =requests .request ("POST",base64 .b64decode (OO00O0O0O00O00O0O .encode ('utf-8')).decode ('utf-8'),headers =OO0O0OO0OOOO0OO00 ,timeout =10 ,data =O00000OO0OOO0O0O0 ).json ()#line:147
        if OOO000OOOOO0O0OOO ['code']==200 :#line:148
            return OOO000OOOOO0O0OOO ['data']#line:149
        else :#line:150
            printf (O0000O0OOOO0OO000 ,f"调用远程h5st接口失败1")#line:151
            return #line:152
    except Exception as O0000O0OOOO0O0000 :#line:153
        printf (O0000O0OOOO0OO000 ,f"调用远程h5st接口失败2:{O0000O0OOOO0O0000}")#line:154
        get_h5st_body (O0OOO000OO000OO0O ,O0000O0OOOO0OO000 ,O000OOO00OO0O0OO0 ,O0O0O0O0000O0OOO0 ,OO00OO0OO000OOOOO )#line:155
        return #line:156
def H5API (OOO0O000OO00OOOOO ,O00O0OOO00000O0O0 ,OO0OO000O0OOO0000 ,O0O00O00O0O00OO0O ,O0O0O00OOOOOO00OO ,proxies =None ):#line:157
    OOO0O00O00OOOO0OO ="https://api.m.jd.com"#line:158
    O0O0O0OOO000OOOOO ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":O00O0OOO00000O0O0 ,"User-Agent":OOO0O000OO00OOOOO ,}#line:159
    OO000O00O000OOOOO =get_h5st_body (OOO0O000OO00OOOOO ,O00O0OOO00000O0O0 ,OO0OO000O0OOO0000 ,O0O0O00OOOOOO00OO ,O0O00O00O0O00OO0O )#line:160
    if not OO000O00O000OOOOO :#line:161
        return #line:162
    O0O00O00O0O00OO0O =OO000O00O000OOOOO #line:163
    try :#line:164
        OOO00OO0OO00000OO =requests .post (OOO0O00O00OOOO0OO ,headers =O0O0O0OOO000OOOOO ,data =O0O00O00O0O00OO0O ,timeout =5 ,proxies =proxies )#line:165
    except Exception as O0O000OO000000O0O :#line:166
        printf (O00O0OOO00000O0O0 ,f"H5API Error:{str(O0O000OO000000O0O)}")#line:167
        return #line:168
    if OOO00OO0OO00000OO .status_code ==200 :#line:169
        return OOO00OO0OO00000OO #line:170
    else :#line:171
        printf (O00O0OOO00000O0O0 ,OOO00OO0OO00000OO .status_code )#line:172
def Result (OO0OOO0OO0OO0000O ,O0O0OOOOO0OOO0OO0 ,O00O000O0O00O0OOO ,O00OO00OOO0O0O0O0 ):#line:173
    for OO00OO00O0O00OOOO ,O0OO00O0OOO00000O in enumerate (linkIds ,1 ):#line:174
        O0OO00OOO00OO00OO =H5API (OO0OOO0OO0OO0000O ,O0O0OOOOO0OOO0OO0 ,"inviteFissionhelp",{'linkId':O0OO00O0OOO00000O ,"isJdApp":True ,'inviter':O00O000O0O00O0OOO },'c5389',O00OO00OOO0O0O0O0 )#line:175
        if not O0OO00OOO00OO00OO :#line:176
            return #line:177
        if int (O0OO00OOO00OO00OO .status_code )!=int (200 ):#line:178
            printf (O0O0OOOOO0OOO0OO0 ,f'接口：{O0OO00OOO00OO00OO.status_code}')#line:179
            return #line:180
        if int (O0OO00OOO00OO00OO .json ()['code'])==0 :#line:181
            if O0OO00OOO00OO00OO .json ()['data']['helpResult']==1 :#line:182
                OOO00OO0OO00OOOO0 ='✅助力成功'#line:183
                power_success .append (O0O0OOOOO0OOO0OO0 )#line:184
            elif O0OO00OOO00OO00OO .json ()['data']['helpResult']==2 :#line:185
                OOO00OO0OO00OOOO0 ='❌火爆...助力失败'#line:186
                power_failure .append (O0O0OOOOO0OOO0OO0 )#line:187
            elif O0OO00OOO00OO00OO .json ()['data']['helpResult']==3 :#line:188
                OOO00OO0OO00OOOO0 ='❌已经助力别人'#line:189
                power_failure .append (O0O0OOOOO0OOO0OO0 )#line:190
            elif O0OO00OOO00OO00OO .json ()['data']['helpResult']==4 :#line:191
                OOO00OO0OO00OOOO0 ='❌助力次数用完了'#line:192
                power_failure .append (O0O0OOOOO0OOO0OO0 )#line:193
            elif O0OO00OOO00OO00OO .json ()['data']['helpResult']==6 :#line:194
                OOO00OO0OO00OOOO0 ='❌已经助力过了'#line:195
                power_failure .append (O0O0OOOOO0OOO0OO0 )#line:196
            else :#line:197
                OOO00OO0OO00OOOO0 ='❌未知状态'#line:198
                power_failure .append (O0O0OOOOO0OOO0OO0 )#line:199
            if OO00OO00O0O00OOOO ==1 :#line:200
                O0OOO000O000OO000 ="JX"#line:201
            else :#line:202
                O0OOO000O000OO000 ="JD"#line:203
            printf (O0O0OOOOO0OOO0OO0 ,f"{O0OO00OOO00OO00OO.status_code}【{O0OOO000O000OO000}】助力-→{O0OO00OOO00OO00OO.json()['data']['nickName']}|{O0OO00OOO00OO00OO.json()['data']['helpResult']} {OOO00OO0OO00OOOO0}")#line:204
        else :#line:205
            printf (O0O0OOOOO0OOO0OO0 ,f"{O0OO00OOO00OO00OO.json()['code']}  💔{O0OO00OOO00OO00OO.json()['errMsg']}")#line:206
            not_login .append (O0O0OOOOO0OOO0OO0 )#line:207
if __name__ =='__main__':#line:210
    try :#line:211
        cks =getCk #line:212
        if not cks :#line:213
            sys .exit ()#line:214
    except :#line:215
        print ("未获取到有效COOKIE,退出程序！")#line:216
        sys .exit ()#line:217
    inviter =remote_redis (f"inviteFissionhelp",3 )#line:218
    inviteDrawPin =os .environ .get ("inviteDrawPin")if os .environ .get ("inviteDrawPin")else ""#line:219
    if inviteDrawPin :#line:220
        cookie_ =[OOOO00O0O0O0O0OOO for OOOO00O0O0O0O0OOO in cks if inviteDrawPin in OOOO00O0O0O0O0OOO ]#line:221
        if cookie_ :#line:222
            print (f"当前使用【{inviteDrawPin}】作为车头！")#line:223
            cookie =cookie_ [0 ]#line:224
        else :#line:225
            print (f"未发现【{inviteDrawPin}】车头CK,退出程序！")#line:226
    else :#line:227
        print ("未设置inviteDrawPin车头,默认CK1作为车头")#line:228
        cookie =cks [0 ]#line:229
    ua =userAgent ()#line:231
    for index ,linkId in enumerate (linkIds ,1 ):#line:232
        response =H5API (ua ,cookie ,"inviteFissionBeforeHome",{'linkId':linkId ,"isJdApp":True ,'inviter':inviter },'02f8d').json ()#line:233
        if response ['success']==False and response ['code']==1000 :#line:234
            printf (cookie ,f"{response['errMsg']}")#line:235
            sys .exit ()#line:236
        if response ['data']['helpResult']==1 :#line:237
            printf (cookie ,f'✅助力作者成功 谢谢你 你是个好人！！！')#line:238
        else :#line:239
            printf (cookie ,f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:240
        response =H5API (ua ,cookie ,'inviteFissionHome',{'linkId':linkId ,"inviter":""},'eb67b').json ()#line:241
        if index ==1 :#line:242
            printf (cookie ,f'【JX】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')#line:243
            prizeNum1 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:244
        else :#line:245
            printf (cookie ,f'【JD】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')#line:246
            prizeNum2 =response ["data"]["prizeNum"]+response ["data"]["drawPrizeNum"]#line:247
        inviter =response ["data"]["inviter"]#line:248
    time .sleep (1 )#line:250
    new_cks =list_of_groups (cks ,threadsNum )#line:251
    for i ,cookies in enumerate (new_cks ,1 ):#line:252
        print (f"\n##############并发第{i}组ck##############")#line:253
        threads =[]#line:254
        proxies =get_proxies (threadsNum )#line:255
        proxies =proxies if proxies else None #line:256
        print (f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")#line:257
        for index ,cookie in enumerate (cookies ,1 ):#line:258
            thead_one =threading .Thread (target =Result ,args =(userAgent (),cookie ,inviter ,{"http":f"http://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}","https":f"https://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}"}if proxies else None ))#line:259
            threads .append (thead_one )#line:260
            power_num =len (power_success )#line:261
            if power_num >=int (number_restrictions ):#line:263
                print (f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")#line:264
                sys .exit ()#line:265
        for t in threads :#line:266
            t .start ()#line:267
            time .sleep (0.05 )#line:268
        for t in threads :#line:269
            t .join ()#line:270
    print (f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')