#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_opencardH1028.py(10.27-11.17 嗨购狂欢节 惊喜享不停)
Author: HarbourJ
Date: 2023/9/12 00:00
TG: https://t.me/HarbourToulu
cron: 0 0 */3 27-31,1-17 10,11 *
new Env('嗨购狂欢节 惊喜享不停');
ActivityEntry: https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/activity/740291?activityId=90523102701
并发变量：export jd_lzdzCommon_uuid="你的uuid"
并发命令：task HarbourJ_HarbourToulu_main/jd_opencardH1028.py conc JD_COOKIE 1-20
"""

import time, requests, sys, re, os, json, random
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
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
inviterUuid = os.environ.get("jd_lzdzCommon_uuid") if os.environ.get("jd_lzdzCommon_uuid") else ""
activityId = "90523102701"

if not activityId:
    print("⚠️未发现有效活动变量,退出程序!")
    sys.exit()

activity_url = f"https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/activity/4629706?activityId={activityId}&shareUuid={inviterUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid=undefined"
print(f"【🛳活动入口】https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/activity/4629706?activityId={activityId}")

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

def getToken(ck, r=None):
    host = f'{activityUrl.split("com/")[0]}com'
    try:
        # redis缓存Token 活动域名+pt_pin
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        # redis缓存Token 活动域名+ck前7位(获取pin失败)
        pt_pin = ck[:15]
    try:
        if r is not None:
            Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
            # print("Token过期时间", r.ttl(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}'))
            if Token is not None:
                print(f"♻️获取缓存Token")
                return Token
            else:
                # print("🈳去设置Token缓存")
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
                sign_txt = sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
                # print(sign_txt)
                f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
                if f.status_code != 200:
                    print(f.status_code)
                    return
                else:
                    if "参数异常" in f.text:
                        return
                Token_new = f.json()['token']
                # print(f"Token->: {Token_new}")
                if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                    print("✅Token缓存成功")
                else:
                    print("❌Token缓存失败")
                return Token_new
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
            sign_txt = sign({"url": f"{host}", "id": ""}, 'isvObfuscator')
            # print(sign_txt)
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                print(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    return
            Token = f.json()['token']
            print(f"✅获取实时Token")
            return Token
    except:
        return

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def refresh_cookies(res):
    if res.cookies:
        cookies = res.cookies.get_dict()
        set_cookie = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
        global activityCookie
        activityCookieMid = [i for i in activityCookie.split(';') if i != '']
        for i in activityCookieMid:
            for x in set_cookie:
                if i.split('=')[0] == x.split('=')[0]:
                    if i.split('=')[1] != x.split('=')[1]:
                        activityCookieMid.remove(i)
        activityCookie = ''.join(sorted([(set_cookie + ";") for set_cookie in list(set(activityCookieMid + set_cookie))]))

def getActivity():
    url = activityUrl
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        if response.cookies:
            cookies = response.cookies.get_dict()
            set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
            set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
        return set_cookie
    else:
        print(response.status_code, "⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def getSystemConfigForNew():
    url = "https://lzdz-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=99'
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo():
    url = "https://lzdz-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"
    payload = f"activityId={activityId}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def getMyPing(index, venderId):
    url = "https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/getMyPing"
    payload = f"userId={venderId}&token={token}&fromType=APP&activityId={activityId}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['secretPin']
    else:
        print(f"⚠️{res['errorMessage']}")
        if index == 1 and "火爆" in res['errorMessage']:
            print(f"\t⛈车头黑,退出本程序！")
            sys.exit()

def accessLogWithAD(venderId, pin):
    url = "https://lzdz-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={venderId}&code=99&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource=null"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSystime():
    url = "https://lzdz-isv.isvjcloud.com/common/getSystime"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': activityCookie,
        'Content-Length': '0',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': ua,
        'Referer': activityUrl,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers)
    refresh_cookies(response)

def getUserInfo(pin):
    url = "https://lzdz-isv.isvjcloud.com/wxActionCommon/getUserInfo"
    payload = f"pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['yunMidImageUrl'], res['data']['pin']
    else:
        print(res['errorMessage'])

def activityContent(pin, pinImg, nickname):
    url = "https://lzdz-isv.isvjcloud.com/dingzhi/union/haigo2311/activityContent"
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&nick={quote_plus(nickname)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}&adSource=null"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': f'IsvToken={token};{activityCookie}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])
        if "活动已结束" in res['errorMessage']:
            sys.exit()

def myInfo(pin, actorUuid):
    url = f"https://lzdz-isv.isvjcloud.com/dingzhi/union/haigo2311/myInfo?_={getJdTime()}"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&uid={actorUuid}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        print(res['errorMessage'])

def friendList(actorUuid, pin):
    url = "https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/friendList?_={getJdTime()}"
    payload = f"page=1&pageSize=5&getNum=true&type=0&activityId={activityId}&pin={quote_plus(pin)}&uid={actorUuid}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['friendNum']
    else:
        print(res['errorMessage'])

def doTask(actorUuid, pin, taskId):
    url = f"https://lzdz-isv.isvjcloud.com/dingzhi/union/haigo2311/doTask?_={getJdTime()}"
    payload = f"taskId={taskId}&activityId={activityId}&pin={quote_plus(pin)}&uid={actorUuid}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    print('doTask', res)
    if res['result']:
        data = res['data']
        return data
    else:
        print(res['errorMessage'])

def helpFriend(actorUuid, pin):
    url = f"https://lzdz-isv.isvjcloud.com/dingzhi/union/haigo2311/helpFriend?_={getJdTime()}"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&uid={actorUuid}&shareUuid={shareUuid}"
    headers = {
        'Host': 'lzdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    print('doTask', res)
    if res['result']:
        data = res['data']
        return data
    else:
        print(res['errorMessage'])

def bindWithVender(cookie, venderId):
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
        response = requests.request("POST", "https://api.m.jd.com/", headers=headers, data=payload, timeout=10).text
        res = json.loads(response)
        if res['success']:
            # return res['message'], res['result']['giftInfo'] if res['result'] else ""
            return res['message']
    except Exception as e:
        print(f"bindWithVender Error: {venderId} {e}")

def getShopOpenCardInfo(cookie, venderId):
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
        response = requests.get(url=url, headers=headers, timeout=5).text
        res = json.loads(response)
        if res['success']:
            venderCardName = res['result']['shopMemberCardInfo']['venderCardName']
            return venderCardName
        else:
            return venderId
    except:
        return venderId


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global shareUuid, inviteSuccNum, activityUrl, firstCk
    inviteSuccNum = 0
    if len(cks) == 1:
        shareUuid = inviterUuid
        activityUrl = activity_url
    else:
        shareUuid = remote_redis(f"lzdz_{activityId}", 2)
        activityUrl = f"https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/activity/4629706?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid=undefined"
    num = 0
    for cookie in cks:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 8 == 0:
            print("⏰等待10s,休息一下")
            time.sleep(10)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        try:
            token = getToken(cookie, r)
            if token is None:
                if num == 1:
                    print(f"⚠️车头获取Token失败,退出本程序！")
                    sys.exit()
                print(f"⚠️获取Token失败！⏰等待3s")
                time.sleep(3)
                continue
            time.sleep(0.2)
            activityCookie = getActivity()
            time.sleep(0.2)
            getSystemConfigForNew()
            time.sleep(0.3)
            getSimAct = getSimpleActInfoVo()
            if getSimAct:
                venderId = getSimAct['venderId']
            else:
                venderId = '1000001582'
            time.sleep(0.2)
            getPin = getMyPing(num, venderId)
            if getPin is not None:
                nickname = getPin[0]
                secretPin = getPin[1]
                time.sleep(0.2)
                accessLogWithAD(venderId, secretPin)
                time.sleep(0.2)
                userInfo = getUserInfo(secretPin)
                time.sleep(0.8)
                nickname = userInfo[0]
                yunMidImageUrl = userInfo[1]
                pin = userInfo[2]
                actContent = activityContent(pin, yunMidImageUrl, nickname)
                # print(f"actContent: {actContent}")
                if not actContent:
                    if num == 1:
                        print("⚠️无法获取车头邀请码,退出本程序！")
                        sys.exit()
                    continue
                hasEnd = actContent['isGameEnd']
                if hasEnd:
                    print("活动已结束，下次早点来~")
                    sys.exit()
                print(f"✅开启【{actContent['activityName']}】活动\n")
                actorUuid = actContent['uid']
                newVip = actContent['newVip']
                isVip = actContent['isVip']
                openCardStatus = actContent['openCardStatus']
                hasFollow = actContent['hasFollow']
                print(f"邀请码->: {actorUuid}")
                print(f"准备助力->: {shareUuid}")

                info = myInfo(pin, actorUuid)
                # print(f"info:{info}")
                tasks = info['task']
                openCardLists = [i['venderId'] for i in info['vip']]
                venderList = info['venderList']
                add2cart_curNum = 0
                coupon_curNum = 0
                helpfriend_curNum = 0
                joinvip_curNum = 0
                order_curNum = 0
                share2help_curNum = 0
                sigin_curNum = 0
                vipdone_curNum = 0
                followshop_curNum = 0
                for task in tasks:
                    if task['taskname'] == '加购':
                        add2cart_curNum = task['curNum']
                    elif task['taskname'] == '领券':
                        coupon_curNum = task['curNum']
                    elif task['taskname'] == '助力好友':
                        helpfriend_curNum = task['curNum']
                    elif task['taskname'] == '加入会员':
                        joinvip_curNum = task['curNum']
                    elif task['taskname'] == '下单':
                        order_curNum = task['curNum']
                    elif task['taskname'] == '邀请好友':
                        share2help_curNum = task['curNum']
                    elif task['taskname'] == '签到':
                        sigin_curNum = task['curNum']
                    elif task['taskname'] == '开卡成功':
                        vipdone_curNum = task['curNum']
                    elif task['taskname'] == '关注店铺':
                        followshop_curNum = task['curNum']
                unOpenCardLists = []
                for venderid in venderList:
                    if venderid["venderId"] not in openCardLists:
                        unOpenCardLists.append((int(venderid['venderId']), venderid['venderName']))
                if num == 1:
                    print(f"🛳已邀请{share2help_curNum}人")
                if isVip == 1 and hasFollow:
                    print("已全部入会并关注店铺")
                    if "helpFriendMsg" in str(actContent):
                        helpFriendMsg = actContent['helpFriendMsg']
                        helpFriendStatus = actContent['helpFriendStatus']
                        print(f"助力状态：{helpFriendStatus} --> {helpFriendMsg}")
                        if helpFriendStatus == 1:
                            print("🎉🎉🎉助力成功~")
                            inviteSuccNum += 1
                            print(f"本次车头已邀请{inviteSuccNum}人")
                    else:
                        help_result = helpFriend(actorUuid, pin)
                        if help_result:
                            helpFriendMsg = help_result['helpFriendMsg']
                            helpFriendStatus = help_result['helpFriendStatus']
                            print(f"助力状态：{helpFriendStatus} --> {helpFriendMsg}")
                            if helpFriendStatus == 1:
                                print("🎉🎉🎉助力成功~")
                                inviteSuccNum += 1
                                print(f"本次车头已邀请{inviteSuccNum}人")
                else:
                    if not hasFollow:
                        print(f"现在去关注店铺")
                        follow_result = doTask(actorUuid, pin, "followshop")
                        print("关注店铺成功")
                    if len(unOpenCardLists) > 0:
                        print(f"现在去开卡,开{len(unOpenCardLists)}张卡")
                        openExit = False
                        for shop in unOpenCardLists:
                            print(f"去开卡 {shop[1]} {shop[0]}")
                            venderId = shop[0]
                            venderCardName = shop[1]
                            # getShopOpenCardInfo(cookie, venderId)
                            retry_time = 0
                            while True:
                                retry_time += 1
                                open_result = bindWithVender(cookie, venderId)
                                if open_result is not None:
                                    if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                                        print(f"\t⛈⛈{venderCardName} {open_result}")
                                        openExit = True
                                    else:
                                        print(f"\t🎉🎉{venderCardName} {open_result}")
                                    break
                                else:
                                    time.sleep(3)
                                if retry_time >= 3:
                                    break
                            if openExit:
                                break
                            time.sleep(3.5)
                        actContent0 = activityContent(pin, yunMidImageUrl, nickname)
                        isVip0 = actContent0['isVip']
                        hasFollow0 = actContent0['hasFollow']
                        if isVip0 == 1 and hasFollow0:
                            if "helpFriendMsg" in str(actContent0):
                                helpFriendMsg = actContent0['helpFriendMsg']
                                helpFriendStatus = actContent0['helpFriendStatus']
                                print(f"助力状态：{helpFriendStatus} --> {helpFriendMsg}")
                                if helpFriendStatus == 1:
                                    print("🎉🎉🎉助力成功~")
                                    inviteSuccNum += 1
                                    print(f"本次车头已邀请{inviteSuccNum}人")
                            else:
                                help_result = helpFriend(actorUuid, pin)
                                if help_result:
                                    helpFriendMsg = help_result['helpFriendMsg']
                                    helpFriendStatus = help_result['helpFriendStatus']
                                    print(f"助力状态：{helpFriendStatus} --> {helpFriendMsg}")
                                    if helpFriendStatus == 1:
                                        print("🎉🎉🎉助力成功~")
                                        inviteSuccNum += 1
                                        print(f"本次车头已邀请{inviteSuccNum}人")
                    # if sigin_curNum == 0:
                    #     print("现在去签到")
                    #     doTask(actorUuid, pin, 'sigin')
                    # if add2cart_curNum == 0:
                    #     print("现在去一键加购")
                    #     doTask(actorUuid, pin, 'add2cart')

        except Exception as e:
            print(f"Main Error: {e}")
            if num == 1:
                exit()

        if num == 1:
            print(f"后面账号全部助力 {actorUuid}")
            shareUuid = actorUuid
            activityUrl = f"https://lzdz-isv.isvjcloud.com/dingzhi/bd/common/activity/4629706?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&lng=00.000000&lat=00.000000&sid=&un_area=&&shopid=undefined"

        time.sleep(3)