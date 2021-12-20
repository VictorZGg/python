# -*- coding: utf-8 -*-
"""
Created on Oct 5 2021

@author: zengg
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
# import re
# import time
# import datetime as dt
import urllib3
# from selenium import webdriver
# import xlsxwriter


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

kv = {'user-agent': 'Mozilla/5.0', 'Connection':'close'} 
table = pd.DataFrame(columns=['来源', '时间', '内容', '地址'])
n = 1


# 证监会
url = 'http://www.csrc.gov.cn/pub/newsite'
soup = getSoup(url, kv)
name = '证监会'

t = soup.find('div', {'class': 'in_list gao_1'})
print ('======='+name+'要闻======')

t1 = t.find('div', {'class': 'hot'}).find('a')
text = t1['title']
ref = url+t1['href'][1:]
table.loc[len(table)] =[name+'要闻', '', text, ref]
print ('第'+str(n)+'条：'+text)
n += 1

t2 = t.ul.find_all('li')
for i in t2:
    text = i.a['title']
    ref = url+i.a['href'][1:]
    dtime = i.span.text
    table_i = [name+'要闻', dtime, text, ref]
    table.loc[len(table)] = table_i
    print ('第'+str(n)+'条：'+text)
    n += 1





