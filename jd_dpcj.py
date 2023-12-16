#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_dpcj.py(店铺抽奖-JK)
Author: HarbourJ
Date: 2022/10/15 23:00
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('店铺抽奖-JK');
ActivityEntry：https://shop.m.jd.com/shop/lottery?shopId=xxxxx&venderId=xxxxx
Description: 变量：export DPCJID="shopId1&shopId2" #变量为店铺🆔
"""

import requests ,time ,re ,os ,sys ,json #line:1
from datetime import datetime #line:2
from sendNotify import *#line:3
from urllib .parse import quote_plus ,unquote_plus #line:4
import warnings #line:5
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:6
from functools import partial #line:7
print =partial (print ,flush =True )#line:8
try :#line:9
    from jd_sign import *#line:10
except ImportError as e :#line:11
    print (e )#line:12
    if "No module"in str (e ):#line:13
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:14
    sys .exit ()#line:15
try :#line:16
    from jdCookie import get_cookies #line:17
    getCk =get_cookies ()#line:18
except :#line:19
    print ("请先下载依赖脚本，\n下载链接：https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:20
    sys .exit (3 )#line:21
dpcj =os .environ .get ("DPCJID")if os .environ .get ("DPCJID")else ""#line:23
if not dpcj :#line:25
    print ("⚠️未发现有效店铺签到活动变量DPCJID,退出程序!")#line:26
    sys .exit ()#line:27
def check (OO000OO0000OO0OOO ,OO0O0OO0O0O00O000 ):#line:29
    try :#line:30
        O0OO0O00OO0OOOO0O ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:31
        O00000O00OOO0000O ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OO0O0OO0O0O00O000 ,"User-Agent":OO000OO0000OO0OOO ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:41
        O0O0000OOOOO0OOO0 =requests .get (url =O0OO0O00OO0OOOO0O ,headers =O00000O00OOO0000O ,timeout =None ).text #line:42
        OO0OO00O0O0O0000O =json .loads (O0O0000OOOOO0OOO0 )#line:43
        if OO0OO00O0O0O0000O ['retcode']=='1001':#line:44
            O00OO0OO000O00000 ="⚠️当前ck已失效，请检查"#line:45
            return {'code':1001 ,'data':O00OO0OO000O00000 }#line:46
        elif OO0OO00O0O0O0000O ['retcode']=='0'and 'userInfo'in OO0OO00O0O0O0000O ['data']:#line:47
            O0OO0OOO0000OO0OO =OO0OO00O0O0O0000O ['data']['userInfo']['baseInfo']['nickname']#line:48
            return {'code':200 ,'name':O0OO0OOO0000OO0OO ,'ck':OO0O0OO0O0O00O000 }#line:49
    except Exception as O000O0OOO0O000OOO :#line:50
        return {'code':0 ,'data':O000O0OOO0O000OOO }#line:51
def get_time ():#line:53
    OO0OOOOOO0000000O =round (time .time ()*1000 )#line:54
    return OO0OOOOOO0000000O #line:55
def getSignInfo (O0O000000OO0O0O00 ,O00OO0O000O0O00OO ,OO0000O000OO0O000 ,OO0000OO00OO00O00 ):#line:57
    OOO0O0O00000O0OO0 =f"https://api.m.jd.com/client.action?functionId=whx_getSignInfo&body=%7B%22shopId%22%3A%22{OO0000O000OO0O000}%22%2C%22venderId%22%3A%22{OO0000OO00OO00O00}%22%2C%22source%22%3A%22m-shop%22%7D&t=1665848303470&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_88_2888_8&uuid=16587341419872043913507"#line:58
    O0O00OOO00O0O0OO0 ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','cookie':O00OO0O000O0O00OO ,'origin':'https://shop.m.jd.com','referer':'https://shop.m.jd.com/','user-agent':O0O000000OO0O0O00 }#line:67
    OOOOOO000OO0OOO0O =requests .request ("GET",OOO0O0O00000O0OO0 ,headers =O0O00OOO00O0O0OO0 )#line:68
    OO000O0OO0O00OO00 =OOOOOO000OO0OOO0O .json ()#line:69
    return OO000O0OO0O00OO00 #line:70
def sign (OOOOOO0OO00OOOO0O ,OO0O0OOOO00O00000 ,O00O0O00OO0O00OO0 ,OO0O0OOO000OO0O0O ):#line:72
    O0O000OO0OOO0O00O =f"https://api.m.jd.com/client.action?functionId=whx_sign&body=%7B%22shopId%22%3A%22{O00O0O00OO0O00OO0}%22%2C%22venderId%22%3A%22{OO0O0OOO000OO0O0O}%22%2C%22source%22%3A%22m-shop%22%7D&t=1665847166130&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_88_2888_8&uuid=16587341419872043913507"#line:73
    OOO0O0OO0OO00O0O0 ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','cookie':OO0O0OOOO00O00000 ,'origin':'https://shop.m.jd.com','referer':'https://shop.m.jd.com/','user-agent':OOOOOO0OO00OOOO0O }#line:82
    O0O0OOO0OOO0O0OO0 =requests .request ("GET",O0O000OO0OOO0O00O ,headers =OOO0O0OO0OO00O0O0 )#line:83
    OO0OO0OOO00OO000O =O0O0OOO0OOO0O0OO0 .json ()#line:84
    return OO0OO0OOO00OO000O #line:85
def get_venderId (O00OOO0OO00O0O00O ,O0000OOO00O0O0OO0 ,O0OOOOO0OO00O00O0 ):#line:87
    O00000OO0OO00O0O0 =f'https://api.m.jd.com/client.action?functionId=whx_getMShopOutlineInfo&body=%7B%22shopId%22%3A%22{O0OOOOO0OO00O00O0}%22%2C%22source%22%3A%22m-shop%22%7D&appid=shop_view&clientVersion=11.0.0&client=wh5'#line:88
    O000OOOO0O0000O00 ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','origin':'https://shop.m.jd.com','referer':'https://shop.m.jd.com/','user-agent':O00OOO0OO00O0O00O ,'cookie':O0000OOO00O0O0OO0 }#line:97
    OOO00O0000OOO0OO0 =requests .request ("GET",O00000OO0OO00O0O0 ,headers =O000OOOO0O0000O00 )#line:98
    O00OO0O000OOO00O0 =OOO00O0000OOO0OO0 .json ()#line:99
    try :#line:100
        if O00OO0O000OOO00O0 ['success']:#line:101
            O00000000O0O0OO00 =O00OO0O000OOO00O0 ['data']['shopInfo']['venderId']#line:102
            return O00000000O0O0OO00 #line:103
        else :#line:104
            return O0OOOOO0OO00O00O0 #line:105
    except :#line:106
        return #line:107
if __name__ =="__main__":#line:110
    global msg #line:111
    msg =''#line:112
    shopIds =dpcj .split ('&')#line:113
    print (f"✅成功获取{len(shopIds)}个DPCJ🆔变量")#line:114
    try :#line:115
        cks =getCk #line:116
        if not cks :#line:117
            sys .exit ()#line:118
    except :#line:119
        print ("未获取到有效COOKIE,退出程序！")#line:120
        sys .exit ()#line:121
    num =0 #line:122
    for cookie in cks :#line:123
        num +=1 #line:124
        if num %9 ==0 :#line:125
            print ("⏰等待3s,休息一下")#line:126
            time .sleep (3 )#line:127
        ua =userAgent ()#line:128
        try :#line:129
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:130
            pt_pin =unquote_plus (pt_pin )#line:131
        except IndexError :#line:132
            pt_pin =f'用户{num}'#line:133
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:134
        print (datetime .now ())#line:135
        result =check (ua ,cookie )#line:137
        if result ['code']!=200 :#line:138
            print (f"‼️{result['data']}")#line:139
            continue #line:140
        signRewards =[]#line:141
        for shopId in shopIds :#line:142
            try :#line:143
                print (f"{shopId}")#line:144
                venderId =get_venderId (ua ,cookie ,shopId )#line:145
                time .sleep (0.2 )#line:146
                if not venderId :#line:147
                    continue #line:148
                signInfo =getSignInfo (ua ,cookie ,shopId ,venderId )#line:149
                time .sleep (0.2 )#line:150
                if signInfo ['isSuccess']:#line:151
                    try :#line:152
                        signInfo_ =signInfo ['result']['result']['signInfo']#line:153
                    except :#line:154
                        print (f"\t⛈店铺抽奖已过期")#line:155
                        continue #line:156
                    if signInfo_ ['isSign']==2 :#line:157
                        print (f"\t⛈店铺已抽奖")#line:158
                    else :#line:159
                        toSign =sign (ua ,cookie ,shopId ,venderId )#line:160
                        if toSign ['isSuccess']and 'isWin'in str (toSign ):#line:161
                            if toSign ['result']['result']['isWin']:#line:162
                                signReward =toSign ['result']['result']['signReward']['name']#line:163
                                print (f"\t🎉{signReward}")#line:164
                                if "东券"in signReward or "购原价"in signReward :#line:165
                                    continue #line:166
                                signRewards .append (signReward )#line:167
                            else :#line:168
                                print ("\t💨💨💨")#line:169
                        else :#line:170
                            print ("\t💨💨💨")#line:171
            except Exception as e :#line:172
                print (e )#line:173
                time .sleep (1 )#line:174
                continue #line:175
        if signRewards :#line:176
            price =','.join (signRewards )#line:177
            msg +=f'【账号{num}】{pt_pin} 🎉{price}\n'#line:178
        time .sleep (0.5 )#line:180
    title ="🗣消息提醒：店铺抽奖-JK"#line:182
    msg =f"⏰{str(datetime.now())[:19]}\n"+msg #line:183
    send (title ,msg )