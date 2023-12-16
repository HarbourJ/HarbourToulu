#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 23:00
# @Author  : HarbourJ
# @TG      : https://t.me/HarbourToulu
# @File    : jdCookie.py

import os #line:1
import time #line:2
from functools import partial #line:3
print =partial (print ,flush =True )#line:4
def get_cookies ():#line:7
    O000OO00000OO00O0 =[]#line:8
    if os .environ .get ("JD_COOKIE"):#line:9
        print ("已获取并使用Env环境 Cookie")#line:10
        if '&'in os .environ ["JD_COOKIE"]:#line:11
            O000OO00000OO00O0 =os .environ ["JD_COOKIE"].split ('&')#line:12
        elif '\n'in os .environ ["JD_COOKIE"]:#line:13
            O000OO00000OO00O0 =os .environ ["JD_COOKIE"].split ('\n')#line:14
        else :#line:15
            O000OO00000OO00O0 =[os .environ ["JD_COOKIE"]]#line:16
    else :#line:18
        if os .path .exists ("JD_COOKIE.txt"):#line:19
            with open ("JD_COOKIE.txt",'r')as OOOO0000O00OO0OO0 :#line:20
                O0O000OO0OOOOO000 =OOOO0000O00OO0OO0 .read ().strip ()#line:21
                if O0O000OO0OOOOO000 :#line:22
                    if '&'in O0O000OO0OOOOO000 :#line:23
                        O000OO00000OO00O0 =O0O000OO0OOOOO000 .split ('&')#line:24
                    elif '\n'in O0O000OO0OOOOO000 :#line:25
                        O000OO00000OO00O0 =O0O000OO0OOOOO000 .split ('\n')#line:26
                    else :#line:27
                        O000OO00000OO00O0 =[O0O000OO0OOOOO000 ]#line:28
                    O000OO00000OO00O0 =sorted (set (O000OO00000OO00O0 ),key =O000OO00000OO00O0 .index )#line:29
        else :#line:31
            print ("未获取到正确✅格式的京东账号Cookie")#line:32
            return #line:33
    print (f"====================共{len(O000OO00000OO00O0)}个京东账号Cookie=========\n")#line:35
    print (f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")#line:36
    print (f"==================🗣活动通知- https://t.me/HarbourToulu=====================\n")#line:37
    return O000OO00000OO00O0 #line:38

# if __name__ == "__main__":
#     get_cookies()
#     print(os.environ.get("JD_COOKIE"))
