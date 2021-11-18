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
import datetime as dt
import urllib3
# import xlsxwriter


def type_list():
    type_list = {'证监会令': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3311/index_7401',
     '证监会公告': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3302/index_7401',
     '办事指南': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3308/index_7401'
     #'监管对象名录': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3309/index_7401'     
     # '统计信息': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3310/index_7401',
     # '行政处罚决定': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401',
     # '市场禁入决定': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3619/index_7401',
     # '行政复议': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3620/index_7401',
     # '预先披露': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3306/index_7401',
     # '发审委公告': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3621/index_7401',
     # '重组委公告': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3622/index_7401',
     # '行政许可批复': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3307/index_7401',
     # '非行政许可事项': 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3386/index_7401'
     }
    return type_list

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


def getContent(url, kv, content_type):
    report = pd.DataFrame(columns=['类型', '文件','发文日期', '链接'])
    page_no = 0
    T = True
    while T:
        print ('==========='+'第'+str(page_no+1)+'页===========')
        url_i = url+['_'+str(page_no), ''][page_no == 0]+'.htm'
        soup = getSoup(url_i, kv)
        t = soup.find_all('div', {'class': 'row'})
        if len(t) == 0:
            T = False
        else:
            for i in t:
                content = i.find('li', {'class': 'mc'}).a.text
                ref = 'http://www.csrc.gov.cn/pub/zjhpublic' + i.find('a')['href'][5:]
                pub_date = i.find('li', {'class': 'fbrq'}).text
                report_i = [content_type, content, pub_date, ref]
                report.loc[len(report)] = report_i
        page_no += 1
    return report


if __name__ == '__main__':
    kv = {'user-agent': 'Mozilla/5.0',
          'Connection':'close'}
    type_list = type_list()
    table = pd.DataFrame(columns=['类型', '文件','发文日期', '链接'])
    for key in type_list:
        content_type = key
        url = type_list[key]
        print ('======================='+content_type+'======================')
        table_i = getContent(url, kv, content_type)
        table = pd.concat([table, table_i])
  
    
    ###################### 全部导出至excel文件 ######################
    path = 'D:\\tools\\python\\python\\zjh\\regulation_list.xlsx'
    table.to_excel(path,index=False,header=True)
    
    import os
    os.system(path)        
    
    
        
    
        
