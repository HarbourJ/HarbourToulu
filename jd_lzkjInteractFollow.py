#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_lzkjInteractFollow.py(jd_lzkjInteract关注有礼)
Author: HarbourJ
Date: 2022/11/24 10:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 *
new Env('jd_lzkjInteract关注有礼');
ActivityEntry: https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType=10053&templateId=20210804190900gzspyl011&activityId=1656581196896083970

Description: 关注xx商品xx豆,自动领奖
"""

import time, requests, sys, re, os, json, random
from datetime import datetime
from urllib.parse import quote_plus, unquote_plus
from functools import partial
from sendNotify import *
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
try:
    from jd_sign import *
except ImportError as e:
    print(e)
    if "No module" in str(e):
        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_sign.py)，安装jd_sign.so依赖")
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

redis_url = os.environ.get("redis_url") if os.environ.get("redis_url") else "172.17.0.1"
redis_port = os.environ.get("redis_port") if os.environ.get("redis_port") else "6379"
redis_pwd = os.environ.get("redis_pwd") if os.environ.get("redis_pwd") else ""
jd_lzkjInteractUrl = os.environ.get("jd_lzkjInteractFollowUrl") if os.environ.get("jd_lzkjInteractFollowUrl") else ""
share_userId = os.environ.get("jd_lzkjInteractUserId") if os.environ.get("jd_lzkjInteractUserId") else ""
runNums = os.environ.get("jd_lzkjInteractFollowRunNums") if os.environ.get("jd_lzkjInteractFollowRunNums") else 12

if "lzkj-isv.isvjcloud.com/prod/cc/interactsaas" not in jd_lzkjInteractUrl:
    print("⛈暂不支持变量设置的活动类型,请检查后重试！仅支持interactsaas类型活动")
    sys.exit()
templateId = re.findall(r"templateId=(.*?)&", jd_lzkjInteractUrl+"&")[0]
activityId = re.findall(r"activityId=(.*?)&", jd_lzkjInteractUrl+"&")[0]
activityType = re.findall(r"activityType=(.*?)&", jd_lzkjInteractUrl+"&")[0]

print(f"【🛳活动入口】https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&templateId={templateId}&activityId={activityId}")

runNums = int(runNums)
if runNums == 12:
    print('🤖本次关注默认跑前12个账号,设置自定义变量:export jd_lzkjInteractAddRunNums="需要运行关注的ck数量"')
else:
    print(f'🤖本次运行前{runNums}个账号')

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

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime

def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def check(ck):
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
        result = requests.get(url=url, headers=header).text
        codestate = json.loads(result)
        if codestate['retcode'] == '1001':
            msg = "当前ck已失效，请检查"
            return {'code': 1001, 'data': msg}
        elif codestate['retcode'] == '0' and 'userInfo' in codestate['data']:
            nickName = codestate['data']['userInfo']['baseInfo']['nickname']
            return {'code': 200, 'name': nickName, 'ck': cookie}
    except Exception as e:
        return {'code': 0, 'data': e}

def getActivity():
    url = activityUrl
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(response.status_code, "⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def followShop(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followShop/follow"
    body = {}
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        return response.json()
    except:
        return False

def getUserInfo(shareUserId):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login"
    body = {
        "status": "1",
        "activityId": activityId,
        "source": "01",
        "tokenPin": token,
        "shareUserId": shareUserId
    }
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': '',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl,
        'Cookie': f'IsvToken={token};'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        res = response.json()
        if res['data']:
            return res['data']
        else:
            print(res)
    else:
        print(f"{response.status_code} ⚠️ip疑似黑了,休息一会再来撸~")
        sys.exit()

def drawPrize(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/drawPrize"
    body = {}
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        res = response.json()
        data = res['data']
        return data
    except:
        return False

def followGoodsAct(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followGoods/getFollowGoods"
    body = {}
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        res = response.json()
        data = res['data']
        return data
    except:
        return False

def followGoods(Token, skuId):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/followGoods/followGoods"
    body = {
        "skuId": skuId,
    }
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        res = response.json()
        if res['resp_code'] == 0:
            if "data" in str(res):
                data = res['data']
                if data['result']:
                    return data
                else:
                    return 99
            else:
                return 99
        else:
            print(f"followGoods Error: {res['resp_msg']}")
    except Exception as e:
        print(f"followGoods Error: {e}")

def getMember(Token, shareUserId):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/getMember"
    body = {
        "shareUserId": shareUserId
    }
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        res = response.json()
        inviteNum = res['data']['shareUser']
        return inviteNum
    except Exception as e:
        print(str(e))
        return False

def prizeList(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/member/prizeList"
    body = {}
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        return response.json()
    except:
        return False

def joinCheck(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/join/check"
    body = {
        "status": "0"
    }
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        return response.json()
    except:
        return False

def getUserId(Token):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/share/getUserId"
    body = {}
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        return response.json()['data']['shareUserId']
    except Exception as e:
        print(str(e))

def receiveAcquire(Token, id):
    url = "https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/prize/receive/acquire"
    body = {
        "prizeInfoId": id,
        "status": 1
    }
    headers = {
        'Host': 'lzkj-isv.isvjcloud.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'token': Token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://lzkj-isv.isvjcloud.com',
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Referer': activityUrl
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        return response.json()['resp_code']
    except:
        print(response.text)
        return False

def bindWithVender(cookie, shopId, venderId):
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
                'shopId': shopId,
                'bindByVerifyCodeFlag': 1
            }, separators=(',', ':'))
        }
        res = s.post('https://api.m.jd.com/', verify=False, timeout=30).json()
        if res['success']:
            return res['message']
    except Exception as e:
        print(e)

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
            response = requests.get(url=url, headers=headers, timeout=10, proxies=proxies).text
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
    global shareUserId, inviteSuccNum, activityUrl, firstCk, MSG
    inviteSuccNum = 0
    shareUserId = ""
    MSG = ''
    title = "🗣消息提醒：lzkjInteract关注有礼"

    activityUrl = f"https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/index?activityType={activityType}&activityId={activityId}&templateId={templateId}&nodeId=101001&prd=null&sid=c77e8b335974724742827d7c42f951cw&un_area=12_1212_11111_22222"

    num = 0
    for cookie in cks[:runNums]:
        num += 1
        if num == 1:
            firstCk = cookie
        if num % 5 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(3)
        global ua, token
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        try:
            result = check(cookie)
            if result['code'] != 200:
                print(f"⚠️当前CK失效！跳过")
                continue
            token = getToken(cookie, r)
            if token is None:
                print(f"⚠️获取Token失败！⏰等待3s")
                time.sleep(2)
                continue
            time.sleep(0.2)
            getActivity()
            time.sleep(0.2)
            userInfo = getUserInfo(shareUserId)
            if not userInfo:
                time.sleep(2)
                continue
            shopId = userInfo['shopId']
            openCardUrl = userInfo['joinInfo']['openCardUrl']
            venderId = re.findall(r"venderId=(\w+)", openCardUrl)
            venderId = venderId[0] if venderId else shopId
            Token = userInfo['token']
            shopName = userInfo['shopName']
            actName = userInfo['actName']
            joinCodeInfo = userInfo['joinInfo']['joinCodeInfo']
            customerId = userInfo['customerId']
            time.sleep(0.2)

            if num == 1:
                print(f"✅ 开启【{actName}】活动")
                print(f"店铺名称：{shopName} {shopId}")
                MSG += f'✅开启{shopName}--{actName}活动\n📝活动地址 {activityUrl.split("&shareUserId=")[0]}\n'

            prize = drawPrize(Token)
            prizeListRecord = []
            prizeNameList = []
            index = 0
            try:
                for prizeitem in prize['prizeInfo']:
                    index += 1
                    print(f"🎁 奖品: {prizeitem['prizeName']}, 剩余：{prizeitem['leftNum']}")
                    prizeNameList.append(f"🎁奖品:{prizeitem['prizeName']},剩余:{prizeitem['leftNum']}\n")
                    if prizeitem['leftNum'] > 0:
                        prizeListRecord.append((prizeitem['prizeName'], prizeitem['id']))
                MSG += f"🎁当前活动奖品如下: \n{str(''.join(prizeNameList))}\n" if num == 1 else ""
            except:
                print('⚠️无法获取奖品列表')

            print(f"参加活动状态：{joinCodeInfo['joinDes']}")
            if "未关注店铺" in joinCodeInfo['joinDes']:
                followShop(Token)
                print(f"关注店铺成功")
                time.sleep(0.2)
            if "不是会员" in joinCodeInfo['joinDes'] or "加入会员" in joinCodeInfo['joinDes']:
                venderCardName = getShopOpenCardInfo(cookie, venderId)
                open_result = bindWithVender(cookie, shopId, venderId)
                if open_result is not None:
                    if "火爆" in open_result or "失败" in open_result or "解绑" in open_result:
                        print(f"⛈{open_result},无法完成关注任务")
                        continue
                    if "加入店铺会员成功" in open_result:
                        print(f"🎉🎉{venderCardName} {open_result}")
        # if "可以参加活动" in joinCodeInfo['joinDes']:  # 1004
            skuInfo = followGoodsAct(Token)
            # print(f"skuInfo: {skuInfo}")
            finishNum = skuInfo[0]['finishNum']
            completeCount = skuInfo[0]['completeCount']
            oneClickFollowPurchase = skuInfo[0]['oneClickFollowPurchase']
            if oneClickFollowPurchase:
                print(f"需要关注{finishNum},已关注{completeCount}")
            else:
                print(f"需要一键关注{finishNum}个商品")
            taskId = skuInfo[0]['taskId']
            skuInfoVO = skuInfo[0]['skuInfoVO']
            skuIds = [i['skuId'] for i in skuInfoVO if not i['status']]
            status = skuInfo[0]['status']
            if completeCount >= finishNum or status:
                print("已经完成过关注任务")
            else:
                needAddCount = finishNum - completeCount
                for x in range(needAddCount):
                    skuId = skuIds[x] if oneClickFollowPurchase else ""
                    followGoodsResult = followGoods(Token, skuId)
                    # print(f"followGoodsResult: {followGoodsResult}")
                    if followGoodsResult == 99:
                        if x == needAddCount - 1:
                            print(f"成功关注{needAddCount}个商品,获得💨💨💨")
                    else:
                        # 1 京豆、4 积分
                        prizeName = followGoodsResult['prizeName']
                        prizeType = followGoodsResult['prizeType']
                        print(f"🎁成功关注{needAddCount}个商品,获得{prizeName}")
                        MSG += f'【账号{num}】{pt_pin} 🎉{prizeName}\n'
                        if "积分" not in prizeName and "京豆" not in prizeName and "优惠券" not in prizeName:
                            print(f"🎉恭喜获得实物,请前往{activityUrl}手动领取奖励！")
                            MSG_ = f'【账号{num}】{pt_pin} 🎉恭喜获得实物,请前往{activityUrl} 手动领取奖励！'
                            msg_ = f"⏰{str(datetime.now())[:19]}\n" + MSG_
                            send(title, msg_)
                    time.sleep(0.1)
        except Exception as e:
            print(e)
        time.sleep(2)

    msg = f"⏰{str(datetime.now())[:19]}\n" + MSG
    send(title, msg)