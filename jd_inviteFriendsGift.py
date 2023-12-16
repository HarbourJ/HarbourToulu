#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: jd_inviteFriendsGift.py(邀好友赢大礼)
Author: Fix by HarbourJ
Date: 2022/7/6 23:26
TG: https://t.me/HarbourToulu
cron: 1 1 1 1 1 1
new Env('邀好友赢大礼');
ActivityEntry：https://prodev.m.jd.com/mall/active/dVF7gQUVKyUcuSsVhuya5d2XD4F/index.html?code=xxxxxxxx&invitePin=xxxxxx
UpdateRecord: 2022.07.06 增加从环境变量中获取authorCode变量，增加对青龙desi JD_COOKIE的适配;
              2022.10.01 修复由于若干接口被更换导致的异常报错
Description: 变量：export jd_inv_authorCode="5f29b7dbcfad44548b685a4d8d151e59"
"""

import requests ,random ,time ,asyncio ,re ,os ,sys ,json #line:1
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
activatyname ='邀请赢大礼'#line:23
activityId ='dVF7gQUVKyUcuSsVhuya5d2XD4F'#line:24
authorCode =os .environ .get ("jd_inv_authorCode")if os .environ .get ("jd_inv_authorCode")else ""#line:26
if not authorCode :#line:28
    print ("⚠️未发现有效活动变量jd_inv_authorCode,退出程序!")#line:29
    sys .exit ()#line:30
async def check (O00O00OOO00OOOO0O ,OOOO0OOO00O00OO0O ):#line:33
    try :#line:34
        O000OO0O000O0O0OO ='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'#line:35
        OOOOOOOOO000OOO0O ={"Host":"me-api.jd.com","Accept":"*/*","Connection":"keep-alive","Cookie":OOOO0OOO00O00OO0O ,"User-Agent":O00O00OOO00OOOO0O ,"Accept-Language":"zh-cn","Referer":"https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&","Accept-Encoding":"gzip, deflate",}#line:45
        O00OO0O00O00O0O00 =requests .get (url =O000OO0O000O0O0OO ,headers =OOOOOOOOO000OOO0O ,timeout =None ).text #line:46
        O0O0OOO0O0O0O000O =json .loads (O00OO0O00O00O0O00 )#line:47
        if O0O0OOO0O0O0O000O ['retcode']=='1001':#line:48
            O0O0000OO0OOO00O0 ="⚠️当前ck已失效，请检查"#line:49
            return {'code':1001 ,'data':O0O0000OO0OOO00O0 }#line:50
        elif O0O0OOO0O0O0O000O ['retcode']=='0'and 'userInfo'in O0O0OOO0O0O0O000O ['data']:#line:51
            OO0OO000OOO00OOO0 =O0O0OOO0O0O0O000O ['data']['userInfo']['baseInfo']['nickname']#line:52
            return {'code':200 ,'name':OO0OO000OOO00OOO0 ,'ck':OOOO0OOO00O00OO0O }#line:53
    except Exception as OOOOOOOOOO0OO0OO0 :#line:54
        return {'code':0 ,'data':OOOOOOOOOO0OO0OO0 }#line:55
def get_time ():#line:58
    O0OO0OOOOOO00OO0O =round (time .time ()*1000 )#line:59
    return O0OO0OOOOOO00OO0O #line:60
async def plogin (O00O0O0OO000OO0OO ,O0000OO00OO00000O ):#line:63
    OO0OOOO00O00O0OO0 =get_time ()#line:64
    O0OOO0OO00000OOO0 =f'https://plogin.m.jd.com/cgi-bin/ml/islogin?time={OO0OOOO00O00O0OO0}&callback=__jsonp{OO0OOOO00O00O0OO0 - 2}&_={OO0OOOO00O00O0OO0 + 2}'#line:65
    OOOOO0000OO0OOOOO ={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh-Hans;q=0.9','Connection':'keep-alive','Cookie':O0000OO00OO00000O ,'Host':'plogin.m.jd.com','Referer':'https://prodev.m.jd.com/','User-Agent':O00O0O0OO000OO0OO }#line:75
    OOOOOOO000OO00O00 =requests .get (url =O0OOO0OO00000OOO0 ,headers =OOOOO0000OO0OOOOO ,timeout =None ).text #line:76
    return OOOOOOO000OO00O00 #line:77
async def memberBringRanking (O00000O000000O0O0 ,OOOO000OO0O00O000 ):#line:80
    O000O0O0OO0OOOO0O =get_time ()#line:81
    O00O0OO00O0O0OO0O ={"code":authorCode ,"pageNum":1 ,"pageSize":10 }#line:86
    O0O0OOOOO000O00OO =f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={O000O0O0OO0OOOO0O}&functionId=memberBringRanking&body={json.dumps(O00O0OO00O0O0OO0O)}&code={authorCode}&pageNum=1&pageSize=10"#line:87
    OOO0O0O000000O00O ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','content-type':'application/json','cookie':OOOO000OO0O00O000 ,'origin':'https://prodev.m.jd.com','referer':'https://prodev.m.jd.com/','user-agent':O00000O000000O0O0 }#line:97
    OO0000000000O0O0O =requests .request ("GET",O0O0OOOOO000O00OO ,headers =OOO0O0O000000O00O ).text #line:98
    print (OO0000000000O0O0O )#line:99
    return json .loads (OO0000000000O0O0O )#line:100
async def memberBringActPage (OOO0OO00OO00O0O0O ,O0OO0000O0OOO00OO ):#line:103
    OOO0OO000OO00O0OO =get_time ()#line:104
    O0OO00O000O0O0OOO ={"code":authorCode ,"invitePin":invitePin ,"_t":OOO0OO000OO00O0OO }#line:109
    OO0O0000O00O0OO00 =f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={OOO0OO000OO00O0OO}&functionId=memberBringActPage&body={json.dumps(O0OO00O000O0O0OOO)}&code={authorCode}&invitePin={invitePin}&_t={t}"#line:110
    O0000OO0OO0OOOO0O ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','content-type':'application/json','cookie':O0OO0000O0OOO00OO ,'origin':'https://prodev.m.jd.com','referer':'https://prodev.m.jd.com/','user-agent':OOO0OO00OO00O0O0O }#line:120
    O0O0OOOO0O0O00000 =requests .request ("GET",OO0O0000O00O0OO00 ,headers =O0000OO0OO0OOOO0O ).text #line:121
    return json .loads (O0O0OOOO0O0O00000 )#line:123
async def memberBringJoinMember (O000OO00OO0O0O000 ,O0O00OO0OO0O0OO00 ):#line:126
    OOOOO0OOOO0O0O0OO =get_time ()#line:127
    OOO000O000OO00000 ={"code":authorCode ,"invitePin":invitePin }#line:131
    O000O0OO00OOOO00O =f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={OOOOO0OOOO0O0O0OO}&functionId=memberBringJoinMember&body={json.dumps(OOO000O000OO00000)}&code={authorCode}&invitePin={invitePin}"#line:132
    OO00OOO00O0000O00 ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','content-type':'application/json','cookie':O0O00OO0OO0O0OO00 ,'origin':'https://prodev.m.jd.com','referer':'https://prodev.m.jd.com/','user-agent':O000OO00OO0O0O000 }#line:142
    OOO0OO00O0OOOO0OO =requests .request ("GET",O000O0OO00OOOO00O ,headers =OO00OOO00O0000O00 ).text #line:143
    return json .loads (OOO0OO00O0OOOO0OO )#line:144
async def check_ruhui (OO0O0O0OOOOOO0000 ,OO0O000OOOO00O0O0 ,OOOOO00O00000O000 ,O00O0OOO0OO000OOO ):#line:146
    O0OOO0O00OO00O0O0 =f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(OO0O0O0OOOOOO0000)}&client=H5&clientVersion=9.2.0&uuid=88888'#line:147
    OOO000OO000O0O000 ={'Host':'api.m.jd.com','Accept':'*/*','Connection':'keep-alive','Cookie':OO0O000OOOO00O0O0 ,'User-Agent':O00O0OOO0OO000OOO ,'Accept-Language':'zh-cn','Referer':f'https://shopmember.m.jd.com/shopcard/?venderId={OOOOO00O00000O000}&channel=801&returnUrl={json.dumps(activityUrl)}','Accept-Encoding':'gzip, deflate'}#line:157
    OOO0000000OOOO0OO =requests .get (url =O0OOO0O00OO00O0O0 ,headers =OOO000OO000O0O000 ,timeout =None ).text #line:158
    return json .loads (OOO0000000OOOO0OO )#line:159
async def memberBringInviteReward (O0O0OO00O0000O0OO ,OOOOOOO0000OOOOO0 ,OO0O0O0OOO000OOO0 ):#line:162
    O0OOOOOOO00O00O00 =get_time ()#line:163
    OOOO00O0O0O0O000O ={"code":authorCode ,"stage":OO0O0O0OOO000OOO0 }#line:167
    OO0O0OOOOO00O0000 =f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={O0OOOOOOO00O00O00}&functionId=memberBringInviteReward&body={OOOO00O0O0O0O000O}&code={authorCode}&stage={OO0O0O0OOO000OOO0}"#line:168
    O0OO0O000O00OOO0O ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','content-type':'application/json','cookie':O0O0OO00O0000O0OO ,'origin':'https://prodev.m.jd.com','referer':'https://prodev.m.jd.com/','user-agent':OOOOOOO0000OOOOO0 }#line:178
    O000O0000OO0O0O00 =requests .request ("GET",OO0O0OOOOO00O0000 ,headers =O0OO0O000O00OOO0O ).text #line:179
    return json .loads (O000O0000OO0O0O00 )#line:180
async def memberBringFirstInvite (OOO0OO00OOO0O00O0 ,O00OO0000O00O00OO ):#line:183
    O0O000O0OO00OOO0O ={"code":authorCode ,}#line:186
    OO0OOOOOOO0000OO0 =f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t=1664407539127&functionId=memberBringFirstInvite&body={json.dumps(O0O000O0OO00OOO0O)}&code={authorCode}"#line:187
    OOOO0OOO0OO00000O ={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'zh-CN,zh;q=0.9','content-type':'application/json','cookie':OOO0OO00OOO0O00O0 ,'origin':'https://prodev.m.jd.com','referer':'https://prodev.m.jd.com/','user-agent':O00OO0000O00O00OO }#line:197
    O000O0O0O000OOO0O =requests .request ("GET",OO0OOOOOOO0000OO0 ,headers =OOOO0OOO0OO00000O ).text #line:198
    return json .loads (O000O0O0O000OOO0O )#line:199
async def get_ck (OOO0O00O0OOOO0O00 ):#line:201
    OOO00O000OO00O00O =[]#line:202
    if OOO0O00O0OOOO0O00 ['code']!=200 :#line:203
        return {'code':0 ,'data':OOO0O00O0OOOO0O00 }#line:204
    else :#line:205
        OO00O00OOO00O00O0 =OOO0O00O0OOOO0O00 ['data']#line:206
        for O0OOO00OO0OOOOOOO in OO00O00OOO00O00O0 :#line:207
            if 'remarks'in O0OOO00OO0OOOOOOO and O0OOO00OO0OOOOOOO ['name']=='JD_COOKIE':#line:208
                OOO00O000OO00O00O .append (O0OOO00OO0OOOOOOO ['value'])#line:209
            else :#line:210
                pass #line:211
    return OOO00O000OO00O00O #line:212
def checkpin (OOOOO000O0OOO00OO :list ,O00O0OOOO0000OO0O ):#line:215
    for O00O0OOO0OOOOOO00 in OOOOO000O0OOO00OO :#line:216
        if O00O0OOOO0000OO0O in O00O0OOO0OOOOOO00 :#line:217
            return O00O0OOO0OOOOOO00 #line:218
        else :#line:219
            None #line:220
async def main ():#line:223
    try :#line:224
        OO0O00000O00OOOO0 =getCk #line:225
        if not OO0O00000O00OOOO0 :#line:226
            return #line:227
    except :#line:228
        print ("未获取到有效COOKIE,退出程序！")#line:229
        return #line:230
    O00O0O00O0OO00OO0 =0 #line:231
    global invitePin ,activityUrl ,MSG #line:232
    MSG =''#line:233
    OO000OO000OOOOOOO ="🗣消息提醒：邀好友赢大礼"#line:234
    OOOO0O0OO00O000O0 =re .compile (r"pt_pin=(.*?);")#line:235
    O0O0OOO0OOO0000O0 =OOOO0O0OO00O000O0 .findall (OO0O00000O00OOOO0 [0 ])[0 ]#line:236
    OOOOO00O0O00O0OO0 =checkpin (OO0O00000O00OOOO0 ,O0O0OOO0OOO0000O0 )#line:237
    try :#line:238
        invitePin =remote_redis (f"invite_{authorCode}",1 )#line:239
        if not invitePin :#line:240
            invitePin =O0O0OOO0OOO0000O0 #line:241
    except :#line:242
        invitePin =O0O0OOO0OOO0000O0 #line:243
    activityUrl =f'https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}&invitePin={invitePin}'#line:244
    OOO0OOOOO00OOO00O =[]#line:245
    OO0OO0O0OO0OOOOOO =[]#line:246
    OO0O000O00OOO000O =[]#line:247
    if OOOOO00O0O00O0OO0 :#line:248
        print (f"📝若已加入活动店铺会员,则无法助力。\n【🛳活动入口】https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}\n")#line:249
        OOOO0OOOO0OOO0000 =userAgent ()#line:250
        O000O0O000000O0O0 =await check (OOOO0OOOO0OOO0000 ,OOOOO00O0O00O0OO0 )#line:251
        if O000O0O000000O0O0 ['code']==200 :#line:252
            await plogin (OOOO0OOOO0OOO0000 ,OOOOO00O0O00O0OO0 )#line:253
            await asyncio .sleep (2 )#line:254
            O000O0O000000O0O0 =await memberBringActPage (OOOO0OOOO0OOO0000 ,OOOOO00O0O00O0OO0 )#line:255
            await memberBringFirstInvite (OOOOO00O0O00O0OO0 ,OOOO0OOOO0OOO0000 )#line:256
            if O000O0O000000O0O0 ['success']:#line:257
                O0O00O0O00OOOO000 =O000O0O000000O0O0 ['data']['brandName']#line:258
                O000OO0O00OO000OO =O000O0O000000O0O0 ['data']['venderId']#line:259
                OOOO00000O0O0O0O0 =[]#line:260
                O0OO0O00O0OOO0OO0 =[]#line:261
                OO0OOOOOO0OO00O00 =O000O0O000000O0O0 ['data']['successCount']#line:262
                O00O0O00O0OO00OO0 +=OO0OOOOOO0OO00O00 #line:263
                O000OO0OOO000OOO0 =O000O0O000000O0O0 ['data']['rewards']#line:264
                print (f'🤖您好！账号[{O0O0OOO0OOO0000O0}]\n✅开启{O0O00O0O00OOOO000}邀请好友活动\n去开活动')#line:265
                MSG +=f'✅账号[{O0O0OOO0OOO0000O0}]\n开启{O0O00O0O00OOOO000}邀请好友活动\n📝活动地址https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}\n'#line:266
                for O00O0OO00000OO0O0 in O000OO0OOO000OOO0 :#line:267
                    O00OO00O000OO00O0 =O00O0OO00000OO0O0 ['stage']#line:268
                    OOO000OO0000OO00O =O00O0OO00000OO0O0 ['inviteNum']#line:269
                    OO0O000O00OOO000O .append (OOO000OO0000OO00O )#line:270
                    O000O00O00OOO00OO =O00O0OO00000OO0O0 ['rewardName']#line:271
                    O0OO0O00O0OOO0OO0 .append (O000O00O00OOO00OO )#line:272
                    OOOO0O00OOOO00000 =O00O0OO00000OO0O0 ['rewardStock']#line:273
                    if OOOO0O00OOOO00000 !=0 :#line:274
                        OOO0OOOOO00OOO00O .append (OOO000OO0000OO00O )#line:275
                        OO0OO0O0OO0OOOOOO .append (OOO000OO0000OO00O )#line:276
                    OOOO00000O0O0O0O0 .append (f'级别{O00OO00O000OO00O0}:  需助力{OOO000OO0000OO00O}人，奖品: {O000O00O00OOO00OO}，库存：{OOOO0O00OOOO00000}件\n')#line:277
                if len (OOOO00000O0O0O0O0 )!=0 :#line:278
                    print ('🎁当前活动奖品如下: \n'+str ('\n'.join (OOOO00000O0O0O0O0 ))+f'\n当前已助力{OO0OOOOOO0OO00O00}次\n')#line:279
                    MSG +=f"🎁当前活动奖品如下: \n{str(''.join(OOOO00000O0O0O0O0))}\n"#line:280
                    for OOO0OO0OOOO0O0O00 in OO0OO0O0OO0OOOOOO :#line:281
                        if O00O0O00O0OO00OO0 >=OOO0OO0OOOO0O0O00 :#line:282
                            print ("🎉您当前助力已经满足了，可以去领奖励了")#line:283
                            print (f'\n📝这就去领取奖励{OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00) + 1}')#line:284
                            O000O0O000000O0O0 =await memberBringInviteReward (OOOOO00O0O00O0OO0 ,OOOO0OOOO0OOO0000 ,OO0O000O00OOO000O .index (OOO0OO0OOOO0O0O00 )+1 )#line:285
                            try :#line:286
                                if O000O0O000000O0O0 ['success']:#line:287
                                    print (f"🎉成功领取 {O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]}")#line:288
                                    MSG +=f"🎉成功领取 {O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]}\n"#line:289
                                else :#line:290
                                    print (f"⛈{O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]} {O000O0O000000O0O0['errorMessage']}")#line:291
                                    MSG +=f"⛈{O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]} {O000O0O000000O0O0['errorMessage']}\n"#line:292
                            except :#line:293
                                print (O000O0O000000O0O0 )#line:294
                                MSG +=f"{O000O0O000000O0O0}\n"#line:295
                            OOO0OOOOO00OOO00O .remove (OOO0OO0OOOO0O0O00 )#line:296
                            await asyncio .sleep (10 )#line:297
                    OO0OO0O0OO0OOOOOO =OOO0OOOOO00OOO00O #line:298
                    if OOO0OOOOO00OOO00O ==[]:#line:299
                        print ('🎉🎉🎉奖励已经全部获取啦，退出程序')#line:300
                        MSG +=f"🎉🎉🎉奖励已经全部获取啦~\n"#line:301
                        MSG =f"⏰{str(datetime.now())[:19]}\n"+MSG #line:302
                        send (OO000OO000OOOOOOO ,MSG )#line:303
                        return #line:304
                for OOOO0000OOOOOO0OO ,O0000O00OO00000OO in enumerate (OO0O00000O00OOOO0 ,1 ):#line:305
                    OOOO0OOOO0OOO0000 =userAgent ()#line:306
                    try :#line:307
                        OOOO0O0000000OO00 =re .findall (r'(pt_pin=([^; ]+)(?=;))',str (O0000O00OO00000OO ))[0 ]#line:308
                        OOOO0O0000000OO00 =(unquote_plus (OOOO0O0000000OO00 [1 ]))#line:309
                    except IndexError :#line:310
                        OOOO0O0000000OO00 =f'用户{OOOO0000OOOOOO0OO}'#line:311
                    print (f'******开始【京东账号{OOOO0000OOOOOO0OO}】{OOOO0O0000000OO00} *********\n')#line:312
                    for O00O0OO00000OO0O0 ,OOO0OO0OOOO0O0O00 in enumerate (OOO0OOOOO00OOO00O ,1 ):#line:313
                        for OOO0OO0OOOO0O0O00 in OO0OO0O0OO0OOOOOO :#line:314
                            if O00O0O00O0OO00OO0 >=OOO0OO0OOOO0O0O00 :#line:315
                                print (OOO0OO0OOOO0O0O00 )#line:316
                                print ("🎉您当前助力已经满足了，可以去领奖励了")#line:317
                                print (f'\n📝这就去领取奖励{OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00) + 1}')#line:318
                                O000O0O000000O0O0 =await memberBringInviteReward (OOOOO00O0O00O0OO0 ,OOOO0OOOO0OOO0000 ,OO0O000O00OOO000O .index (OOO0OO0OOOO0O0O00 )+1 )#line:319
                                try :#line:320
                                    if O000O0O000000O0O0 ['success']:#line:321
                                        print (f"🎉成功领取 {O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]}")#line:322
                                        MSG +=f"🎉成功领取 {O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]}\n"#line:323
                                    else :#line:324
                                        print (f"⛈{O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]} {O000O0O000000O0O0['errorMessage']}")#line:325
                                        MSG +=f"⛈{O0OO0O00O0OOO0OO0[OO0O000O00OOO000O.index(OOO0OO0OOOO0O0O00)]} {O000O0O000000O0O0['errorMessage']}\n"#line:326
                                except :#line:327
                                    print (O000O0O000000O0O0 )#line:328
                                    MSG +=f"{O000O0O000000O0O0}\n"#line:329
                                OOO0OOOOO00OOO00O .remove (OOO0OO0OOOO0O0O00 )#line:330
                                await asyncio .sleep (10 )#line:331
                        OO0OO0O0OO0OOOOOO =OOO0OOOOO00OOO00O #line:332
                        if OOO0OOOOO00OOO00O ==[]:#line:333
                            print ('🎉🎉🎉奖励已经全部获取啦，退出程序')#line:334
                            MSG +=f"🎉🎉🎉奖励已经全部获取啦~\n"#line:335
                            MSG =f"⏰{str(datetime.now())[:19]}\n"+MSG #line:336
                            send (OO000OO000OOOOOOO ,MSG )#line:337
                            return #line:338
                    await plogin (OOOO0OOOO0OOO0000 ,O0000O00OO00000OO )#line:339
                    O000O0O000000O0O0 =await check (OOOO0OOOO0OOO0000 ,O0000O00OO00000OO )#line:340
                    if OOOO0000OOOOOO0OO !=1 :#line:341
                        invitePin =O0O0OOO0OOO0000O0 #line:342
                        activityUrl =f'https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}&invitePin={invitePin}'#line:343
                    if O000O0O000000O0O0 ['code']==200 :#line:344
                        O000O0O000000O0O0 =await memberBringActPage (OOOO0OOOO0OOO0000 ,O0000O00OO00000OO )#line:345
                        if O000O0O000000O0O0 ['success']:#line:346
                            print (f'✅账户[{OOOO0O0000000OO00}]已开启{O0O00O0O00OOOO000}邀请好友活动\n')#line:347
                            await asyncio .sleep (3 )#line:348
                            O000O0O000000O0O0 =await check_ruhui ({"venderId":str (O000OO0O00OO000OO ),"channel":"401"},O0000O00OO00000OO ,O000OO0O00OO000OO ,OOOO0OOOO0OOO0000 )#line:350
                            try :#line:351
                                if O000O0O000000O0O0 ['result']['userInfo']['openCardStatus']==0 :#line:352
                                    await asyncio .sleep (2 )#line:353
                                    print (f'😆您还不是会员哦，这就去去助力{invitePin}\n')#line:354
                                    O000O0O000000O0O0 =await memberBringJoinMember (OOOO0OOOO0OOO0000 ,O0000O00OO00000OO )#line:355
                                    if O000O0O000000O0O0 ['success']:#line:356
                                        O00O0O00O0OO00OO0 +=1 #line:357
                                        print (f'🎉助力成功! 当前成功助力{O00O0O00O0OO00OO0}个\n')#line:358
                                    else :#line:359
                                        if '交易失败'in str (O000O0O000000O0O0 ):#line:360
                                            O00O0O00O0OO00OO0 +=1 #line:361
                                            print (f'🎉助力成功! 当前成功助力{O00O0O00O0OO00OO0}个\n')#line:362
                                        else :#line:363
                                            try :#line:364
                                                print (f"⛈{O000O0O000000O0O0['errorMessage']}")#line:365
                                            except :#line:366
                                                print (O000O0O000000O0O0 )#line:367
                                    await asyncio .sleep (2 )#line:368
                                else :#line:369
                                    print ('⛈您已经是会员啦，不去请求入会了\n')#line:370
                                    continue #line:371
                            except TypeError as O0OOO0OO0O00OO00O :#line:372
                                print (O0OOO0OO0O00OO00O )#line:373
                                O000O0O000000O0O0 =await memberBringJoinMember (OOOO0OOOO0OOO0000 ,O0000O00OO00000OO )#line:374
                                if O000O0O000000O0O0 ['success']:#line:375
                                    O00O0O00O0OO00OO0 +=1 #line:376
                                    print (f'🎉助力成功! 当前成功助力{O00O0O00O0OO00OO0}个\n')#line:377
                                else :#line:378
                                    if '交易失败'in O000O0O000000O0O0 :#line:379
                                        O00O0O00O0OO00OO0 +=1 #line:380
                                        print (f'🎉助力成功! 当前成功助力{O00O0O00O0OO00OO0}个\n')#line:381
                                    else :#line:382
                                        print (f"⛈{O000O0O000000O0O0['errorMessage']}")#line:383
                                await asyncio .sleep (2 )#line:384
                            if OOOO0000OOOOOO0OO ==1 :#line:385
                                await memberBringFirstInvite (OOOOO00O0O00O0OO0 ,OOOO0OOOO0OOO0000 )#line:386
                        else :#line:388
                            print ('未获取到活动参数信息\n')#line:389
                            break #line:390
                    else :#line:391
                        print (O000O0O000000O0O0 ['data'])#line:392
                        continue #line:393
            else :#line:394
                print ('未能获取到活动信息\n')#line:395
                return #line:396
        else :#line:398
            print (O000O0O000000O0O0 ['data'])#line:399
            return #line:400
    else :#line:401
        print (f'pin填写有误，请重试')#line:402
if __name__ =="__main__":#line:405
    asyncio .run (main ())