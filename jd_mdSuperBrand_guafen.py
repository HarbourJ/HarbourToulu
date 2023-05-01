#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_mdSuperBrand_guafen.py(美的超级品牌日 4.29-5.10)
Author: HarbourJ
Date: 2023/4/29 00:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('美的超级品牌日-瓜分40')
ActivityEntry: https://lzdz1-isv.isvjcloud.com/m/1000282702/9013856/dza7e4d0cb861648dc913088ba7e83/?shareUuid=f53763a2f0004c9ab4e8066cff9557a7&adsource=null
"""

import time, requests, sys, re, os, json, random, threading
from datetime import datetime
from urllib.parse import quote_plus, unquote_plus
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
try:
    from jd_sign import *
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")
    sys.exit()
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)


# 这里填写品易代理参数(目前仅支持品易代理)
neek = ""
appkey = ""


redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
neek = os.environ.get("neek") if os.environ.get("neek") else neek
appkey = os.environ.get("appkey") if os.environ.get("appkey") else appkey

venderId = "1000282702"
activityId = "dza7e4d0cb861648dc913088ba7e83"
activity_url = f"https://lzdz1-isv.isvjcloud.com/m/1000282702/9013856/{activityId}/"
print(f"【🛳活动入口】{activity_url}\n")

def redis_conn():
    try:
        import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
            r = redis.Redis(connection_pool=pool)
            r.get('conn_test')
            print('✅redis连接成功')
            return r
        except:
            print("⚠️redis连接异常")
    except:
        print("⚠️缺少redis依赖，请运行pip3 install redis")
        sys.exit()

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
        localIp = requests.get("https://pycn.yapi.3866866.com/get_client_ip").json()["ret_data"]
    except:
        localIp = requests.get("https://ifconfig.me/").text
    print(f"\n获取当前IP:{localIp}")
    print("当前使用品易代理")
    # 自动填写品易IP白名单
    requests.get(f"https://pycn.yapi.3866866.com/index/index/save_white?neek={neek}&appkey={appkey}&white={localIp}")
    # 流量套餐
    resp = requests.get(f"http://zltiqu.pyhttp.taolop.com/getip?count={count}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")

    ip = resp.text
    print(ip)
    if re.match(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', ip) is None:
        print(ip)
        # exit("IP 不正确")
        return None
    ip = ip.split('\r\n')
    ip = [x for x in ip if x]

    return ip

def getToken(ck, proxies, activityUrl, r=None):
    host = f'{activityUrl.split("com/")[0]}com'
    try:
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        pt_pin = ck[:15]
    try:
        try:
            Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
        except Exception as e:
            # printf(ck, f"redis get error: {str(e)}")
            Token = None
        if Token is not None:
            printf(ck, f"♻️获取缓存Token")
            return Token
        else:
            s.headers = {
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': '',
                'Cookie': ck,
                'Host': 'api.m.jd.com',
                'Referer': '',
                'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
                'Accept': '*/*'
            }
            sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
            s.proxies = proxies
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                printf(ck, f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    printf(ck, f.text)
                    return
            Token_new = f.json()['token']
            try:
                if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                    printf(ck, "✅Token缓存成功")
                else:
                    printf(ck, "❌Token缓存失败")
            except Exception as e:
                # printf(ck, f"redis set error: {str(e)}")
                printf(ck, f"✅获取实时Token")
            return Token_new
    except Exception as e:
        printf(ck, f"Token error: {str(e)}")
        return

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def refresh_cookies(res, setCookie):
    if res.cookies:
        cookies = res.cookies.get_dict()
        set_cookie = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
        activityCookieMid = [i for i in setCookie.split(';') if i != '']
        for i in activityCookieMid:
            for x in set_cookie:
                if i.split('=')[0] == x.split('=')[0]:
                    if i.split('=')[1] != x.split('=')[1]:
                        activityCookieMid.remove(i)
        setCookie = ''.join(sorted([(set_cookie + ";") for set_cookie in list(set(activityCookieMid + set_cookie))]))
        return setCookie

def getActivity(ua, cookie, activityUrl, proxies):
    url = f"https://lzdz1-isv.isvjcloud.com/wxCommonInfo/token?t={getJdTime()}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("GET", url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        if response.cookies:
            cookies = response.cookies.get_dict()
            set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
            set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
        return set_cookie
    else:
        printf(cookie, f"{response.status_code} ⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def getMyCidPing(ua, cookie, activityUrl, setCookie, venderId, token, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/customer/getMyCidPing"
    payload = f"userId={venderId}&activityId={activityId}&token={token}&fromType=APP&pin="
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie, res['data']['nickname'], res['data']['secretPin'], res['data']['cid']
    else:
        printf(cookie, f"getMyCidPing Error: {res['errorMessage']}")

def getSystemConfigForNew(ua, activityUrl, setCookie, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=99&pin='
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    return setCookie

def init(ua, cookie, activityUrl, setCookie, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/init"
    payload = f"activityId={activityId}&dzActivityType=0&pin="
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    return setCookie

def accessLogWithAD(ua, activityUrl, setCookie, venderId, secretPin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={venderId}&code=99&pin={quote_plus(secretPin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=JDApp&adSource=null"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    return setCookie

def getUserInfo(ua, cookie, activityUrl, setCookie, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo"
    payload = f"pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie, res['data']['nickname'], res['data']['yunMidImageUrl'], res['data']['pin']
    else:
        printf(cookie, f"getUserInfo Error: {res['errorMessage']}")

def activityContent(ua, cookie, activityUrl, setCookie, pin, pinImg, nickname, shareUuid, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/mdTsak/active/activityContent"
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&nick={quote_plus(nickname)}&shareUuid={shareUuid}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie, res['data']
    else:
        printf(cookie, f"activityContent Error: {res['errorMessage']}")

def saveTask(ua, cookie, activityUrl, setCookie, actorUuid, shareUuid, pin, taskType, taskValue, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/mdTsak/active/saveTask"
    payload = f"activityId={activityId}&actorUuid={actorUuid}&shareUuid={shareUuid}&pin={quote_plus(pin)}&taskType={taskType}&taskValue={taskValue}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie, res['data']
    else:
        printf(cookie, f"saveTask Error: {res['errorMessage']}")

def writePersonInfo(ua, cookie, activityUrl, setCookie, jdActivityId, actionType, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/interaction/write/writePersonInfo"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&venderId={venderId}&jdActivityId={jdActivityId}&actionType={actionType}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie
    else:
        printf(cookie, f"writePersonInfo Error: {res['errorMessage']}")

def insertCrmPageVisit(ua, cookie, activityUrl, setCookie, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/crm/pageVisit/insertCrmPageVisit"
    payload = f"elementId=%E9%82%80%E8%AF%B7%E5%A5%BD%E5%8F%8B&pageId={activityId}&venderId={venderId}&pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    if res['result']:
        return setCookie
    else:
        printf(cookie, f"insertCrmPageVisit Error: {res['errorMessage']}")

def drawContent(ua, cookie, activityUrl, setCookie, actorUuid, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent"
    payload = f"activityId={actorUuid}&pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    return setCookie

def draw(ua, cookie, activityUrl, setCookie, actorUuid, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/mdTsak/active/draw"
    payload = f"activityId={activityId}&actorUuid={actorUuid}&pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        # 'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    # printf(cookie, headers)
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    printf(cookie, f"draw:{res}")
    if res['result']:
        return res['data']
    else:
        printf(cookie, f"draw Error: {res['errorMessage']}")

def drawBean(ua, cookie, activityUrl, setCookie, actorUuid, pin, proxies):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/mdTsak/active/drawBean"
    payload = f"activityId={activityId}&actorUuid={actorUuid}&pin={quote_plus(pin)}&type=2"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': ua,
        # 'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': setCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    setCookie = refresh_cookies(response, setCookie)
    res = response.json()
    # printf(cookie, f"drawBean:{res}")
    if res['result']:
        return setCookie, res['data']
    else:
        printf(cookie, f"drawBean Error: {res['errorMessage']}")

def bindWithVender(ua, cookie, venderId, proxies):
    try:
        payload = {
                'appid': 'jd_shop_member',
                'functionId': 'bindWithVender',
                'body': json.dumps({
                    'venderId': venderId,
                    'shopId': venderId,
                    'bindByVerifyCodeFlag': 1
                }, separators=(',', ':'))
            }
        headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': ua,
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': 'https://shopmember.m.jd.com/',
            'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
            'Accept': '*/*'
        }
        response = requests.request("POST", "https://api.m.jd.com/", headers=headers, data=payload, timeout=10, proxies=proxies).text
        res = json.loads(response)
        if res['success']:
            return res['message'], res['result']['giftInfo'] if res['result'] else ""
    except Exception as e:
        printf(cookie, f"bindWithVender Error: {venderId} {e}")

def getShopOpenCardInfo(ua, cookie, venderId, proxies):
    try:
        body = {"venderId": str(venderId), "channel": "401"}
        url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888'
        headers = {
            'Host': 'api.m.jd.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'User-Agent': ua,
            'Accept-Language': 'zh-cn',
            'Referer': 'https://shopmember.m.jd.com/',
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.get(url=url, headers=headers, timeout=5, proxies=proxies).text
        res = json.loads(response)
        if res['success']:
            venderCardName = res['result']['shopMemberCardInfo']['venderCardName']
            return venderCardName
        else:
            return venderId
    except:
        return venderId

def main_task(ua, cookie, proxies):
    shareUuid = random.choice(needHelpList) if needHelpList else "f53763a2f0004c9ab4e8066cff9557a7"
    activityUrl = f"https://lzdz1-isv.isvjcloud.com/m/1000282702/9013856/{activityId}/?shareUuid={shareUuid}&adsource=null&sid=d441642f659840ff8893c880beee407w&un_area=12_1212_22222_22222"
    token = getToken(cookie, proxies, activityUrl, r)
    if token is None:
        printf(cookie, f"⚠️获取Token失败！")
        return
    time.sleep(0.1)
    activityCookie = getActivity(ua, cookie, activityUrl, proxies)
    if not activityCookie:
        return
    getPin = getMyCidPing(ua, cookie, activityUrl, activityCookie, venderId, token, proxies)
    if not getPin:
        return
    activityCookie = getPin[0]
    nickname = getPin[1]
    secretPin = getPin[2]
    time.sleep(0.1)
    activityCookie = getSystemConfigForNew(ua, activityUrl, activityCookie, proxies)
    time.sleep(0.1)
    activityCookie = init(ua, cookie, activityUrl, activityCookie, proxies)
    time.sleep(0.1)
    activityCookie = accessLogWithAD(ua, activityUrl, activityCookie, venderId, secretPin, proxies)
    time.sleep(0.1)
    userInfo = getUserInfo(ua, cookie, activityUrl, activityCookie, secretPin, proxies)
    time.sleep(0.1)
    if not userInfo:
        return
    activityCookie = userInfo[0]
    nickname = userInfo[1]
    yunMidImageUrl = userInfo[2]
    pin = userInfo[3]
    time.sleep(0.1)
    actContent_ = activityContent(ua, cookie, activityUrl, activityCookie, pin, yunMidImageUrl, nickname, shareUuid, proxies)
    if not actContent_:
        return
    activityCookie = actContent_[0]
    actContent = actContent_[1]
    hasEnd = actContent['hasEnd']
    if hasEnd:
        printf(cookie, "活动已结束，下次早点来~")
        return
    actorUuid = actContent['actorUuid']

    openCard = actContent['openCard']
    assistStatus = actContent['assistStatus']
    addInfo = actContent['addInfo']
    if openCard:
        printf(cookie, f"已开卡无法助力,助力状态-->{assistStatus}")
    else:
        printf(cookie, "现在去开卡")
        printf(cookie, f"去开卡 {venderId}")
        venderCardName = getShopOpenCardInfo(ua, cookie, venderId, proxies)
        open_result = bindWithVender(ua, cookie, venderId, proxies)
        if open_result is not None:
            if "火爆" in open_result[0] or "失败" in open_result[0] or "解绑" in open_result[0]:
                printf(cookie, f"⛈{open_result[0]}")
                return
            if "加入店铺会员成功" in open_result[0]:
                printf(cookie, f"🎉🎉{venderCardName} {open_result[0]}")
                if open_result[1]:
                    printf(cookie, f"🎁获得{','.join([gift['discountString'] + gift['prizeName'] for gift in open_result[1]['giftList']])}")
        time.sleep(0.3)
        actContent_ = activityContent(ua, cookie, activityUrl, activityCookie, pin, yunMidImageUrl, nickname, shareUuid, proxies)
        if not actContent_:
            return
        activityCookie = actContent_[0]
        actContent = actContent_[1]
        assistStatus = actContent['assistStatus']
        if assistStatus == 0:
            printf(cookie, "无法助力自己")
        elif assistStatus == 2:
            printf(cookie, "已经助力过好友")
        elif assistStatus == 1:
            printf(cookie, f"🎉🎉🎉助力{shareUuid}成功")
        time.sleep(0.1)

    printf(cookie, f"邀请码->: {actorUuid}")
    printf(cookie, f"准备助力->: {shareUuid}")
    time.sleep(0.1)

    activityCookie = drawContent(ua, cookie, activityUrl, activityCookie, actorUuid, pin, proxies)
    time.sleep(0.1)

    # 瓜分
    drawBeanInfo = drawBean(ua, cookie, activityUrl, activityCookie, actorUuid, pin, proxies)
    if drawBeanInfo:
        activityCookie = drawBeanInfo[0]
        drawBean_ = drawBeanInfo[1]
        beanNum = drawBean_['beanNum']
        sendStatus = drawBean_['sendStatus']
        if sendStatus:
            printf(cookie, f"🎁瓜分获得{beanNum}京豆")


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()

    global inviteSuccNum, needHelpList
    inviteSuccNum = 0
    needHelpList = []

    for index, cookie in enumerate(cks, 1):
        proxies = get_proxies(1)
        proxies = proxies if proxies else None
        print(f"****************提取{len(proxies) if proxies else 0}个IP****************")
        index = 1
        main_task(userAgent(), cookie, {"http": f"http://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}", "https": f"https://{proxies[index-1].split(':')[0]}:{proxies[index-1].split(':')[1]}"} if proxies else None)
        time.sleep(1)