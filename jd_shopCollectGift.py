#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_shopCollectGift.py(店铺会员礼包-监控脚本)
Author: HarbourJ
Date: 2022/9/2 12:00
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourSailing
cron: 1 1 1 1 1 1
new Env('店铺会员礼包-JK');
ActivityEntry: https://shop.m.jd.com/shop/home?shopId=1000003443
Description: 部分账号开卡后无法自动领取开卡奖励,不自动开卡,仅领取已开卡的会员礼包
             变量export jd_shopCollectGiftId="1000003443" 变量为店铺venderId
"""

import requests ,sys ,os ,re ,time #line:1
from datetime import datetime #line:2
from functools import partial #line:3
print =partial (print ,flush =True )#line:4
import warnings #line:5
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:6
from urllib .parse import quote_plus ,unquote_plus #line:7
try :#line:8
    from jd_sign import *#line:9
except ImportError as e :#line:10
    print (e )#line:11
    if "No module"in str (e ):#line:12
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:13
    sys .exit ()#line:14
try :#line:15
    from jdCookie import get_cookies #line:16
    getCk =get_cookies ()#line:17
except :#line:18
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:19
    sys .exit (3 )#line:20
venderId =os .environ .get ("jd_shopCollectGiftId")if os .environ .get ("jd_shopCollectGiftId")else ""#line:22
if not venderId :#line:24
    print ("⚠️未发现有效活动变量,退出程序!")#line:25
    sys .exit ()#line:26
def collectGift (O0O0O000O0O0O000O ,OO0OOOOO0OOO0OO00 ,OOOOOOOOO00000000 ,O0O0O0O0O0O000OO0 ):#line:28
    O0O0000O0O00OO0O0 =f"https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=collectGift&body=%7B%22venderId%22%3A%22{O0O0O000O0O0O000O}%22%2C%22activityId%22%3A{OO0OOOOO0OOO0OO00}%2C%22activityType%22%3A{OOOOOOOOO00000000}%7D&clientVersion=9.2.0&client=H5&uuid=88888"#line:29
    O0OOOO00O0OO0O00O ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':O0O0O0O0O0O000OO0 ,'User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate, br'}#line:39
    O0OO0OO0O000O000O =requests .request ("GET",O0O0000O0O00OO0O0 ,headers =O0OOOO00O0OO0O00O )#line:40
    O0O00OO00000OOOO0 =O0OO0OO0O000O000O .json ()#line:41
    if O0O00OO00000OOOO0 ['success']:#line:42
        return O0O00OO00000OOOO0 ['message']#line:43
    else :#line:44
        print (O0O00OO00000OOOO0 )#line:45
def getFansDetail (OO000O0OO0O00O0OO ,OOO000000O0000O00 ):#line:47
    OO0O0O00O00000O0O =f"https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getFansFuseMemberDetail&clientVersion=9.2.0&client=H5&uuid=88888&body=%7B%22venderId%22%3A%22{OO000O0OO0O00O0OO}%22%2C%22channel%22%3A406%2C%22queryVersion%22%3A%2210.5.2%22%7D"#line:48
    O0O0OO0OO00O0OO0O ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OOO000000O0000O00 ,'User-Agent':ua ,'Accept-Language':'zh-CN,zh-Hans;q=0.9','Referer':'https://shopmember.m.jd.com/','Accept-Encoding':'gzip, deflate, br'}#line:58
    OO0O000OOO0O00000 =requests .request ("GET",OO0O0O00O00000O0O ,headers =O0O0OO0OO00O0OO0O )#line:59
    O00O00O0OO0OOO000 =OO0O000OOO0O00000 .json ()#line:60
    if O00O00O0OO0OOO000 ['success']:#line:61
        O0OO00OOOOO0O0O0O =O00O00O0OO0OOO000 ['data'][0 ]['cardInfo']['brandName']#line:62
        if 'newGiftList'in str (O00O00O0OO0OOO000 )and O00O00O0OO0OOO000 ['data'][0 ]['newGiftList']:#line:63
            O0000OO0O00OOO0OO =O00O00O0OO0OOO000 ['data'][0 ]['newGiftList'][0 ]['activityId']#line:64
            OO000OO00O0O00OO0 =O00O00O0OO0OOO000 ['data'][0 ]['newGiftList'][0 ]['activityType']#line:65
            OO000OO0O0OOO0000 =O00O00O0OO0OOO000 ['data'][0 ]['newGiftList'][0 ]['prizeTypeName']#line:66
            OOOO0O0O0O0000O00 =O00O00O0OO0OOO000 ['data'][0 ]['newGiftList'][0 ]['discount']#line:67
            return O0000OO0O00OOO0OO ,OO000OO00O0O00OO0 ,OOOO0O0O0O0000O00 ,OO000OO0O0OOO0000 ,O0OO00OOOOO0O0O0O #line:68
        else :#line:69
            print (f"{O0OO00OOOOO0O0O0O} 未发现店铺礼包💨")#line:70
if __name__ =='__main__':#line:72
    try :#line:73
        cks =getCk #line:74
        if not cks :#line:75
            sys .exit ()#line:76
    except :#line:77
        print ("未获取到有效COOKIE,退出程序！")#line:78
        sys .exit ()#line:79
    num =0 #line:80
    for cookie in cks [:]:#line:81
        num +=1 #line:82
        global ua #line:83
        ua =userAgent ()#line:84
        try :#line:85
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:86
            pt_pin =unquote_plus (pt_pin )#line:87
        except IndexError :#line:88
            pt_pin =f'用户{num}'#line:89
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:90
        print (datetime .now ())#line:91
        try :#line:93
            getFD =getFansDetail (venderId ,cookie )#line:94
            if getFD :#line:95
                activityId =getFD [0 ]#line:96
                activityType =getFD [1 ]#line:97
                discount =getFD [2 ]#line:98
                prizeTypeName =getFD [3 ]#line:99
                brandName =getFD [4 ]#line:100
                cg =collectGift (venderId ,activityId ,activityType ,cookie )#line:101
                if cg :#line:102
                    if "领取成功"in cg :#line:103
                        print (f"🎉🎉🎉{brandName} {discount}{prizeTypeName} {cg}")#line:104
                    else :#line:105
                        print (brandName ,cg )#line:106
        except :#line:107
            continue #line:108
        time .sleep (0.5 )