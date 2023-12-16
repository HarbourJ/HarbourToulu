#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_shopFollowGift.py(关注有礼-JK)
Author: tttccz,HarbourJ
Date: 2022/8/8 19:52
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('关注有礼-JK');
ActivityEntry: https://shop.m.jd.com/?shopId=12342136
               变量 export jd_shopFollowGiftId="店铺shopId1&店铺shopId2" #变量为店铺🆔,建议一次仅运行2-3个shopId
                   export jd_shopFollowGiftRunNums=xx #变量为需要运行账号数量,默认跑前10个账号
"""

import time ,requests ,sys ,re ,os ,json ,random #line:1
from datetime import datetime #line:2
from urllib .parse import quote_plus ,unquote_plus #line:3
from sendNotify import *#line:4
from functools import partial #line:5
print =partial (print ,flush =True )#line:6
import warnings #line:7
warnings .filterwarnings ("ignore",category =DeprecationWarning )#line:8
try :#line:10
    from jd_sign import *#line:11
except ImportError as e :#line:12
    print (e )#line:13
    if "No module"in str (e ):#line:14
        print ("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")#line:15
    sys .exit ()#line:16
try :#line:17
    from jdCookie import get_cookies #line:18
    getCk =get_cookies ()#line:19
except :#line:20
    print ("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")#line:21
    sys .exit (3 )#line:22
redis_url =os .environ .get ("redis_url")if os .environ .get ("redis_url")else "172.17.0.1"#line:24
redis_pwd =os .environ .get ("redis_pwd")if os .environ .get ("redis_pwd")else ""#line:25
jd_shopFollowGiftId =os .environ .get ("jd_shopFollowGiftId")if os .environ .get ("jd_shopFollowGiftId")else ""#line:26
runNums =os .environ .get ("jd_shopFollowGiftRunNums")if os .environ .get ("jd_shopFollowGiftRunNums")else 10 #line:27
if not jd_shopFollowGiftId :#line:29
    print ("⚠️未发现有效活动变量jd_shopFollowGiftId,退出程序!")#line:30
    sys .exit ()#line:31
runNums =int (runNums )#line:33
if runNums ==10 :#line:34
    print ('🤖本次关注默认跑前10个账号,设置自定义变量:export jd_shopFollowGiftRunNums="需要运行加购的ck数量"')#line:35
else :#line:36
    print (f'🤖本次运行前{runNums}个账号')#line:37
def getJdTime ():#line:39
    O000O00O0000OO00O =int (round (time .time ()*1000 ))#line:40
    return O000O00O0000OO00O #line:41
def randomString (OO0O0O0OO00O0OOOO ,flag =False ):#line:43
    O00000OO00O00OO0O ="0123456789abcdef"#line:44
    if flag :O00000OO00O00OO0O =O00000OO00O00OO0O .upper ()#line:45
    O000OOO00OOO000OO =[random .choice (O00000OO00O00OO0O )for _OO0O0OOOO00000O0O in range (OO0O0O0OO00O0OOOO )]#line:46
    return ''.join (O000OOO00OOO000OO )#line:47
def check (O000000O0O0O0O000 ,OO0O0O0O0OOOOO00O ):#line:49
    try :#line:50
        OO00O0OOO000O00OO ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:51
        OO000OOOOO0O0OO0O ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OO0O0O0O0OOOOO00O ,"User-Agent":O000000O0O0O0O000 ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:61
        OO0O0OO0OO000O0O0 =requests .get (url =OO00O0OOO000O00OO ,headers =OO000OOOOO0O0OO0O ,timeout =None ).text #line:62
        O00OOO0000O00O000 =json .loads (OO0O0OO0OO000O0O0 )#line:63
        if O00OOO0000O00O000 ['retcode']=='1001':#line:64
            return {'code':1001 ,'data':'⚠️当前ck已失效，请检查'}#line:65
        elif O00OOO0000O00O000 ['retcode']=='0'and 'userInfo'in O00OOO0000O00O000 ['data']:#line:66
            O000OO0O00OOO00O0 =O00OOO0000O00O000 ['data']['userInfo']['baseInfo']['nickname']#line:67
            return {'code':200 ,'name':O000OO0O00OOO00O0 ,'ck':OO0O0O0O0OOOOO00O }#line:68
    except Exception as OO0OO0OOO000OOOOO :#line:69
        return {'code':0 ,'data':OO0OO0OOO000OOOOO }#line:70
def get_venderId (O0O00O000O0OOOO0O ,O000OO0OO0O000000 ):#line:72
    OOO00OOOO00OO000O =f'https://api.m.jd.com/client.action?functionId=whx_getMShopOutlineInfo&body=%7B%22shopId%22%3A%22{O000OO0OO0O000000}%22%2C%22source%22%3A%22m-shop%22%7D&appid=shop_view&clientVersion=11.0.0&client=wh5'#line:73
    OO0O0OOOOOOO00000 ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','origin':'https://shop.m.jd.com','referer':'https://shop.m.jd.com/','user-agent':ua ,'cookie':cookie }#line:82
    O000000O00OOO000O =requests .request ("GET",OOO00OOOO00OO000O ,headers =OO0O0OOOOOOO00000 )#line:83
    OOOOOO00OOOO0000O =O000000O00OOO000O .json ()#line:84
    if OOOOOO00OOOO0000O ['success']:#line:85
        OO0O000OOO00000O0 =OOOOOO00OOOO0000O ['data']['shopInfo']['venderId']#line:86
        O0O00000OO0OO0O00 =OOOOOO00OOOO0000O ['data']['shopInfo']['shopName']if OOOOOO00OOOO0000O ['data']['shopInfo']['shopName']else ""#line:87
        print (f'【店铺{O0O00O000O0OOOO0O}】{O0O00000OO0OO0O00}')#line:88
        return O0O00000OO0OO0O00 ,OO0O000OOO00000O0 #line:89
    else :#line:90
        print (f'获取店铺信息失败！')#line:91
        return None ,None #line:92
def getShopHomeActivityInfo (O0O0000O0OOOOOOO0 ,OO0O0OOOO0O000OOO ,OO0OO000OO0O0OOOO ):#line:94
    global MSG #line:95
    OO0OOO0OOO0OOO0O0 ={"shopId":O0O0000O0OOOOOOO0 ,"source":"app-shop","latWs":"0","lngWs":"0","displayWidth":"1170.000000","sourceRpc":"shop_app_home_home","lng":"0","lat":"0","venderId":OO0O0OOOO0O000OOO }#line:106
    s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OO0OO000OO0O0OOOO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:117
    sign (OO0OOO0OOO0OOO0O0 ,'getShopHomeActivityInfo')#line:118
    OOO000O000OOOO0O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:119
    if OOO000O000OOOO0O0 .status_code !=200 :#line:120
        print (OOO000O000OOOO0O0 .status_code )#line:121
        MSG +=f" ⛈{OOO000O000OOOO0O0.status_code}"#line:122
        return #line:123
    else :#line:124
        if "参数异常"in OOO000O000OOOO0O0 .text :#line:125
            return #line:126
    O000OO00O0000O0OO =OOO000O000OOOO0O0 .json ()#line:127
    if O000OO00O0000O0OO ['isSuccess']and O000OO00O0000O0OO ["code"]=='0':#line:128
        if O000OO00O0000O0OO ["result"]["followed"]:#line:129
            print ("\t🤖已关注过店铺")#line:130
            return #line:131
        else :#line:132
            if 'shopGifts'in str (O000OO00O0000O0OO ):#line:133
                O00O0000000O0000O =O000OO00O0000O0OO ['result']['shopGifts']#line:134
                for OO000O000OOOOOOOO in O00O0000000O0000O :#line:135
                    OOOOOOOO0O00OO00O =OO000O000OOOOOOOO ['redWord']#line:136
                    OOOOO00OOO0O0O0O0 =OO000O000OOOOOOOO ['rearWord']#line:137
                    print (f'\t🎁关注有礼奖励：{OOOOOOOO0O00OO00O}{OOOOO00OOO0O0O0O0}')#line:138
                    if OOOOO00OOO0O0O0O0 .find ('京豆')>-1 :#line:139
                        return O000OO00O0000O0OO ['result']['activityId']#line:140
            else :#line:141
                print ('\t⛈未发现关注有礼活动')#line:142
                return #line:143
    else :#line:144
        print ('⛈获取活动信息失败！')#line:145
        return #line:146
def drawShopGift (OO00OO0O00OOOO0O0 ,OO00OOOOO00OOO000 ,OOOO0OO00O00O0000 ,OO000O0OO000O0OO0 ):#line:148
    OOO0000OO0000000O ={"shopId":OO00OO0O00OOOO0O0 ,"source":"app-shop","latWs":"0","lngWs":"0","displayWidth":"1170.000000","sourceRpc":"shop_app_home_home","lng":"0","lat":"0","venderId":OO00OOOOO00OOO000 ,"activityId":OO000O0OO000O0OO0 }#line:160
    s .headers ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'','Cookie':OOOO0OO00O00O0000 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:171
    O0OO000OOO0O00OOO =sign (OOO0000OO0000000O ,'drawShopGift')#line:172
    O00OOO00OOO0000O0 =s .post ('https://api.m.jd.com/client.action',verify =False ,timeout =30 )#line:173
    if O00OOO00OOO0000O0 .status_code !=200 :#line:174
        print (O00OOO00OOO0000O0 .status_code )#line:175
        return #line:176
    else :#line:177
        if "参数异常"in O00OOO00OOO0000O0 .text :#line:178
            return #line:179
    return O00OOO00OOO0000O0 .json ()#line:180
if __name__ =='__main__':#line:182
    global MSG #line:183
    MSG =''#line:184
    title ="🗣消息提醒：关注有礼-JK"#line:185
    shopIds =jd_shopFollowGiftId .split ('&')#line:186
    print (f"✅成功获取{len(shopIds)}个jd_shopFollowGift🆔变量")#line:187
    try :#line:188
        cks =getCk #line:189
        if not cks :#line:190
            sys .exit ()#line:191
    except :#line:192
        print ("未获取到有效COOKIE,退出程序！")#line:193
        sys .exit ()#line:194
    num =0 #line:195
    for cookie in cks [:runNums ]:#line:196
        num +=1 #line:197
        if num %10 ==0 :#line:198
            print ("⏰等待3s,休息一下")#line:199
            time .sleep (3 )#line:200
        global ua #line:201
        ua =userAgent ()#line:202
        try :#line:203
            pt_pin =re .compile (r'pt_pin=(.*?);').findall (cookie )[0 ]#line:204
            pt_pin =unquote_plus (pt_pin )#line:205
        except IndexError :#line:206
            pt_pin =f'用户{num}'#line:207
        print (f'\n******开始【京东账号{num}】{pt_pin} *********\n')#line:208
        MSG +=f"【账号{num}】{pt_pin}"#line:209
        print (datetime .now ())#line:210
        result =check (ua ,cookie )#line:212
        if result ['code']!=200 :#line:213
            print (f"‼️{result['data']}")#line:214
            MSG +=f" ⚠️当前ck已失效\n"#line:215
            time .sleep (1 )#line:216
            continue #line:217
        MSG1 =''#line:219
        for index ,shopId in enumerate (shopIds ,1 ):#line:220
            shopInfo =get_venderId (index ,shopId )#line:221
            shopName =shopInfo [0 ]#line:222
            venderId =shopInfo [1 ]#line:223
            if venderId :#line:224
                activityId =getShopHomeActivityInfo (shopId ,venderId ,cookie )#line:225
                time .sleep (0.5 )#line:226
                if activityId :#line:227
                    drawResult =drawShopGift (shopId ,venderId ,cookie ,activityId )#line:228
                    if drawResult :#line:229
                        if drawResult ['isSuccess']and drawResult ['code']=='0':#line:230
                            drawResultDesc =drawResult ['result']['followDesc']#line:231
                            if '关注成功'in str (drawResultDesc ):#line:232
                                drawResultTotal =''#line:233
                                drawResultPrizes =drawResult ['result']['alreadyReceivedGifts']#line:234
                                for drawResultPrize in drawResultPrizes :#line:235
                                    drawResultTotal +=str (drawResultPrize ['redWord'])+drawResultPrize ['rearWord']+''#line:236
                                print (f"\t🎉🎉🎉成功领取 {drawResultTotal}")#line:237
                                MSG1 +=f"\n    🎉【{shopName}】{drawResultTotal}"#line:238
                            else :#line:239
                                print ('⛈奖励领取失败1！')#line:240
                                MSG1 +=f"\n    ⛈【{shopName}】奖励领取失败1！"#line:241
                        else :#line:242
                            print ('⛈奖励领取失败2！')#line:243
                            MSG1 +=f"\n    ⛈【{shopName}】奖励领取失败2！"#line:244
                    else :#line:245
                        print ('⛈奖励领取失败3！')#line:246
                        MSG1 +=f"\n    ⛈【{shopName}】奖励领取失败3！"#line:247
            time .sleep (0.5 )#line:248
        if not MSG1 :#line:250
            MSG +=" 💨💨💨\n"#line:251
        else :#line:252
            MSG +=MSG1 +"\n"#line:253
        time .sleep (1 )#line:254
    MSG =f"⏰{str(datetime.now())[:19]}\n"+MSG #line:256
    send (title ,MSG )