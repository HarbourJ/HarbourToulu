#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_schoolRoom.py(宿舍大作战)
Author: HarbourJ
Date: 2022/03/23 12:00
TG: https://t.me/HarbourToulu
cron: 7 7 7 7 7
new Env('宿舍大作战');
活动入口: https://xinrui-isv.isvjcloud.com/school/
"""


import time, requests, sys, re, os, json, random
from urllib.parse import quote_plus, unquote_plus
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=DeprecationWarning)
from functools import partial
print = partial(print, flush=True)

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
    sys.exit(3)

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""

activity_url = f"https://xinrui-isv.isvjcloud.com/school/"
print(f"【🛳活动入口】{activity_url}")

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
                print(f"✅获取实时Token")
            return Token_new
    except Exception as e:
        print(f"Token error: {str(e)}")
        return

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def getActivity():
    url = activityUrl
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,image/tpg,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'X-Requested-With': 'com.jingdong.app.mall',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': f'IsvToken={token}'
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return
    else:
        print(response.status_code)
        print("⚠️疑似ip黑了")
        sys.exit()

def getAuth():
    url = f"https://xinrui-isv.isvjcloud.com/auth/jos?token={token}&jd_source=01&is_share=0"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'App-Key': '6myeMAtP',
        'User-Agent': ua,
        'X-Requested-With': 'com.jingdong.app.mall',
        'Referer': activityUrl,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        response = requests.request("POST", url, headers=headers)
        res = response.json()
        if res['status'] == 0:
            return res['body']['access_token']
        else:
            print(f"⚠️getAuth: {res}")
    except Exception as e:
        print(f"getAuth Error: {str(e)}")

def getUserInfo(authToken):
    url = "https://xinrui-isv.isvjcloud.com/jd-school-room-api/api/info?is_share=0&source=zhuhuichang&channel=2"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'App-Key': '6myeMAtP',
        'Authorization': f'Bearer {authToken}',
        'is-wechat': '0',
        'X-Requested-With': 'com.jingdong.app.mall',
        'User-Agent': ua,
        'Referer': activityUrl,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        response = requests.request("GET", url, headers=headers)
        res = response.json()
        if res['status'] == 0:
            rooms = res['body']['rooms']
            room_order_num = res['body']['room_order_num']
            user = res['body']['user']
            return rooms, room_order_num, user
        else:
            print(f"获取信息失败：{res['message']}")
    except Exception as e:
        print(f"getUserInfo Error: {e}")

def assist(authToken, shareUuid):
    url = f"https://xinrui-isv.isvjcloud.com/jd-school-room-api/api/assist?inviter_id={shareUuid}&is_share=0&source=zhuhuichang&channel=2"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'App-Key': '6myeMAtP',
        'Authorization': f'Bearer {authToken}',
        'Sec-Fetch-Site': 'same-origin',
        'is-wechat': '0',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://xinrui-isv.isvjcloud.com',
        'User-Agent': ua,
        'Referer': activityUrl,
        'Accept': 'application/json, text/plain, */*',
        'Cookie': 'jcloud_alb_route=cae1c2c57ae205418df0ab4fa6c31b28'
    }
    try:
        response = requests.request("POST", url, headers=headers)
        res = response.json()
        # print(f"assist:{res}")
        status = res['status']
        message = res['message']
        body = res['body']
        if status == 0:
            print(f"助力结果: {message}")
        else:
            message = res['message']
            print(f"助力结果: {message}")
        return status, message, body
    except Exception as e:
        print(f"assist Error: {str(e)}")

def lottery_num_tips(authToken):
    url = "https://xinrui-isv.isvjcloud.com/jd-school-room-api/api/lottery-num-tips?is_share=0&source=zhuhuichang&channel=2"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'App-Key': '6myeMAtP',
        'Authorization': f'Bearer {authToken}',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'is-wechat': '0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ua,
        'Referer': activityUrl
    }
    try:
        response = requests.request("GET", url, headers=headers)
        res = response.json()
        print(f"lottery: {res}")
        if res['status'] == 0:
            body = res['body']
            invite_num_tip = body['invite_num_tip']
            order_num_tip = body['order_num_tip']
            print(f"当前邀请人数：{invite_num_tip}, 下单人数：{order_num_tip}")
            return invite_num_tip, order_num_tip
        else:
            message = res['message']
            print(f"lottery_num_tips: {message}")
    except Exception as e:
        print(f"lottery_num_tips Error: {str(e)}")
    # {"status": 0, "message": "ok", "body": {"invite_num_tip": "0", "order_num_tip": "0"}}

def lottery(authToken):
    url = "https://xinrui-isv.isvjcloud.com/jd-school-room-api/api/prize/lottery?is_share=0&source=zhuhuichang&channel=2"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'App-Key': '6myeMAtP',
        'Authorization': f'Bearer {authToken}',
        'is-wechat': '0',
        'Origin': 'https://xinrui-isv.isvjcloud.com',
        'X-Requested-With': 'com.jingdong.app.mall',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': ua,
        'Referer': activityUrl
    }
    try:
        response = requests.request("POST", url, headers=headers)
        res = response.json()
        # print(f"lottery: {res}")
        if res['status'] == 0:
            body = res['body']
            prize_type = body['user_prize']['prize_type']
            prize_name = body['user_prize']['prize_name']
            quota = body['user_prize']['prize_info']['quota']
            if prize_type == 1:
                print(f"🎁获得:{prize_name} {quota}")
            else:
                print(f"🎁获得:{prize_name}")
            return res
        else:
            message = res['message']
            print(f"抽奖结果: {message}")
    except Exception as e:
        print(f"lottery Error: {str(e)}")

def school_share(authToken):
    url = "https://xinrui-isv.isvjcloud.com/burying/stat?action=school-share&is_share=0&source=zhuhuichang&channel=2 HTTP/1.1:"
    headers = {
        'Host': 'xinrui-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'App-Key': '6myeMAtP',
        'Authorization': f'Bearer {authToken}',
        'is-wechat': '0',
        'Origin': 'https://xinrui-isv.isvjcloud.com',
        'X-Requested-With': 'com.jingdong.app.mall',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': ua,
        'Referer': activityUrl
    }
    requests.request("POST", url, headers=headers)


if __name__ == '__main__':
    r = redis_conn()
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global shareUuid, inviteSuccNum, activityUrl, firstCk, allCookies
    inviteSuccNum = 0
    try:
        brand = "xinrui"
        shareUuid = remote_redis(brand, 1)
        if not shareUuid:
            shareUuid = "40555"
    except:
        shareUuid = "40555"
    activityUrl = f"https://xinrui-isv.isvjcloud.com/school/?share_type=invite&inviter_token={shareUuid}&source=zhuhuichang&sid=3e1fc7c1470b8f70499c018ee2af115w&un_area=15_1213_71706_717"
    allCookies = cks
    num = 0
    for cookie in allCookies[:]:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 6 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(3)
        global ua, activityCookie, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')

        print(datetime.now())
        token = None
        token = getToken(cookie, r)
        if token is None:
            if num == 1:
                print(f"⚠️车头获取Token失败,退出本程序！")
                sys.exit()
            print(f"⚠️获取Token失败！⏰等待3s")
            time.sleep(3)
            continue
        time.sleep(0.3)
        getActivity()
        time.sleep(0.1)
        authToken = getAuth()
        if not authToken:
            if num == 1:
                print("‼️车头为火爆号,换车头重新运行！")
                sys.exit()
            else:
                print("📝移除火爆账号")
                time.sleep(1.5)
                continue
        time.sleep(0.1)
        userInfo = getUserInfo(authToken)
        if not userInfo:
            if num == 1:
                sys.exit()
            else:
                time.sleep(1.5)
                continue
        rooms, room_order_num, user = userInfo[0], userInfo[1], userInfo[2]
        # print(rooms, room_order_num, user)
        shareUuid1 = user['id']
        print(f"🤖助力码: {shareUuid1}")
        time.sleep(0.1)
        if num == 1:
            if rooms:
                inviteSuccNum = len(rooms) - 1
            print(f"🧑‍🤝‍🧑CK1已邀请{inviteSuccNum}人")
            if inviteSuccNum >= 5:
                lottery_num = lottery_num_tips(authToken)
                for i in range(50):
                    invite_type = i + 1
                    print(f"开始第{invite_type}次抽奖")
                    drawPrize = lottery(authToken)
                    try:
                        if drawPrize:
                            continue
                        else:
                            break
                    except Exception as e:
                        print(f"抽奖有误: {e}")
                sys.exit()
        time.sleep(0.1)
        assistInfo = assist(authToken, shareUuid)
        exit_flag = False
        if assistInfo:
            if assistInfo[0] == 0:
                inviteSuccNum += 1
                print(f"🎉助力成功！已邀请{inviteSuccNum}人")
            else:
                if assistInfo[1] == "请先认证校园身份" and num == 1:
                    exit_flag = True
                elif assistInfo[1] == "宿舍已经满员了" and num != 1:
                    exit_flag = True
        for i in range(50):
            invite_type = i + 1
            print(f"开始第{invite_type}次抽奖")
            drawPrize1 = lottery(authToken)
            try:
                if drawPrize1:
                    continue
                else:
                    break
            except Exception as e:
                print(f"抽奖有误: {e}")
        if exit_flag:
            sys.exit()
        time.sleep(0.1)
        school_share(authToken)

        if inviteSuccNum >= 5:
            print(f"已邀请{inviteSuccNum}人")
            token = getToken(firstCk, r)
            time.sleep(0.1)
            getActivity()
            time.sleep(0.1)
            authToken0 = getAuth()
            time.sleep(0.1)
            getUserInfo(authToken0)
            time.sleep(0.1)
            for i in range(6):
                invite_type = i + 1
                print(f"开始第{invite_type}次抽奖")
                drawPrize0 = lottery(authToken0)
                try:
                    if drawPrize0:
                        continue
                    else:
                        break
                except Exception as e:
                    print(f"抽奖有误: {e}")
            sys.exit()

        if num == 1:
            shareUuid = shareUuid1
            activityUrl = f"https://xinrui-isv.isvjcloud.com/school/?share_type=invite&inviter_token={shareUuid}&source=zhuhuichang&sid=3e1fc7c1470b8f70499c018ee2af115w&un_area=15_1213_71706_717"
            print(f"🤖后面的号全部助力: {shareUuid}")

        time.sleep(2)