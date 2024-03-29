# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 00:14:22 2021

@author: Administrator
"""

import requests
import urllib3
from bs4 import BeautifulSoup
import pandas as pd


def getSoup(url, kv):
    try:
        requests.adapters.DEFAULT_RETRIES = 5 # 增加连接重试次数
        s = requests.session()
        s.keep_alive = False # http connection关闭keep-alive
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # r = requests.get(url, headers = kv)
        r = requests.get(url, headers = kv, verify=False)
        r.raise_for_status()
        r.encoding = 'utf-8'
        # print("status_code: " + str(r.status_code))
        # print("encoding: " + r.encoding)
    except:
        print("\n\n爬取失败\n\n")
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    # print ('\n\n防止爬取过快，休息1秒钟\n\n')
    #time.sleep(0.1)
    return soup


member_list = pd.read_excel('D:\\tools\\python\\python\\web\\fund_member_private.xlsx')

table = pd.DataFrame(columns=['机构名称', '机构类型'])



kv = {'user-agent': 'Mozilla/5.0', 'Connection':'close'} 

