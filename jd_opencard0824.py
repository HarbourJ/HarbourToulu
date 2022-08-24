#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 12:05
# @Author  : HarbourJ
# @File    : jd_opencard0824.py

"""
File: jd_opencard0824.py(家有萌宠 为爱而生)
Author: HarbourJ
Date: 2022/8/25 7:37
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 0 1 0 1-27 8,9 *
new Env('家有萌宠 为爱而生');
ActivityEntry: https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activity/5929859?activityId=dze115fd25c54e28a185e305a8fc5126&shareUuid=fb7e0185279d43c3a0fd892b401c677e&adsource=null&shareuserid4minipg=null&shopid=1000075792
Description: 每日限制成功邀请前10名好友，达到10上限自动停。邀请成功获得20豆，被邀请者获得10豆。
"""

import time
import requests
import sys
import re
import os
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
    "fb7e0185279d43c3a0fd892b401c677e",
    "da896f5a45a34660b87f6ab8e8b8c475",
]

inviterUuid = random.choice(inviterUuids)
activityId = "dze115fd25c54e28a185e305a8fc5126"
shopId = "1000075792"
activity_url = f"https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activity/5929859?activityId={activityId}&shareUuid={inviterUuid}&adsource=null&shareuserid4minipg=null&shopid={shopId}"

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
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 493:
            logger.info(response.status_code, "⚠️ip疑似黑了,休息一会再来撸~")
            sys.exit()
        if response.cookies:
            cookies = response.cookies.get_dict()
            set_cookies = [(set_cookie + "=" + cookies[set_cookie]) for set_cookie in cookies]
            set_cookie = ''.join(sorted([(set_cookie + ";") for set_cookie in set_cookies]))
        return set_cookie
    except:
        logger.info("⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def getSystemConfigForNew():
    url = "https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew"
    payload = f'activityId={activityId}&activityType=99'
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSimpleActInfoVo():
    url = "https://lzdz1-isv.isvjcloud.com/dz/common/getSimpleActInfoVo"
    payload = f"activityId={activityId}"
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        logger.info(res['errorMessage'])

def getMyPing(index, venderId):
    url = "https://lzdz1-isv.isvjcloud.com/customer/getMyPing"
    payload = f"userId={venderId}&token={token}&fromType=APP"
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

def accessLogWithAD(venderId, pin):
    url = "https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD"
    payload = f"venderId={venderId}&code=99&pin={quote_plus(pin)}&activityId={activityId}&pageUrl={quote_plus(activityUrl)}&subType=app&adSource=null"
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)

def getSystime():
    url = "https://lzdz1-isv.isvjcloud.com/common/getSystime"
    headers = {
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']['nickname'], res['data']['yunMidImageUrl'], res['data']['pin']
    else:
        logger.info(res['errorMessage'])

def activityContent(pin, pinImg):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activityContent"
    try:
        yunMidImageUrl = quote_plus(pinImg)
    except:
        yunMidImageUrl = quote_plus("https://img10.360buyimg.com/imgzone/jfs/t1/21383/2/6633/3879/5c5138d8E0967ccf2/91da57c5e2166005.jpg")
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&pinImg={quote_plus(yunMidImageUrl)}&nick={quote_plus(nickname)}&shareUuid={shareUuid}"
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
        'Cookie': f'IsvToken={token};{activityCookie}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_cookies(response)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        logger.info(res['errorMessage'])
        if "活动已结束" in res['errorMessage']:
            sys.exit()

def drawContent(actorUuid, pin):
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
        'Cookie': activityCookie
    }
    requests.request("POST", url, headers=headers, data=payload)

def checkOpenCard(pin, shareUuid):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/checkOpenCard"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&shareUuid={shareUuid}&actorUuid={actorUuid}"
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
        'Cookie':  f'IsvToken={token};{activityCookie}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res['result']:
        return res['data']
    else:
        logger.info(res['errorMessage'])

def getShareRecord(pin, actorUuid):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/getShareRecord"
    payload = f"activityId={activityId}&pin={quote_plus(pin)}&actorUuid={actorUuid}&num=50"
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # refresh_cookies(response)
    res = json.loads(response.text)
    if res['result']:
        logger.info(f"\n已累计邀请{len(res['data'])}人")

def saveTask(actorUuid, pin, taskType, taskValue, shareUuid):
    url = "https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/saveTask"
    payload = f"activityId={activityId}&actorUuid={actorUuid}&pin={quote_plus(pin)}&taskType={taskType}&taskValue={taskValue}&shareUuid={shareUuid}"
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
        'Cookie': activityCookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    if res['result']:
        data = res['data']
        if data['addBeanNum'] == 0:
            logger.info("\t获得 💨💨💨")
        else:
            logger.info(f"\t🎉获得{data['addBeanNum']}京豆")
    else:
        logger.info(res['errorMessage'])

def bindWithVender(cookie, venderId, shareUuid):
    try:
        shopcard_url0 = f"https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activity/7854908?activityId={activityId}&shareUuid={shareUuid}"
        shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=401&returnUrl={quote_plus(shopcard_url0)}"
        body = {"venderId": venderId, "bindByVerifyCodeFlag": 1,"registerExtend": {},"writeChildFlag":0, "channel": 401}
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
            return res['message']
    except Exception as e:
        logger.info(e)

def getShopOpenCardInfo(cookie, venderId):
    shopcard_url0 = f"https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activity/7854908?activityId={activityId}&shareUuid={shareUuid}"
    shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=401&returnUrl={quote_plus(shopcard_url0)}"
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
            'Referer': shopcard_url,
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.get(url=url, headers=headers, timeout=5).text
        res = json.loads(response)
        if res['success']:
            venderCardName = res['result']['shopMemberCardInfo']['venderCardName']
            return venderCardName
    except:
        return None


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        logger.info("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global shareUuid, inviteSuccNum, activityUrl, firstCk
    inviteSuccNum = 0
    shareUuid = inviterUuid
    activityUrl = activity_url
    num = 0
    for cookie in cks[:]:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 8 == 0:
            logger.info("⏰等待10s,休息一下")
            time.sleep(10)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        logger.info(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        logger.info(datetime.now())

        token = getToken(cookie, r)
        if token is None:
            if num == 1:
                logger.info(f"⚠️车头获取Token失败,退出本程序！")
                sys.exit()
            logger.info(f"⚠️获取Token失败！⏰等待3s")
            time.sleep(3)
            continue
        time.sleep(0.5)
        activityCookie = getActivity()
        time.sleep(0.5)
        getSystemConfigForNew()
        time.sleep(0.3)
        getSimAct = getSimpleActInfoVo()
        venderId = getSimAct['venderId']
        time.sleep(0.2)
        getPin = getMyPing(num, venderId)
        if getPin is not None:
            nickname = getPin[0]
            secretPin = getPin[1]
            time.sleep(0.3)
            accessLogWithAD(venderId, secretPin)
            time.sleep(0.5)
            userInfo = getUserInfo(secretPin)
            time.sleep(0.3)
            nickname = userInfo[0]
            yunMidImageUrl = userInfo[1]
            pin = userInfo[2]
            actContent = activityContent(pin, yunMidImageUrl)
            if not actContent:
                if num == 1:
                    logger.info("⚠️无法获取车头邀请码,退出本程序！")
                    sys.exit()
                continue
            endTime = actContent['endTime']
            if getJdTime() > endTime:
                logger.info("活动已结束，下次早点来~")
            actorUuid = actContent['actorUuid']
            followShop = actContent['followShop']
            skuAddCart = actContent['addSku']
            logger.info(f"邀请码->: {actorUuid}")
            logger.info(f"准备助力->: {shareUuid}")
            time.sleep(0.5)
            initOpen = checkOpenCard(pin, shareUuid)
            time.sleep(0.5)
            drawContent(actorUuid, pin)
            if initOpen:
                assist = False
                assistStatus = initOpen['assistStatus']
                if assistStatus == 2:
                    logger.info("已经助力过你~")
                elif assistStatus == 3:
                    logger.info("已助力过其他好友~")
                elif assistStatus == 1:
                    logger.info("已完成开卡关注任务,未助力过好友~")
                    assist = True
                elif assistStatus == 77:
                    logger.info("无法助力自己~")
                else:
                    logger.info("现在去开卡~")
                    assist = False
                assistStatus = initOpen['sendStatus']
                if initOpen['allOpenCard']:
                    logger.info("已完成全部开卡")
                else:
                    assist = True
                    # logger.info("现在去开卡")
                    unOpenId = []
                    openInfo = initOpen['openInfo']
                    for info in openInfo:
                        if info['openStatus'] == 0:
                            unOpenId.append(info['venderId'])
                    for venderId in unOpenId:
                        getShopInfo = getShopOpenCardInfo(cookie, venderId)
                        if not getShopInfo:
                            venderCardName = ''
                        else:
                            venderCardName = getShopInfo
                        open_result = bindWithVender(cookie, venderId, shareUuid)
                        if open_result is not None:
                            if "火爆" in open_result:
                                time.sleep(1.5)
                                logger.info("\t尝试重新入会 第1次")
                                open_result = bindWithVender(cookie)
                                if "火爆" in open_result:
                                    time.sleep(1.5)
                                    logger.info("\t尝试重新入会 第2次")
                                    open_result = bindWithVender(cookie)
                            if "火爆" in open_result:
                                logger.info(f"\t⛈⛈{venderCardName} {open_result}")
                            else:
                                logger.info(f"\t🎉🎉{venderCardName} {open_result}")
                        time.sleep(0.5)
            time.sleep(0.5)
            if followShop:
                logger.info("已完成关注店铺任务")
            else:
                logger.info("现在去一键关注店铺")
                saveTask(actorUuid, pin, 23, '', shareUuid)
            initOpen0 = checkOpenCard(pin, shareUuid)
            if assist and initOpen0['assistStatus'] == 2 or initOpen0['assistStatus'] == 1 and initOpen0['allOpenCard']:
                logger.info("🎉🎉🎉助力成功！")
                inviteSuccNum += 1
                if inviteSuccNum >= 10:
                    logger.info(f"已邀请{inviteSuccNum}人,退出程序")
                else:
                    logger.info(f"已邀请{inviteSuccNum}人")

            if not skuAddCart:
                logger.info("现在去一键加购")
                saveTask(actorUuid, pin, 21, 1, shareUuid)
            if num == 1:
                getShareRecord(pin, actorUuid)
                logger.info(f"后面账号全部助力 {actorUuid}")
            if num == 1:
                shareUuid = actorUuid
                activityUrl = f"https://lzdz1-isv.isvjcloud.com/dingzhi/petkk/active/activity/7854908?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg=null&shopid={shopId}"

        time.sleep(3)