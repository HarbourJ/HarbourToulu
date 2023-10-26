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

import time, requests, sys, re, threading, os, random
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
number_restrictions = 5000

linkIds = ['Wvzc_VpNTlSkiQdHT8r7QA', '3orGfh1YkwNLksxOcN8zWQ']
power_success = []
power_failure = []
not_login= []
start = time.time()

def printf(cookie, T):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    print(f"{str(datetime.now())[0:22]}->{pt_pin}->{T}")

def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list

def get_proxies(count):
    # 获取当前运行环境网IP
    try:
        localIp = requests.get("https://pycn.yapi.py.cn/get_client_ip").json()["ret_data"]
    except:
        localIp = requests.get("https://ifconfig.me/").text
    print(f"获取当前IP:{localIp}")
    # 默认为本地ip，若使用代理请设置参数proxyType="xxx"
    if proxyType == "":
        print('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')
        return None
    elif proxyType == "1":
        print("当前使用品易代理")
        # 自动填写品易IP白名单
        requests.get(f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={localIp}")
        # 根据并发数提取IP数量
        # resp = requests.get(f"http://tiqu.pyhttp.taolop.com/getflowip?count={count}&neek={neek}&type=1&sep=1&sb=&ip_si=1&mr=0")
        if timeMode:
            # 时长套餐
            if not pack:
                print(f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")
                sys.exit()
            resp = requests.get(f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={count}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")
        else:
            # 流量套餐
            resp = requests.get(f"http://zltiqu.pyhttp.taolop.com/getip?count={count}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")
    elif proxyType == "2":
        print("当前使用星空代理,1个ip一个店铺模式")
        resp = requests.get(f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={count}&format=txt&split=2&sign={signxk}")
    elif proxyType == "3":
        print("当前使用小象代理")
        resp = requests.get(f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")
    elif proxyType == "4":
        print("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")
        resp = requests.get(f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={count}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")
    elif proxyType == "5":
        time.sleep(1)
        print("当前使用51代理,1个ip一个店铺模式")
        resp = requests.get(daili51)
    elif proxyType == "6":
        print("当前使用代理池工具")
        return [proxyPoolIp] * count
    else:
        print("当前选择代理无效,默认使用本地ip")
        return None

    ip = resp.text
    # print(ip)
    if re.match(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', ip) is None:
        print(ip)
        # exit("IP 不正确")
        return None
    ip = ip.split('\r\n')
    ip = [x for x in ip if x]

    return ip

def convert_ms_to_hours_minutes(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}h{minutes}m'

def get_h5st_body (OOO00OOO0O0O00O0O ,O00OOOO0OOOOOOOO0 ,OO00000OOO0O0O0O0 ,OOOO00OO0O000OO00 ,O0OO0000O00O0000O ):#line:1
    try :#line:2
        OO0O0O0O0O0O00000 =re .compile (r'pt_pin=(.*?);').findall (O00OOOO0OOOOOOOO0 )[0 ]#line:3
        OO0O0O0O0O0O00000 =unquote_plus (OO0O0O0O0O0O00000 )#line:4
    except IndexError :#line:5
        OO0O0O0O0O0O00000 =re .compile (r'pin=(.*?);').findall (O00OOOO0OOOOOOOO0 )[0 ]#line:6
        OO0O0O0O0O0O00000 =unquote_plus (OO0O0O0O0O0O00000 )#line:7
    O00OOO0OOOO0OOOOO =OOO00OOO0O0O00O0O .split (";")[2 ]#line:8
    O0OO0000O00O0000O ={"appId":OOOO00OO0O000OO00 ,"appid":"activities_platform","ua":OOO00OOO0O0O00O0O ,"pin":OO0O0O0O0O0O00000 ,"functionId":OO00000OOO0O0O0O0 ,"body":O0OO0000O00O0000O ,"expand":{"url":"https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html","og":"https://pro.m.jd.com"},"clientVersion":O00OOO0OOOO0OOOOO ,"version":"4.1"}#line:22
    try :#line:23
        import base64 #line:24
        OOOO0OOOO00O0O0O0 = ["aHR0cDovLzEuOTQuOC4yNDQ6MzAwMS9hcGkvaDVzdA==","aHR0cDovL2hhcmJvdXJqLmNmOjMwMDEvYXBpL2g1c3Q=","aHR0cDovLzEzMi4yMjYuMjM4LjE4NjozMDAxL2FwaS9oNXN0"] #line:25
        OOOO0OOOO00O0O0O0 = random.choice(OOOO0OOOO00O0O0O0)
        OO0OO000OOO00OOO0 =json .dumps (O0OO0000O00O0000O )#line:26
        OO0000OOO0OOOO00O ={'Content-Type':'application/json'}#line:29
        OO00OO0O00OO0OOOO =requests .request ("POST",base64 .b64decode (OOOO0OOOO00O0O0O0 .encode ('utf-8')).decode ('utf-8'),headers =OO0000OOO0OOOO00O ,timeout =10 ,data =OO0OO000OOO00OOO0 ).json ()#line:30
        if OO00OO0O00OO0OOOO ['code']==200 :#line:31
            return OO00OO0O00OO0OOOO ['data']#line:33
        else :#line:34
            printf (O00OOOO0OOOOOOOO0 ,f"调用远程h5st接口失败1")#line:35
            return #line:36
    except Exception as O000O0O0O0OOO0OO0 :#line:37
        printf (O00OOOO0OOOOOOOO0 ,f"调用远程h5st接口失败2:{O000O0O0O0OOO0OO0}")#line:38
        get_h5st_body (OOO00OOO0O0O00O0O ,O00OOOO0OOOOOOOO0 ,OO00000OOO0O0O0O0 ,OOOO00OO0O000OO00 ,O0OO0000O00O0000O )#line:39
        return #line:40
def H5API (OOOOO0000OO0OOO0O ,OOO0OO00O0000000O ,OOO0O0000OO000000 ,O00O0O0OO00O00OOO ,OO0O0O00O000OO000 ,proxies =None ):#line:42
    O0OOOOO0OO0O0O000 ="https://api.m.jd.com"#line:43
    O00O0O0O0OOO0OO00 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":OOO0OO00O0000000O ,"User-Agent":OOOOO0000OO0OOO0O ,}#line:55
    O0O0000OOOO0O0OOO =get_h5st_body (OOOOO0000OO0OOO0O ,OOO0OO00O0000000O ,OOO0O0000OO000000 ,OO0O0O00O000OO000 ,O00O0O0OO00O00OOO )#line:56
    if not O0O0000OOOO0O0OOO :#line:57
        return #line:58
    O00O0O0OO00O00OOO =O0O0000OOOO0O0OOO #line:59
    try :#line:60
        OO000O00OOOO0OO0O =requests .post (O0OOOOO0OO0O0O000 ,headers =O00O0O0O0OOO0OO00 ,data =O00O0O0OO00O00OOO ,timeout =5 ,proxies =proxies )#line:61
    except Exception as O0O0OO0OO0OOO0OOO :#line:62
        printf (OOO0OO00O0000000O ,f"H5API Error:{str(O0O0OO0OO0OOO0OOO)}")#line:63
        return #line:64
    if OO000O00OOOO0OO0O .status_code ==200 :#line:65
        return OO000O00OOOO0OO0O #line:66
    else :#line:67
        printf (OOO0OO00O0000000O ,OO000O00OOOO0OO0O .status_code )#line:68
def Result (O0000000OO00000OO ,OOOO0O0OO00O0O000 ,OOO0O0O0OO0OO0OO0 ,O000000000O0OOOOO ):#line:70
    for OOOO000OO0OOOO0OO ,O0000OO0O0OOO0000 in enumerate (linkIds ,1 ):#line:71
        O0000OO000OOOOOO0 =H5API (O0000000OO00000OO ,OOOO0O0OO00O0O000 ,"inviteFissionhelp",{'linkId':O0000OO0O0OOO0000 ,"isJdApp":True ,'inviter':OOO0O0O0OO0OO0OO0 },'02f8d',O000000000O0OOOOO )#line:72
        if not O0000OO000OOOOOO0 :#line:73
            return #line:74
        if int (O0000OO000OOOOOO0 .status_code )!=int (200 ):#line:75
            printf (OOOO0O0OO00O0O000 ,f'接口：{O0000OO000OOOOOO0.status_code}')#line:76
            return #line:77
        if int (O0000OO000OOOOOO0 .json ()['code'])==0 :#line:78
            if O0000OO000OOOOOO0 .json ()['data']['helpResult']==1 :#line:79
                O000OO00O000O0OO0 ='✅助力成功'#line:80
                power_success .append (OOOO0O0OO00O0O000 )#line:81
            elif O0000OO000OOOOOO0 .json ()['data']['helpResult']==2 :#line:82
                O000OO00O000O0OO0 ='❌火爆...助力失败'#line:83
                power_failure .append (OOOO0O0OO00O0O000 )#line:84
            elif O0000OO000OOOOOO0 .json ()['data']['helpResult']==3 :#line:85
                O000OO00O000O0OO0 ='❌已经助力别人'#line:86
                power_failure .append (OOOO0O0OO00O0O000 )#line:87
            elif O0000OO000OOOOOO0 .json ()['data']['helpResult']==4 :#line:88
                O000OO00O000O0OO0 ='❌助力次数用完了'#line:89
                power_failure .append (OOOO0O0OO00O0O000 )#line:90
            elif O0000OO000OOOOOO0 .json ()['data']['helpResult']==6 :#line:91
                O000OO00O000O0OO0 ='❌已经助力过了'#line:92
                power_failure .append (OOOO0O0OO00O0O000 )#line:93
            else :#line:94
                O000OO00O000O0OO0 ='❌未知状态'#line:95
                power_failure .append (OOOO0O0OO00O0O000 )#line:96
            if OOOO000OO0OOOO0OO ==1 :#line:97
                O00000OO0O00O00O0 ="JX"#line:98
            else :#line:99
                O00000OO0O00O00O0 ="JD"#line:100
            printf (OOOO0O0OO00O0O000 ,f"{O0000OO000OOOOOO0.status_code}【{O00000OO0O00O00O0}】助力-→{O0000OO000OOOOOO0.json()['data']['nickName']}|{O0000OO000OOOOOO0.json()['data']['helpResult']} {O000OO00O000O0OO0}")#line:101
        else :#line:102
            printf (OOOO0O0OO00O0O000 ,f"{O0000OO000OOOOOO0.json()['code']}  💔{O0000OO000OOOOOO0.json()['errMsg']}")#line:103
            not_login .append (OOOO0O0OO00O0O000 )


if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    inviter = remote_redis(f"inviteFissionhelp", 3)
    inviteDrawPin = os.environ.get("inviteDrawPin") if os.environ.get("inviteDrawPin") else ""
    if inviteDrawPin:
        cookie_ = [ck for ck in cks if inviteDrawPin in ck]
        if cookie_:
            print(f"当前使用【{inviteDrawPin}】作为车头！")
            cookie = cookie_[0]
        else:
            print(f"未发现【{inviteDrawPin}】车头CK,退出程序！")
    else:
        print("未设置inviteDrawPin车头,默认CK1作为车头")
        cookie = cks[0]
    # 获取车头助力码
    ua = userAgent()
    for index, linkId in enumerate(linkIds, 1):
        response = H5API(ua, cookie, "inviteFissionhelp", {'linkId': linkId, "isJdApp": True, 'inviter': inviter}, '02f8d').json()
        if response['success'] == False and response['code'] == 1000:
            printf(cookie, f"{response['errMsg']}")
            sys.exit()
        if response['data']['helpResult'] == 1:
            printf(cookie, f'✅助力作者成功 谢谢你 你是个好人！！！')
        else:
            printf(cookie, f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')
        response = H5API(ua, cookie, 'inviteFissionHome', {'linkId': linkId, "inviter": ""}, 'af89e').json()
        if index == 1:
            printf(cookie, f'【JX】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')
            prizeNum1 = response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]
        else:
            printf(cookie, f'【JD】⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')
            prizeNum2 = response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]
        inviter = response["data"]["inviter"]

    time.sleep(1)
    new_cks = list_of_groups(cks, threadsNum)
    for i, cookies in enumerate(new_cks, 1):
        print(f"\n##############并发第{i}组ck##############")
        threads = []
        proxies = get_proxies(threadsNum)
        proxies = proxies if proxies else None
        print(f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")
        for index, cookie in enumerate(cookies, 1):
            thead_one = threading.Thread(target=Result, args=(userAgent(), cookie, inviter, {"http": f"http://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}", "https": f"https://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}"} if proxies else None))
            threads.append(thead_one)  # 线程池添加线程
            power_num = len(power_success)
            # print(f"🎉当前已获取助力{power_num}\n")
            if power_num >= int(number_restrictions):
                print(f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")
                sys.exit()
        for t in threads:
            t.start()
            time.sleep(0.05)
        for t in threads:
            t.join()
    print(f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')