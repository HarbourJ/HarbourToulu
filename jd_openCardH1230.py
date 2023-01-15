#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_openCardH1230.py(12.28-1.15 年货大牌,下单领好礼)
Author: HarbourJ
Date: 2022/12/30 00:00
TG: https://t.me/HarbourToulu
cron: 1 0 6,18 28-30,1-15 12,1 *
new Env('12.28-1.15 年货大牌,下单领好礼');
活动入口：10:/来京东，更超值，➠Jℹ️ng☆岽！I8KAe4kIeq0N！
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
    sys.exit()
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""

activity_urls = ["https://mpdz6-dz.isvjcloud.com/jdbeverage/pages/nianhuojie/nianhuojie?bizExtString=c2hhcmVOaWNrOk55MG0xSzF0VkhJSnZ0MGo0U1E5UmJSUFhNSEhmJTJCRHJObU1WZlQ4UzVocTNTallNQUFDcmJFSFpRNDBKNXlQWQ=="]
activity_url = random.choice(activity_urls)
# nianhuojie/nianhuojie

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
        pt_pin = unquote_plus(re.compile(r'pt_pin=(.*?);').findall(ck)[0])
    except:
        pt_pin = ck[:15]
    try:
        try:
            Token = r.get(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}')
        except Exception as e:
            # print(f"redis get error: {str(e)}")
            Token = None
        if Token is not None:
            print(f"♻️获取缓存Token")
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
            f = s.post('https://api.m.jd.com/client.action', verify=False, timeout=30)
            if f.status_code != 200:
                print(f.status_code)
                return
            else:
                if "参数异常" in f.text:
                    print(f.text)
                    return
            Token_new = f.json()['token']
            try:
                if r.set(f'{activityUrl.split("https://")[1].split("-")[0]}_{pt_pin}', Token_new, ex=1800):
                    print("✅Token缓存成功")
                else:
                    print("❌Token缓存失败")
            except Exception as e:
                # print(f"redis set error: {str(e)}")
                print(f"✅获取实时Token")
            return Token_new
    except Exception as e:
        print(f"Get Token Error: {str(e)}")
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
    url = "https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/activity/load?open_id=&mix_nick=&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"admJson": {"buyerNick": "", "method": "/jdNewYearsFestival/activity/load", "jdToken": token, "userId": 10299171, "source": "01", "actId": "jdNewYearsFestivalunion", "inviteNick": "BrhkV49OBlcgmCGIvW/S6Fs/ye9oluZX4nOTK56TeMXbR7I2OlzZch4hTs22oCUS"}, "commonParameter": {"sign": "c754077b488af94d2da76ec5419f1316", "timestamp": getJdTime(), "userId": 10299171, "m": "POST"}}}
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
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/report/temporary?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "b33ba430a0fa63f9cfe728b65746e57c", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "type": type, "method": "/jdNewYearsFestival/report/temporary", "userId": 10299171, "buyerNick": buyerNick}}}
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

def shopList(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/shop/shopList?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1f357ae84ac8013e9a1a09425c1b8cbf", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "method": "/jdNewYearsFestival/shop/shopList", "userId": 10299171, "buyerNick": buyerNick}}}
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

def completeState(index=1, buyerNick=None):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/mission/completeState?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "missionType": "shareAct", "method": "/jdNewYearsFestival/mission/completeState", "userId": 10299171, "buyerNick": buyerNick}}}
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
    complete_state = json.loads(response.text)
    print('completeState', response.text)
    # if completeMission['success']:
    #     if completeMission['data']['status'] == 200:
    #         remark = completeMission['data']['data']['remark']
    #         if index == 1:
    #             if "助力成功" in remark:
    #                 print(f"\tCK1助力船长~")
    #             else:
    #                 print(f"\t🛳{remark}")
    #         else:
    #             print(f"\t🛳{remark}")
    #     else:
    #         msg = completeMission['data']['msg']
    #         print(f"\t🛳{msg}")
    # else:
    #     errorMessage = completeMission['errorMessage']
    #     print(errorMessage)

def inviteList(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/customer/inviteList?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "inviteType": 1, "method": "/jdNewYearsFestival/customer/inviteList", "userId": 10299171, "buyerNick": buyerNick}}}
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
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/mission/completeMission?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "1b96d3a4e5f083eaf631ebbfe8dc4c0e", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "missionType": missionType, "method": "/jdNewYearsFestival/mission/completeMission", "userId": 10299171, "buyerNick": buyerNick}}}
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
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/mission/completeMission?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "c095088c95d508bf1bb2fb0742621559", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "missionType": missionType, "method": "/jdNewYearsFestival/mission/completeMission", "shopId": venderId, "userId": 10299171, "buyerNick": buyerNick}}}
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
        if completeMission['data']['status'] == 200:
            remark = completeMission['data']['data']['remark']
            if "开卡成功" in remark:
                print(f"\t🎉🎉{remark}")
            else:
                print(f"⛈⛈{remark}")
        else:
            msg = completeMission['data']['msg']
            print(f"\t🛳{msg}")
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

def getShopOpenCardInfo(cookie, venderId, ua):
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

def bindWithVender(cookie, venderId, ua):
    try:
        s.headers = {
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
        s.params = {
            'appid': 'jd_shop_member',
            'functionId': 'bindWithVender',
            'body': json.dumps({
                'venderId': venderId,
                'shopId': venderId,
                'bindByVerifyCodeFlag': 1
            }, separators=(',', ':'))
        }
        res = s.post('https://api.m.jd.com/', verify=False, timeout=30).json()
        if res['success']:
            return res['message']
    except Exception as e:
        print(e)

def checkOpenCard(buyerNick):
    url = f"https://mpdz6-dz.isvjcloud.com/dm/front/jdNewYearsFestival/customer/checkOpenCard?open_id=&mix_nick={buyerNick}&user_id=10299171"
    payload = {"jsonRpc": "2.0", "params": {"commonParameter": {"m": "POST", "sign": "e291a2c8b9625c637d743c3b0e52f1d8", "timestamp": getJdTime(), "userId": 10299171}, "admJson": {"actId": "jdNewYearsFestivalunion", "method": "/jdNewYearsFestival/customer/checkOpenCard", "userId": 10299171, "buyerNick": buyerNick}}}
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
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
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
                        getShopOpenCardInfo(ck, venderId, ua)
                        open_result = bindWithVender(ck, venderId, ua)
                        if open_result is not None:
                            if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                                print(f"\t⛈⛈{shopTitle} {open_result}")
                                break
                            else:
                                print(f"\t🎉🎉{shopTitle} {open_result}")
                        time.sleep(1.5)
                else:
                    print("\t已全部开卡")
                temporary(buyerNick, "fenxiang")
                checkOpenCard(buyerNick)
                time.sleep(1)