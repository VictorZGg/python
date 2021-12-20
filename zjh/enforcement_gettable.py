# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:26:39 2021

@author: zengg
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
# import xlsxwriter
urllib3.disable_warnings()

import os
print (os.getcwd())
os.chdir('D:\\tools\\python\\python\\zjh')


def getSoup(url, head):
    try:
        requests.adapters.DEFAULT_RETRIES = 5 # 增加连接重试次数
        s = requests.session()
        s.keep_alive = False # http connection关闭keep-alive
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # r = requests.get(url, headers = kv)
        r = requests.get(url, headers = head, verify=False)
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

origin_table = pd.read_excel(io = 'zjh_enforcement.xlsx')
head = {'user-agent': 'Mozilla/5.0', 'Connection':'close'}

report = pd.DataFrame(columns=['发布机构','发文日期','名称','文号','内容'])
# i = 0
for i in range(len(origin_table)):
    print ('===========第'+str(i+1)+'条记录===========')
    origin_table_i = origin_table.loc[i]
    url = origin_table_i['url']
    soup = getSoup(url, head)
    t1 = soup.find('div', {'class': 'xxgk-table'}).table.tbody.find_all('tr')
    pub_institution = t1[1].find_all('td')[0].text
    pub_date = origin_table_i['发文日期']
    pub_title = origin_table_i['标题']
    pub_nbr = origin_table_i['文号']
    
    t2 = soup.find('div', {'class': 'detail-news'}).find_all('p')
    pub_content = ''
    for j in t2:
        pub_content = pub_content + '\n' + j.text
    
    report.loc[len(report)] = [pub_institution, pub_date, pub_title, pub_nbr, pub_content]
    

###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\zjh\\enforcement_table.xlsx'
report.to_excel(path,index=False,header=True)

# import os
# os.system(path)        
    
    
        
    
        
