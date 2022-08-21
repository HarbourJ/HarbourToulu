#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/20 20:16
# @Author  : HarbourJ
# @File    : jd_XAY.py

"""
File: jd_XAY.py(飞利浦新安怡组队瓜分)
Author: HarbourJ
Date: 2022/8/1 22:37
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('8.20-8.21 飞利浦新安怡组队瓜分');
活动入口: https://lzkjdz-isv.isvjcloud.com/pool/captain/7409220?activityId=0bcdfb58215f4907a63af8a773eba62e&signUuid=8ffb7a0a6aa54bc5a681cf22d86bf2bf
"""

import time
import requests
import sys
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime
import json
import random
from urllib.parse import quote_plus, unquote_plus
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    if "aarch" in os.uname().machine:
        from utils.jd_sign_arm64 import *
    else:
        from utils.jd_sign_x86 import *
except:
    from utils.jd_sign import *
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    logger.info("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)
try:
    if os.environ.get("redis_url"):
        redis_url = os.environ["redis_url"]  # redis ip
    else:
        redis_url = "172.17.0.1"
    if os.environ.get("redis_pwd"):
        redis_pwd = os.environ["redis_pwd"]  # redis 密码
    else:
        redis_pwd = ""
except:
    redis_url = "172.17.0.1"
    redis_pwd = ""

inviterUuids = [
    "8ffb7a0a6aa54bc5a681cf22d86bf2bf",
    "6808a7789086456d875e37c7138c5b3e"
]

inviterUuid = random.choice(inviterUuids)
activityId = "0bcdfb58215f4907a63af8a773eba62e"
shopId = "1000002527"
activity_url = f"https://lzkjdz-isv.isvjcloud.com/pool/captain/7409220?activityId={activityId}&signUuid={inviterUuid}"

def redis_conn():
    try:
        import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=6379, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
            r = redis.Redis(connection_pool=pool)
            r.get('conn_test')
            logger.info('✅redis连接成功')
            return r
        except:
            logger.info("⚠️redis连接异常")
    except:
        logger.info("⚠️缺少redis依赖，请运行pip3 install redis")

def getToken(ck, r=None):
    try:
        # redis缓存Token 活动域名+pt_pin
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        # redis缓存Token 活动域名+ck前7位(获取pin失败)
        pt_pin = ck[:8]
    try:
        if r is not None:
            Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
            # logger.info("Token过期时间", r.ttl(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}'))
            if Token is not None:
                logger.info(f"♻️获取缓存Token->: {Token}")
                return Token
            else:
                logger.info("🈳去设置Token缓存-->")
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
                sign_txt = sign({"url": f"{activityUrl}", "id": ""}, 'isvObfuscator')
                # logger.info(sign_txt)
                f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
                if f.status_code != 200:
                    logger.info(f.status_code)
                    return
                else:
                    if "参数异常" in f.text:
                        return
                Token_new = f.json()['token']
                logger.info(f"Token->: {Token_new}")
                if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                    logger.info("✅Token缓存设置成功")
                else:
                    logger.info("❌Token缓存设置失败")
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
            sign_txt = sign({"url": f"{activityUrl}", "id": ""}, 'isvObfuscator')
            # logger.info(sign_txt)
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                logger.info(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    return
            Token = f.json()['token']
            logger.info(f"Token->: {Token}")
            return Token
    except:
        return

def getJdTime():
    url = "http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'api.m.jd.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    try:
        response = requests.request("GET", url, headers=headers, timeout=2)
        if response.status_code == 200:
            res = response.json()
            jdTime = res['currentTime2']
    except:
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

def getActivity(token):
    url = activityUrl
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': f'IsvToken={token}',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    # logger.info(response.text)
    if response.status_code == 493:
        logger.info(response.status_code, "⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()
    if response.cookies:
        cookies = response.cookies.get_dict()
        set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
        set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
    return set_cookie

def getSystemConfigForNew(activityId):
    url = "https://lzkjdz-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=46'
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo(activityId):
    url = "https://lzkjdz-isv.isvjcloud.com/customer/getSimpleActInfoVo"
    payload = f"activityId={activityId}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
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
        logger.info(res['errorMessage'])

def getMyPing(shopId, token, index):
    url = "https://lzkjdz-isv.isvjcloud.com/customer/getMyPing"
    payload = f"userId={shopId}&token={token}&fromType=APP"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
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
        logger.info(f"⚠️{res['errorMessage']}")
        if index == 1:
            logger.info(f"\t⛈车头黑,退出本程序！")
            sys.exit()

def accessLogWithAD(shopId, pin):
    url = "https://lzkjdz-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={shopId}&code=46&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&shopid={shopId}&subType=app&adSource="
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSystime():
    url = "https://lzkjdz-isv.isvjcloud.com/common/getSystime"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
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

def activityContent(pin, signUuid):
    url = "https://lzkjdz-isv.isvjcloud.com/pool/activityContent"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&signUuid={signUuid}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # logger.info(response.text)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        logger.info(res['errorMessage'])

def getUserInfo(pin):
    url = "https://lzkjdz-isv.isvjcloud.com/wxActionCommon/getUserInfo"
    payload = f"pin={quote_plus(pin)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
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
        logger.info(res['errorMessage'])

def saveCandidate(signUuid, pin, pinImg, nickname):
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    url = "https://lzkjdz-isv.isvjcloud.com/pool/saveCandidate"
    payload = f"activityId={activityId}&signUuid={signUuid}&pin={quote_plus(pin)}&pinImg={yunMidImageUrl}&jdNick={quote_plus(nickname)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def saveCaptain(pin, pinImg, nickname):
    url = "https://lzkjdz-isv.isvjcloud.com/pool/saveCaptain"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={quote_plus(pinImg)}&jdNick={quote_plus(nickname)}"
    headers = {
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': activityCookie
    }
    logger.info('saveCaptain', saveCaptain)
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['signUuid']
    else:
        logger.info(res['errorMessage'])

def shopmember(cookie):
    url = f'https://shopmember.m.jd.com/shopcard/?venderId={user_id}&channel=401&returnUrl={quote_plus(activityUrl + "&isOpenCard=1")}'
    headers = {
        'Host': 'shopmember.m.jd.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jinggeng-isv.isvjcloud.com/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    requests.request("GET", url, headers=headers)

def getShopOpenCardInfo(cookie):
    shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={shopId}&channel=7014&returnUrl={quote_plus(activityUrl)}"
    body = {"venderId": str(shopId), "channel": "7014"}
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888'
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'User-Agent': ua,
        'Accept-Language': 'zh-cn',
        'Referer': shopcard_url,
        'Accept-Encoding': 'gzip, deflate'
    }
    response = requests.get(url=url, headers=headers, timeout=5).text
    return json.loads(response)

def bindWithVender(cookie):
    try:
        shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={shopId}&channel=7014&returnUrl={quote_plus(activityUrl)}"
        body = {"venderId": shopId, "shopId": shopId, "bindByVerifyCodeFlag": 1,"registerExtend": {},"writeChildFlag":0, "channel": 7014}
        url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888&h5st=20220614102046318%3B7327310984571307%3Bef79a%3Btk02wa31b1c7718neoZNHBp75rw4pE%2Fw7fXko2SdFCd1vIeWy005pEHdm0lw2CimWpaw3qc9il8r9xVLHp%2Bhzmo%2B4swg%3Bdd9526fc08234276b392435c8623f4a737e07d4503fab90bf2cd98d2a3a778ac%3B3.0%3B1655173246318'
        headers = {
            'Host': 'api.m.jd.com',
            'Cookie': cookie,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': ua,
            'Referer': shopcard_url
        }
        response = requests.get(url=url, headers=headers, timeout=30).text
        res = json.loads(response)
        if res['success']:
            open_result = res['message']
            if "火爆" in open_result:
                logger.info(f"\t⛈⛈{open_result}")
            else:
                logger.info(f"\t🎉🎉{open_result}")
            return res['message']
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        logger.info("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global signUuid, inviteSuccNum, activityUrl, firstCk
    inviteSuccNum = 0
    signUuid = inviterUuid
    activityUrl = activity_url
    num = 0
    for cookie in cks:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 9 == 0:
            logger.info("⏰等待3s,休息一下")
            time.sleep(5)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        logger.info(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        logger.info(datetime.now())
        token = ''
        activityCookie = ''
        activityCookie = getActivity(token)
        try:
            token = getToken(cookie, r)
            if token is None:
                if num == 1:
                    logger.info(f"⚠️车头获取Token失败,退出本程序！")
                    sys.exit()
                logger.info(f"⚠️获取Token失败！⏰等待3s")
                time.sleep(3)
                continue
        except:
            logger.info(f"⚠️获取Token失败！⏰等待3s")
            time.sleep(3)
            continue
        time.sleep(0.5)
        getSystemConfigForNew(activityId)
        time.sleep(0.5)
        getSimpleActInfoVo(activityId)
        time.sleep(0.5)
        getPin = getMyPing(shopId, token, num)
        if getPin is not None:
            nickname = getPin[0]
            secretPin = getPin[1]
            time.sleep(0.5)
            accessLogWithAD(shopId, secretPin)
            time.sleep(0.5)
            actContent = activityContent(secretPin, signUuid)
            time.sleep(1)
            userInfo = getUserInfo(secretPin)
            nickname = userInfo[0]
            yunMidImageUrl = userInfo[1]
            pin = userInfo[2]
            logger.info(f"邀请码->: {actContent['signUuid']}")
            logger.info(f"准备助力->: {signUuid}")
            if actContent['canJoin']:
                logger.info("🎉加入队伍成功，请等待队长瓜分京豆")
                saveCandidate(signUuid, pin, yunMidImageUrl, nickname)
                logger.info("现在去开卡")
                time.sleep(1)
                if not actContent['openCard']:
                    try:
                        result1 = getShopOpenCardInfo(cookie)
                    except:
                        continue
                    if result1['result']['userInfo']['openCardStatus'] == 0:
                        open_result = bindWithVender(cookie)
                        if open_result is not None:
                            if "火爆" in open_result:
                                time.sleep(1.5)
                                logger.info("\t尝试重新入会 第1次")
                                open_result = bindWithVender(cookie)
                                if "火爆" in open_result:
                                    time.sleep(1.5)
                                    logger.info("\t尝试重新入会 第2次")
                                    open_result = bindWithVender(cookie)
                            if "加入店铺会员成功" in open_result:
                                inviteSuccNum += 1
                                logger.info(f"🛳🛳🛳助力成功,本次已邀请{inviteSuccNum}人")
                                # if inviteSuccNum >= 4:
                                #     sys.exit()
                    else:
                        logger.info("⛈疑似黑号,助力失败！")

                    time.sleep(1)
                    actContent1 = activityContent(pin, signUuid)
                    time.sleep(0.5)
                    if num == 1:
                        if actContent1['canCreate']:
                            logger.info("创建队伍")
                            time.sleep(0.5)
                            signUuid1 = saveCaptain(pin, yunMidImageUrl, nickname)
            else:
                if num == 1:
                    logger.info("创建队伍")
                    if actContent['canCreate']:
                        signUuid1 = saveCaptain(pin, yunMidImageUrl, nickname)
                    else:
                        logger.info("你已经是队长了")
                        signUuid0 = actContent['signUuid']
                        logger.info(f"队伍id->: {signUuid0}")
                else:
                    logger.info("无法加入队伍")
            if num == 1:
                signUuid = actContent['signUuid']
                activityUrl = f"https://lzkjdz-isv.isvjcloud.com/pool/captain/7409220?activityId={activityId}&signUuid={signUuid}"

        time.sleep(3)