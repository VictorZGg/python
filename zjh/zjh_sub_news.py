# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:26:39 2021

@author: zengg
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
# import datetime as dt
import urllib3
# import xlsxwriter
urllib3.disable_warnings()


def getSoup(url, kv):
    try:
        requests.adapters.DEFAULT_RETRIES = 5 # 增加连接重试次数
        s = requests.session()
        s.keep_alive = False # http connection关闭keep-alive
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
    time.sleep(0.1)
    return soup

head = {'user-agent': 'Mozilla/5.0', 'Connection':'close'}


url = 'http://www.csrc.gov.cn'
soup = getSoup(url, head)
t = soup.find('div', {'class': 'jg-box'}).find_all('li')

sub_list = {}
for i in t:
    sub_list[i.a.text] = 'http://www.csrc.gov.cn' + i.a['href']


#sub_list = {
#'西藏证监局':'tibet',
#'陕西证监局':'shanxi',
#'甘肃证监局':'gansu',
#'青海证监局':'qinghai',
#'宁夏证监局':'ningxia',
#'新疆证监局':'xinjiang',
#'深圳证监局':'shenzhen',
#'大连证监局':'dalian',
#'宁波证监局':'ningbo',
#'厦门证监局':'xiamen'
#}

report = pd.DataFrame(columns=['主体', '内容', '日期', '链接'])
for sub_name, sub_ref in sub_list.items():
    # url = 'http://www.csrc.gov.cn/' + sub_ref + '/index.shtml'
    url = sub_ref
    soup = getSoup(url, head)
    t = soup.find_all('div', {'class': 'tab-list'})
    for i in t:
        y = i.find_all('li')
        for j in y:      
            if j.attrs=={}:
                content = j.a.text
                ref = 'http://www.csrc.gov.cn' + j.a['href']
                pub_date = '2021-' + j.span.text
                report.loc[len(report)] = [sub_name, content, pub_date, ref]
            else:
                pass

#report = report[report['主体'].isin(['西藏',
#                    '陕西',
#                    '甘肃',
#                    '青海',
#                    '宁夏',
#                    '新疆',
#                    '深圳',
#                    '大连',
#                    '宁波',
#                    '厦门'])]
    
report = report.sort_values(by="日期" , ascending=False)

###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\zjh\\zjh_sub_news.xlsx'
report.to_excel(path,index=False,header=True)

import os
os.system(path)        
    
    
        
    
        
