#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_inviteDraw9.9.py(京喜自营抽奖助力)
Author: HarbourJ
Date: 2024/3/27 00:00
TG: https://t.me/HarbourToulu
cron: 30 0 0,19,22 * * *
new Env('京喜自营抽奖助力');
ActivityEntry: 京东-9.9包邮日-1分钱京喜自营好礼
"""

import time, requests, sys, json, re, threading
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
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
    sys.exit()

# 代理参数默认为本地ip,参数proxyType="";
# 品易代理,参数proxyType="1"; 时长(包月/包日)套餐timeMode改为True,并填写pack参数;流量套餐timeMode为False

proxyType = ""  # 留空默认本地ip，1-品易，2-星空，3-小象，4-携趣，5-51代理，6-代理池
# 这里填写品易代理参数
neek = ""
appkey = ""
timeMode = False  # 时长(包月/包日)套餐改为True;流量套餐为False
pack = ""  # timeMode=True时需要设置pack参数,在提取链接中获取pack
# 这里填写星空代理参数
apikey = ""
signxk = ""
# 这里填写小象代理参数
appKey = ""
appSecret = ""
# 这里填写携趣代理参数
uid = ""
vkey = ""
# 这里填写51代理提取链接
daili51 = ""
# 这里填写代理池地址，如 192.168.31.12:8081
proxyPoolIp = ""
# 并发数量
threadsNum = 1
# 限制最大邀请数量
number_restrictions = 10000

power_success = []
power_failure = []
not_login= []
start = time.time()

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
        localIp = requests.get("https://pycn.yapi.py.cn/get_client_ip").json()["ret_data"]
    except:
        localIp = requests.get("https://ifconfig.me/ip").text
    print(f"获取当前IP:{localIp}")
    # 默认为本地ip，若使用代理请设置参数proxyType="xxx"
    if proxyType == "":
        print('当前使用本地ip,若需使用品易代理,参数proxyType="1";星空代理,参数proxyType="2";小象代理,参数proxyType="3";携趣代理,参数proxyType="4"')
        return None
    elif proxyType == "1":
        print("当前使用品易代理")
        # 自动填写品易IP白名单
        requests.get(f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={localIp}")
        # 根据并发数提取IP数量
        # resp = requests.get(f"http://tiqu.pyhttp.taolop.com/getflowip?count={count}&neek={neek}&type=1&sep=1&sb=&ip_si=1&mr=0")
        if timeMode:
            # 时长套餐
            if not pack:
                print(f"当前时长套餐未设置pack参数,请在提取链接中获取pack参数！")
                sys.exit()
            resp = requests.get(f"http://zltiqu.pyhttp.taolop.com/getpoolip?count={count}&neek={neek}&pack={pack}&type=1&yys=0&port=1&sb=&mr=0&sep=1")
        else:
            # 流量套餐
            resp = requests.get(f"http://zltiqu.pyhttp.taolop.com/getip?count={count}&neek={neek}&type=1&yys=0&port=1&sb=&mr=2&sep=1&username=chukou01&spec=1")
    elif proxyType == "2":
        print("当前使用星空代理,1个ip一个店铺模式")
        resp = requests.get(f"http://api2.xkdaili.com/tools/XApi.ashx?apikey={apikey}&qty={count}&format=txt&split=2&sign={signxk}")
    elif proxyType == "3":
        print("当前使用小象代理")
        resp = requests.get(f"https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=text")
    elif proxyType == "4":
        print("当前使用携趣代理30s有效套餐,1个ip一个店铺模式")
        resp = requests.get(f"http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid={uid}&vkey={vkey}&num={count}&time=30&plat=1&re=0&type=1&so=1&ow=1&spl=1&addr=&db=1")
    elif proxyType == "5":
        time.sleep(1)
        print("当前使用51代理,1个ip一个店铺模式")
        resp = requests.get(daili51)
    elif proxyType == "6":
        print("当前使用代理池工具")
        return [proxyPoolIp] * count
    else:
        print("当前选择代理无效,默认使用本地ip")
        return None

    ip = resp.text
    # print(ip)
    if re.match(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', ip) is None:
        print(ip)
        # exit("IP 不正确")
        return None
    ip = [line.strip() for line in ip.splitlines() if line.strip()]
    ip = [x for x in ip if x]
    # print(ip)

    return ip

def convert_ms_to_hours_minutes(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}h{minutes}m'

def get_h5st_body(ua, cookie, functionId, appId, body):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    clientVersion = ua.split(";")[2]
    body = {
        "appId": appId,
        "appid": "signed_wh5",
        "ua": ua,
        "pin": pt_pin,
        "functionId": functionId,
        "body": body,
        "clientVersion": "1.0.0",
        "client": "wh5",
        "version": "4.4"
    }
    try:
        import base64
        url = "aHR0cDovLzEuOTQuOC4yNDQ6MzAwMi9hcGkvaDVzdA=="
        payload = json.dumps(body)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", base64.b64decode(url.encode('utf-8')).decode('utf-8'), headers=headers, timeout=10, data=payload).json()
        if response['code'] == 200:
            # printf(cookie, f"调用远程h5st4.1接口成功")
            return response['data']
        else:
            printf(cookie, f"调用远程h5st接口失败1")
            return
    except Exception as e:
        printf(cookie, f"调用远程h5st接口失败2:{e}")
        get_h5st_body(ua, cookie, functionId, appId, body)
        return

def H5API(ua, cookie, functionId, body, appId, proxies=None):
    url = "https://api.m.jd.com"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html",
        "Origin": "https://pro.m.jd.com",
        "Cookie": cookie,
        "User-Agent": ua,
        "X-Referer-Page": "https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html",
        "X-Rp-Client": "h5_1.0.0"
    }
    h5stbody = get_h5st_body(ua, cookie, functionId, appId, body)
    if not h5stbody:
        return
    body = h5stbody + f"&uuid=&d_model=0-2-999&osVersion=17.3" # &eid={jsToken['eid']}&x-api-eid-token={jsToken['token']}"
    try:
        response = requests.post(url, headers=headers, data=body, timeout=5, proxies=proxies)
    except Exception as e:
        printf(cookie, f"H5API Error:{str(e)}")
        return
    if response.status_code == 200:
        return response
    else:
        printf(cookie, response.status_code)

def gen_invite(ua, cookie, proxies=None):
    url = "https://api.m.jd.com"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://pro.m.jd.com/mall/active/3SqixAPiuuXFrLo8K6otUHB1oZjU/index.html",
        "Origin": "https://pro.m.jd.com",
        "Cookie": cookie,
        "User-Agent": ua
    }
    body = "functionId=jx_party_invite&appid=signed_wh5&body=%7B%22channel%22%3A%22jkl%22%7D"
    try:
        try:
            response = requests.post(url, headers=headers, data=body, timeout=5, proxies=proxies)
        except Exception as e:
            printf(cookie, f"gen_invite Error1:{str(e)}")
            return
        if response.status_code == 200:
            if "inviteCode" in response.text:
                return response.json()["data"]["result"]["inviteCode"]
            elif "未登录" in response.text:
                printf(cookie, "⚠️车头账号失效！请手动关闭程序！")
            else:
                printf(cookie, "⚠️疑似黑号,获取助力码失败！请手动关闭程序！")
        else:
            printf(cookie, response.status_code)
    except Exception as e:
        printf(cookie, f"gen_invite Error2:{str(e)}")
        return


def genRandomString(i11i1i=32, Iilill="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"):
    II1l11 = len(Iilill)
    llil1I = ""
    for ilIi1i in range(i11i1i):
        llil1I += Iilill[random.randint(0, II1l11 - 1)]
    return llil1I

def Result(ua, cookie, inviter, proxies):
    unpl = genRandomString(300, "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    response = H5API(ua, cookie, "jx_party_assist", {"inviteCode":inviter,"areaInfo":"","unpl":unpl,"qdPageId":"MO-J2011-1","mdClickId":"Babel_dev_other_11lotterystart"}, 'a525b', proxies)
    if not response:
        return
    if int(response.status_code) != int(200):
        printf(cookie, f'接口：{response.status_code}')
        return
    if int(response.json()['code']) == 0:
        if 'result' in response.text:
            msg = '✅助力成功'
            power_success.append(cookie)
        elif response.json()['data']['bizCode'] == -9007:
            msg = '❌火爆...助力失败'
            power_failure.append(cookie)
        elif response.json()['data']['bizCode'] == -9004:
            msg = '❌不能给自己助力呦～'
            power_failure.append(cookie)
        elif response.json()['data']['bizCode'] == -102:
            msg = '💔未登录'
            not_login.append(cookie)
        elif response.json()['data']['bizCode'] == -9010:
            msg = '❌已经助力过了'
            power_failure.append(cookie)
        else:
            msg = response.json()['data']['bizMsg']
            power_failure.append(cookie)
        printf(cookie, f"{response.status_code} 助力结果|{msg}")
    elif int(response.json()['code']) == 405:
        printf(cookie, f"{response.json()['code']}  ❌{response.json()['errMsg']}")
    else:
        printf(cookie, f"{response.json()['code']}  💔{response.json()['errMsg']}")
        not_login.append(cookie)

if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    inviter = remote_redis(f"inviteFission99", 3)
    cookie = cks[0] # 获取车头助力码
    ua = userAgent()
    response = H5API(ua, cookie, "jx_party_assist", {"inviteCode":inviter,"areaInfo":"","unpl":genRandomString(300, "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"),"qdPageId":"MO-J2011-1","mdClickId":"Babel_dev_other_11lotterystart"}, 'a525b')
    if int(response.status_code) != 200:
        printf(cookie, f'接口：{response.status_code}')
        sys.exit()
    if int(response.json()['code']) == 0:
        if 'result' in response.text:
            printf(cookie, f'✅助力作者成功 谢谢你 你是个好人！！！')
        else:
            printf(cookie, f'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')
    else:
        printf(cookie, f"{response.json()['code']}  💔{response.json()['errMsg']}")
    time.sleep(0.1)
    inviteCode = gen_invite(ua, cookie)
    if not inviteCode:
        inviter
    else:
        printf(cookie,f'✅【助力码】:{inviteCode}')
        inviter = inviteCode
    new_cks = list_of_groups(cks, threadsNum)[:]
    for i, cookies in enumerate(new_cks, 1):
        print(f"\n##############并发第{i}组ck##############")
        threads = []
        proxies = get_proxies(threadsNum)
        proxies = proxies if proxies else None
        print(f"****************并发{len(cookies) if cookies else 0}个COOKIE****************")
        for index, cookie in enumerate(cookies, 1):
            cookie = cookie.split(';---')[0] + ';'
            if proxies:
                if "@" in proxies[index-1]:
                    _proxie = {"http": f"http://{proxies[index-1].split('@')[0]}@{proxies[index-1].split('@')[1]}", "https": f"https://{proxies[index-1].split('@')[0]}@{proxies[index-1].split('@')[1]}"}
                else:
                    _proxie = {"http": f"http://{proxies[index - 1].split(':')[0]}:{proxies[index - 1].split(':')[1]}",
                               "https": f"https://{proxies[index - 1].split(':')[0]}:{proxies[index - 1].split(':')[1]}"}
            else:
                _proxie = None
            thead_one = threading.Thread(target=Result, args=(userAgent(), cookie, inviter, _proxie))
            threads.append(thead_one)  # 线程池添加线程
            power_num = len(power_success)
            if power_num >= int(number_restrictions):
                print(f"🎉当前已获取助力{power_num} ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人\n  ⏰耗时:{time.time() - start}, 已达到限制人数,退出程序！")
                sys.exit()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # time.sleep(2)
    print(f'\n\n\n##############清点人数##############\n ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK:{len(not_login)}人\n  ⏰耗时:{time.time() - start}')