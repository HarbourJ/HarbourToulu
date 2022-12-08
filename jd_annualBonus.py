#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_annualBonus.py(年终奖-助力)
Author: HarbourJ
Date: 2022/12/8 13:53
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('年终奖-助力');
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

inviteId = os.environ.get("inviteId") if os.environ.get("inviteId") else ""

if not inviteId:
    print("⚠️未发现有效助力码,退出程序!")
    sys.exit()

def check(ua, ck):
    try:
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
        header = {
            "Host": "me-api.jd.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": ck,
            "User-Agent": ua,
            "Accept-Language": "zh-cn",
            "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
            "Accept-Encoding": "gzip, deflate",
        }
        result = requests.get(url=url, headers=header, timeout=None).text
        codestate = json.loads(result)
        if codestate['retcode'] == '1001':
            msg = "⚠️当前ck已失效，请检查"
            return {'code': 1001, 'data': msg}
        elif codestate['retcode'] == '0' and 'userInfo' in codestate['data']:
            nickName = codestate['data']['userInfo']['baseInfo']['nickname']
            return {'code': 200, 'name': nickName, 'ck': ck}
    except Exception as e:
        return {'code': 0, 'data': e}

def splitHongbao_getHomeData(ua, ck, inviteId):
    url = 'https://api.m.jd.com/client.action'
    headers = {
        'Host': 'api.m.jd.com',
        'Origin': 'https://h5.m.jd.com',
        'Referer': 'https://h5.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Cookie': ck,
        'User-Agent': ua,
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    taskToken = {"appId": "1EFVXyw", "taskToken": inviteId}
    body = f"functionId=splitHongbao_getHomeData&appid=&area=&body={json.dumps(taskToken)}&client=wh5&clientVersion=1.0.0"
    try:
        response = requests.request("POST", url, headers=headers, data=body)
        res = response.json()
        if res['code'] == 0:
            print(res['data'])
            print("✅助力成功！")
        else:
            print(res['msg'])
    except Exception as e:
        print(str(e))

def harmony_collectScore(ua, ck, inviteId):
    url = 'https://api.m.jd.com/client.action'
    headers = {
        'Host': 'api.m.jd.com',
        'Origin': 'https://h5.m.jd.com',
        'Referer': 'https://h5.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Cookie': ck,
        'User-Agent': ua,
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    taskToken = {"appId": "1EFVXyw", "taskToken": inviteId, "taskId": 6, "actionType": 0}
    body = f"functionId=harmony_collectScore&appid=&area=&body={json.dumps(taskToken)}&client=wh5&clientVersion=1.0.0"
    try:
        response = requests.request("POST", url, headers=headers, data=body)
        res = response.json()
        if res['code'] == 0:
            print(res['data'])
            # print("✅助力成功！")
        else:
            print(res['msg'])
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    num = 0
    for cookie in cks[:]:
        num += 1
        if num % 9 == 0:
            print("⏰等待5s,休息一下")
            time.sleep(5)
        global ua
        ua = userAgent(False)[1]
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        result = check(ua, cookie)
        if result['code'] != 200:
            print(f"‼️{result['data']}")
            continue

        print(f"🤖现在去助力{inviteId}")
        splitHongbao_getHomeData(ua, cookie, inviteId)
        time.sleep(1)
        harmony_collectScore(ua, cookie, inviteId)
        time.sleep(1)










