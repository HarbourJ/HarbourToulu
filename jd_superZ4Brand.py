#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_superBrandZ.py('特务Z-春天来拉)
Author: HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('特务Z-春天来拉');
ActivityEntry: app首页下拉，做任务抽奖
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

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""

activityId = "1013526"
encryptProjectId = "2bEZS3UewMUyK3icSVhT4MC94eHe"
activityUrl = "https://pro.m.jd.com/mall/active/2SFC2qDsJC9H1K75VAiFbSmaPrk/index.html"
print(f"【🛳活动入口】app首页下拉")

def redis_conn():
    try:
        import redis
        try:
            pool = redis.ConnectionPool(host=redis_url, port=6379, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
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
        print(f"Token error: {str(e)}")
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

def superBrandTaskList(ua, ck):
    url = f"https://api.m.jd.com/?uuid=&client=wh5&area=12_1212_1212_22222&appid=ProductZ4Brand&functionId=superBrandTaskList&t={getJdTime()}&body=%7B%22source%22:%22run%22,%22activityId%22:{activityId},%22assistInfoFlag%22:1%7D"
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://prodev.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'User-Agent': ua,
        'Cookie': ck
    }
    try:
        response = requests.request("POST", url, headers=headers)
        refresh_cookies(response)
        res = response.json()
        if res['code'] == '0' and res['data']['success']:
            taskList = res['data']['result']['taskList']
            return taskList
        else:
            print(res['data']['bizMsg'])
    except Exception as e:
        print('获取活动列表失败')
        print(f"superBrandTaskList Error: {e}")

def superBrandDoTask(ua, ck, activityId, encryptProjectId, itemId, assignmentType, encryptAssignmentId):
    if assignmentType == 5:
        url = f"https://api.m.jd.com/?uuid=&client=wh5&area=12_1212_1212_22222&appid=ProductZ4Brand&functionId=superBrandDoTask&t={getJdTime()}&body=%7B%22source%22:%22run%22,%22activityId%22:{activityId},%22encryptProjectId%22:%22{encryptProjectId}%22,%22encryptAssignmentId%22:%22{encryptAssignmentId}%22,%22assignmentType%22:{assignmentType},%22itemId%22:%22{itemId}%22,%22actionType%22:0,%22dropDownChannel%22:1%7D"
    else:
        url = f"https://api.m.jd.com/?uuid=&client=wh5&area=12_1212_1212_22222&appid=ProductZ4Brand&functionId=superBrandDoTask&t={getJdTime()}&body=%7B%22source%22:%22run%22,%22activityId%22:{activityId},%22encryptProjectId%22:%22{encryptProjectId}%22,%22encryptAssignmentId%22:%22{encryptAssignmentId}%22,%22assignmentType%22:{assignmentType},%22itemId%22:%22{itemId}%22,%22actionType%22:0%7D"
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://prodev.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'User-Agent': ua,
        'Cookie': ck
    }
    response = requests.request("POST", url, headers=headers)
    refresh_cookies(response)
    res = response.json()
    if res['code'] == '0':
        taskList = res['data']['result']
        bizMsg = res['data']['bizMsg']
        return bizMsg, taskList
    else:
        print('任务出错')

def superBrandTaskLottery(ua, ck):
    url = f"https://api.m.jd.com/?uuid=&client=wh5&area=12_1212_1212_22222&appid=ProductZ4Brand&functionId=superBrandTaskLottery&t={getJdTime()}&body=%7B%22source%22:%22run%22,%22activityId%22:{activityId}%7D"
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://prodev.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'User-Agent': ua,
        'Cookie': ck
    }
    response = requests.request("POST", url, headers=headers)
    refresh_cookies(response)
    res = response.json()
    if res['code'] == '0':
        result = res['data']['result']
        bizMsg = res['data']['bizMsg']
        return bizMsg, result
    else:
        print('任务出错')

def bindWithVender(ua, cookie, venderId):
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
            return res['message'], res['result']['giftInfo'] if res['result'] else ""
    except Exception as e:
        print(f"bindWithVender Error: {venderId} {e}")

def getShopOpenCardInfo(ua, cookie, venderId):
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
        response = requests.get(url=url, headers=headers, timeout=10).text
        res = json.loads(response)
        if res['success']:
            venderCardName = res['result']['shopMemberCardInfo']['venderCardName']
            return venderCardName
        else:
            return venderId
    except:
        return venderId


if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    global needHelpList, shareUuid
    try:
        shareUuid = remote_redis(f"super_{activityId}", 1)
    except:
        shareUuid = ""
    needHelpList = []
    num = 0
    for cookie in cks:
        num += 1
        if num % 10 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(3)
        global ua
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        taskList = superBrandTaskList(ua, cookie)
        if not taskList:
            time.sleep(1)
            continue
        print(f"共计{len(taskList)}个任务")
        if not taskList:
            time.sleep(1.5)
            continue
        for oneTask in taskList:
            encryptAssignmentId = oneTask['encryptAssignmentId']
            assignmentType = oneTask['assignmentType']
            if oneTask['completionFlag']:
                print(f"任务：{oneTask['assignmentName']}，已完成")
            else:
                if "抽奖" in oneTask['assignmentName'] or "攒一攒" in oneTask['assignmentName'] or "抽奖" in oneTask['assignmentName']:
                    continue
                print(f"去做任务：{oneTask['assignmentName']},共计{oneTask['assignmentTimesLimit']}个子任务,已完成{oneTask['completionCnt']}个")
                if assignmentType == 3:
                    # 关注店铺
                    followShopInfo = oneTask['ext']['followShop']
                    for i in followShopInfo:
                        comments = i['comments']
                        comments = comments[0] if comments else oneTask['assignmentName']
                        itemId = i['itemId']
                        status = i['status']
                        if status == 1:
                            print(f"\t去做{comments}任务")
                            doTaskInfo = superBrandDoTask(ua, cookie, activityId, encryptProjectId, itemId, assignmentType, encryptAssignmentId)
                            if doTaskInfo:
                                print(f"\t\t{doTaskInfo[0]},获得{doTaskInfo[1]['quantity']}春意值")
                        time.sleep(0.3)
                elif assignmentType == 7:
                    # 开卡
                    brandMemberList = oneTask['ext']['brandMemberList']
                    for i in brandMemberList:
                        comments = i['title']
                        itemId = i['itemId']
                        vendorIds = i['vendorIds']
                        status = i['status']
                        if status == 1:
                            print(f"\t去做{comments}任务")
                            venderCardName = getShopOpenCardInfo(ua, cookie, vendorIds)
                            open_result = bindWithVender(ua, cookie, vendorIds)
                            if open_result is not None:
                                if "火爆" in open_result[0] or "失败" in open_result[0] or "解绑" in open_result[0]:
                                    print(f"\t\t⛈{open_result[0]}")
                                    continue
                                if "加入店铺会员成功" in open_result[0]:
                                    print(f"\t\t🎉🎉{venderCardName} {open_result[0]}")
                                    if open_result[1]:
                                        print(f"\t\t🎁获得{','.join([gift['discountString'] + gift['prizeName'] for gift in open_result[1]['giftList']])}")
                            doTaskInfo = superBrandDoTask(ua, cookie, activityId, encryptProjectId, itemId, assignmentType, encryptAssignmentId)
                            if doTaskInfo:
                                print(f"\t\t{doTaskInfo[0]},获得{doTaskInfo[1]['quantity']}春意值")
                        time.sleep(0.3)
                elif assignmentType == 5:
                    # 下拉
                    sign2 = oneTask['ext']['sign2']
                    assignmentDesc = oneTask['assignmentDesc']
                    for i in sign2:
                        itemId = i['itemId']
                        status = i['status']
                        if status == 1:
                            print(f"\t去做{assignmentDesc}任务")
                            doTaskInfo = superBrandDoTask(ua, cookie, activityId, encryptProjectId, itemId, assignmentType, encryptAssignmentId)
                            if doTaskInfo:
                                print(f"\t\t{doTaskInfo[0]},获得{doTaskInfo[1]['quantity']}春意值")
                        elif status == 1:
                            print(f"未到任务时间")
                        time.sleep(0.3)
                elif assignmentType == 1:
                    # 浏览
                    shoppingActivity = oneTask['ext']['shoppingActivity']
                    waitDuration = oneTask['ext']['waitDuration']
                    for i in shoppingActivity:
                        itemId = i['itemId']
                        status = i['status']
                        if status == 1:
                            title = i['title']
                            itemId = i['itemId']
                            status = i['status']
                            print(f"\t去做{title}任务")
                            doTaskInfo = superBrandDoTask(ua, cookie, activityId, encryptProjectId, itemId, assignmentType, encryptAssignmentId)
                            if doTaskInfo:
                                print(f"\t\t{doTaskInfo[0]},获得{doTaskInfo[1]['quantity']}春意值")
                        time.sleep(0.3)
                elif assignmentType == 2:
                    # 邀好友助力
                    assistTaskDetail = oneTask['ext']['assistTaskDetail']
                    assignmentName = oneTask['assignmentName']
                    inviteUuid = assistTaskDetail['itemId']
                    print(f"\t去做{assignmentName}任务,助力{shareUuid}")
                    doTaskInfo = superBrandDoTask(ua, cookie, activityId, encryptProjectId, shareUuid, assignmentType, encryptAssignmentId)
                    if doTaskInfo:
                        print(f"\t\t{doTaskInfo[0]},获得{doTaskInfo[1]['quantity']}春意值")
                    if num == 1:
                        shareUuid = inviteUuid
                        print(f"后面全部助力{inviteUuid}")
                    time.sleep(0.3)
            time.sleep(0.5)
        print("现在去抽奖")
        while True:
            lottery_result = superBrandTaskLottery(ua, cookie)
            if lottery_result:
                bizMsg = lottery_result[0]
                result = lottery_result[1]
                if "积分不足" in bizMsg:
                    print('\t积分不足,退出')
                    break
                if "任务已完成" in bizMsg:
                    print('\t已达到抽奖上限,退出')
                    break
                rewards = result['rewards']
                if rewards:
                    rewardsList = [f"{i['quantity']}{i['awardName']}" for i in rewards]
                    print(f"\t🎉抽奖获得{' '.join(rewardsList)}")
            else:
                print(f"\t😭抽奖获得💨💨💨")
            time.sleep(0.2)

        time.sleep(1.5)
