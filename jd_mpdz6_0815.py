#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_mpdz6_0815.py(畅享一夏 消费赢壕礼)
Author: HarbourJ
Date: 2022/8/15 22:37
TG: https://t.me/HarbourToulu
cron: 1 0 0,18 15-25 8 *
new Env('8.15-8.25 畅享一夏 消费赢壕礼');
活动入口：19(W7tbW6VkKB)，【/ Jiιngㅛ諌】来京东，更超值
"""

import time
import requests
import sys
import re
from base64 import b64encode, b64decode
from urllib.parse import urlencode
from datetime import datetime
import json
import random
from urllib.parse import quote, unquote
from urllib.parse import quote_plus, unquote_plus
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from jd_sign import *

redis_url = "172.17.0.1"

activity_urls = ["https://mpdz6-dz.isvjcloud.com/jdbeverage/pages/Summer0815/summer?bizExtString=c2hhcmVOaWNrOk55MG0xSzF0VkhJSnZ0MGo0U1E5UmJSUFhNSEhmJTJCRHJObU1WZlQ4UzVocTNTallNQUFDcmJFSFpRNDBKNXlQWQ==", "https://mpdz6-dz.isvjcloud.com/jdbeverage/pages/Summer0815/summer?bizExtString=c2hhcmVOaWNrOnBXR1VXWkpRM2FjdGV4MFgydlF5THNqTmhOYVlGeTJIdGVFckU2aXpsaFRmOW5yR1k3Z0JrQ2RHVTRDNnolMkZ4RA=="]
activity_url = random.choice(activity_urls)

def redis_conn():
    try:
        import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=6379, decode_responses=True, socket_connect_timeout=5)
            r = redis.Redis(connection_pool=pool)
            r.get('conn_test')
            print('✅redis连接成功')
            return r
        except:
            print("⚠️redis连接异常")
    except:
        print("⚠️缺少redis依赖，请运行pip3 install redis")

def getToken(ck, r=None):
    if r is not None:
        Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{ck}')
        # print("Token过期时间", r.ttl(f'{activityUrl.split("https://")[1].split("-")[0]}_{ck}'))
        if Token is not None:
            print(f"♻️获取缓存Token->: {Token}")
            return Token
        else:
            print("🈳去设置Token缓存-->")
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
            # print(sign_txt)
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                print(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    print("获取token失败！")
                    return
            Token_new = f.json()['token']
            print(f"Token->: {Token_new}")
            if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{ck}', Token_new, ex=1800):
                print("✅Token缓存设置成功")
            else:
                print("❌Token缓存设置失败")
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
        # print(sign_txt)
        f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
        if f.status_code != 200:
            print(f.status_code)
            return
        else:
            if "参数异常" in f.text:
                print("获取token失败！")
                return
        Token = f.json()['token']
        print(f"Token->: {Token}")
        return Token

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

def getActivity(token):
    url = activityUrl
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': f'IsvToken={token};',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    requests.request("GET", url, headers=headers)
#加载活动信息,获得buyerNick
def loadActivity(token):
    url = "https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/activity/load?open_id=&mix_nick=&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"admJson": {"buyerNick": "", "method": "/jdUnionOrder/activity/load", "jdToken": token, "userId": 10299171, "source": "01", "actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "inviteNick": "BrhkV49OBlcgmCGIvW/S6Fs/ye9oluZX4nOTK56TeMXbR7I2OlzZch4hTs22oCUS"}, "commonParameter": {"sign": "47a0586b4d3941faaa7b7abdc59a0d1d", "timestamp": getJdTime(), "userId": 10299171, "m": "POST"}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    # print('loadActivity', response.text)
    return json.loads(response.text)
# 记录成功
def temporary(buyerNick, type):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/report/temporary?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "b33ba430a0fa63f9cfe728b65746e57c", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "type": type, "method": "/jdUnionOrder/report/temporary", "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    temporary = json.loads(response.text)
    if temporary['success']:
        temporary['data']['msg']
# 开卡信息
def shopList(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/shop/shopList?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1f357ae84ac8013e9a1a09425c1b8cbf", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "method": "/jdUnionOrder/shop/shopList", "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    open_shopList = json.loads(response.text)
    # print('open_shopList', open_shopList)
    unopen_shopList = []
    if open_shopList['success']:
        open_shopList = open_shopList['data']['data']
        for shop in open_shopList:
            if not shop['open']:
                unopen_shopList.append(shop)
    else:
        return
    return unopen_shopList
# 任务完成信息(分享)
def completeMissionShareAct(index=1, buyerNick=None):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/mission/completeMission?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "missionType": "shareAct", "method": "/jdUnionOrder/mission/completeMission", "userId": 10299171, "inviterNick": shareNick, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    completeMission = json.loads(response.text)
    # print('completeMission', response.text)
    if completeMission['success']:
        if completeMission['data']['status'] == 200:
            remark = completeMission['data']['data']['remark']
            if index == 1:
                if "助力成功" in remark:
                    print(f"\tCK1助力船长~")
                else:
                    print(f"\t🛳{remark}")
            else:
                print(f"\t🛳{remark}")
        else:
            msg = completeMission['data']['msg']
            print(f"\t🛳{msg}")
    else:
        errorMessage = completeMission['errorMessage']
        print(errorMessage)
# 邀请列表
def inviteList(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/customer/inviteList?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "inviteType": 1, "method": "/jdUnionOrder/customer/inviteList", "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    inviteList = json.loads(response.text)
    # print('inviteList', response.text)
    if inviteList['success']:
        data = inviteList['data']['data']
        # inviteNum = data['inviteNum']
        inviteNum = data['pageInfo']['total']
        print(f"\t🎉已成功邀请{inviteNum}人")
    else:
        errorMessage = inviteList['errorMessage']
        print(errorMessage)
# 任务完成信息(关注)
def completeMission(buyerNick, missionType):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/mission/completeMission?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "missionType": missionType, "method": "/jdUnionOrder/mission/completeMission", "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    completeMission = json.loads(response.text)
    # print('completeMission', response.text)
    if completeMission['success']:
        if completeMission['data']['status'] == 200:
            remark = completeMission['data']['data']['remark']
            print(f"\t🛳{remark}")
        else:
            msg = completeMission['data']['msg']
            print(f"\t🛳{msg}")
    else:
        errorMessage = completeMission['errorMessage']
        print(errorMessage)
# 任务完成信息(开卡)
def completeMissionCard(buyerNick, venderId, missionType):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/mission/completeMission?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "c095088c95d508bf1bb2fb0742621559", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "missionType": missionType, "method": "/jdUnionOrder/mission/completeMission", "shopId": venderId, "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    completeMission = json.loads(response.text)
    if completeMission['success']:
        remark = completeMission['data']['data']['remark']
        if "开卡成功" in remark:
            print(f"\t🎉🎉{remark}")
        else:
            print(f"⛈⛈{remark}")
    else:
        errorMessage = completeMission['data']
        print(errorMessage)
# 开卡信息
def shopmember(venderId, cookie):
    shopcard_url = quote_plus(f"{activityUrl}?joinShopId={venderId}")
    url = f"https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=401&returnUrl={shopcard_url}"
    headers = {
        'Host': 'shopmember.m.jd.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://mpdz6-dz.isvjcloud.com/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    requests.request("GET", url, headers=headers)
# 检查开卡状态
def getShopOpenCardInfo(body, venderId, cookie, ua):
    shopcard_url0 = quote_plus(f"{activityUrl}?joinShopId={venderId}")
    shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=401&returnUrl={shopcard_url0}"
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
# 开卡入会
def bindWithVender(cookie, venderId, body):
    try:
        shopcard_url0 = quote_plus(f"{activityUrl}?joinShopId={venderId}")
        shopcard_url = f"https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=401&returnUrl={shopcard_url0}"
        url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888&h5st=20220614090341129%3B0284392757226553%3Bef79a%3Btk02wcbf51cf018njrSeb2PERKoZxKtLTPV0g0paq33tkJwK4bJurufnMpBuFkn4RVxkfBmwRhN8VRd%2BB2q%2BrzaXvMR7%3B3f2a1efdb5f2b79e17aa8836a38af77030ad35b4aab128c11e3edbaa034c1733%3B3.0%3B1655168621129'
        header = {
            'Host': 'api.m.jd.com',
            'Cookie': cookie,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': ua,
            'Referer': shopcard_url
        }
        response = requests.get(url=url, headers=header, timeout=30).text
        return json.loads(response)
    except Exception as e:
        print(e)
# 检查开卡信息
def checkOpenCard(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdUnionOrder/customer/checkOpenCard?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "e291a2c8b9625c637d743c3b0e52f1d8", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "47a0586b4d3941faaa7b7abdc59a0d1d", "method": "/jdUnionOrder/customer/checkOpenCard", "userId": 10299171, "buyerNick": buyerNick}}}
    headers = {
        'Host': 'mpdz6-dz.isvjcloud.com',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://mpdz6-dz.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    checkOpenCard = json.loads(response.text)
    # print('checkOpenCard', checkOpenCard)
    if checkOpenCard['success']:
        msg = checkOpenCard['data']['msg']
        print(msg)
    else:
        errorMessage = checkOpenCard['data']
        print(errorMessage)


if __name__ == '__main__':
    r = redis_conn()
    num = 0
    global activityUrl, buyerNick, shareNick
    activityUrl = None
    shareNick = None
    buyerNick = None
    for ck in cks:
        num += 1
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(ck)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())
        ua = userAgent()
        if num == 1:
            activityUrl = activity_url
        if num <= 2:
            buyerInfo = buyerUrl6(num, activityUrl, buyerNick)
            activityUrl = buyerInfo[0]
            shareNick = buyerInfo[1]
        try:
            token = getToken(ck, r)
            if token is None:
                continue
        except:
            continue
        time.sleep(1)
        getActivity(token)
        time.sleep(1)
        LA = loadActivity(token)
        if LA['success']:
            buyerNick = LA['data']['data']['missionCustomer']['buyerNick']
            buyerNick_nickName = LA['data']['data']['missionCustomer']['nickName']
            buyerNick_headPicUrl = LA['data']['data']['missionCustomer']['headPicUrl']
            print(f"邀请码->: {buyerNick}")
            time.sleep(1)
            print("现在去做助力任务")
            print(f"\t准备助力->: {shareNick}")
            temporary(buyerNick, "pv")
            shopList0 = shopList(buyerNick)
            time.sleep(1)
            completeMissionShareAct(num, buyerNick)
            time.sleep(1)
            inviteList(buyerNick)
            print("现在去做关注任务")
            temporary(buyerNick, "guanzhu")
            completeMission(buyerNick, "uniteCollectShop")
            time.sleep(0.5)
            if shopList0 is not None:
                print("现在去做开卡任务")
                if len(shopList0) > 0:
                    # print("现在去做开卡任务")
                    for shop0 in shopList0:
                        shopTitle = shop0['shopTitle']
                        venderId = shop0['userId']
                        shopId = shop0['shopId']
                        temporary(buyerNick, "kaika")
                        completeMissionCard(buyerNick, venderId, "openCard")
                        time.sleep(0.5)
                        shopmember(venderId, ck)
                        time.sleep(0.5)
                        # 检查入会状态
                        try:
                            result1 = getShopOpenCardInfo({"venderId": str(venderId), "channel": "401"}, venderId, ck,
                                                          ua)
                            # print(result1)
                        except:
                            continue
                        try:
                            if result1['result']['userInfo']['openCardStatus'] == 0:
                                ruhui = bindWithVender(ck, venderId,
                                                       {"venderId": str(venderId), "bindByVerifyCodeFlag": 1,
                                                        "registerExtend": {}, "writeChildFlag": 0,
                                                        "activityId": 2599647, "channel": 401})
                                print(f"\t{shopTitle} {ruhui['message']}")
                                if "火爆" in str(ruhui) or "失败" in str(ruhui):
                                    print("尝试重新入会 第1次")
                                    time.sleep(2.5)
                                    ruhui = bindWithVender(ck, venderId,
                                                           {"venderId": str(venderId), "bindByVerifyCodeFlag": 1,
                                                            "registerExtend": {}, "writeChildFlag": 0,
                                                            "activityId": 2599647, "channel": 401})
                                    print(f"\t{shopTitle} {ruhui['message']}")
                                    if "火爆" in str(ruhui) or "失败" in str(ruhui):
                                        print("尝试重新入会 第2次")
                                        time.sleep(2.5)
                                        ruhui = bindWithVender(ck, venderId, {"venderId": str(venderId),
                                                                              "bindByVerifyCodeFlag": 1,
                                                                              "registerExtend": {},
                                                                              "writeChildFlag": 0,
                                                                              "activityId": 2599647,
                                                                              "channel": 401})
                                        print(f"\t{shopTitle} {ruhui['message']}")
                            # **********************
                            getActivity(token)
                            time.sleep(0.5)
                            loadActivity(token)
                            temporary(buyerNick, "pv")
                            time.sleep(0.5)
                            completeMissionCard(buyerNick, venderId, "openCard")
                            time.sleep(0.5)
                            shopList1 = shopList(buyerNick)
                            if len(shopList1) == 0:
                                print("😆开卡任务已完成")
                            time.sleep(0.5)
                            # inviteList(buyerNick)
                            # time.sleep(0.5)
                        except:
                            continue
                else:
                    print("\t已全部开卡")
                temporary(buyerNick, "fenxiang")
                checkOpenCard(buyerNick)
                time.sleep(1)