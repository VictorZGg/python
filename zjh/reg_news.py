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


report = pd.DataFrame(columns=['主体', '内容', '日期', '链接'])
head = {'user-agent': 'Mozilla/5.0', 'Connection':'close'}


######### 证券期货法律法规：全量
#from selenium import webdriver
#report_2 = pd.DataFrame(columns=['序号', '文件', '文号', '单位', '发文日期'])
#url = 'https://neris.csrc.gov.cn/falvfagui/'
#opt = webdriver.ChromeOptions()
#driver = webdriver.Chrome(chrome_options = opt)
#driver.maximize_window()
#driver.get(url)
#time.sleep(3)
#
#source_html = driver.page_source
#x = BeautifulSoup(source_html, "html.parser")
#page_max = x.find('div', {'class': 'jump'}).find_all('span')[3].text
#page_max = int(page_max[page_max.find('有')+1:page_max.find('页')])
#
#page_no = 1
## 第一页
#print ('=================第'+str(page_no)+'页,共'+str(page_max)+'页======================')
#t = x.find('tbody').find_all('tr')
#for i in t:
#    s = i.find_all('td')
#    report_i = []
#    for j  in s:
#        report_i.append(j.text)
#    report_2.loc[len(report_2)] = report_i
#
## 其余页
#while page_no < page_max:
#    page_no += 1
#    print ('=================第'+str(page_no)+'页,共'+str(page_max)+'页======================')
#    path_1 = driver.find_element_by_xpath("//a[text()='下一页']")
#    path_1.click()
#    time.sleep(0.5)
#    
#    source_html = driver.page_source
#    x = BeautifulSoup(source_html, "html.parser")
#    t = x.find('tbody').find_all('tr')
#    for i in t:
#        s = i.find_all('td')
#        report_i = []
#        for j  in s:
#            report_i.append(j.text)
#        report_2.loc[len(report_2)] = report_i
#    
#driver.quit()
#
#path = 'D:\\tools\\python\\python\\zjh\\sec_and_fut_regulation_list.xlsx'
#report_2.to_excel(path,index=False,header=True)




######### 证监会要闻、证监会令、证监会公告、证监会行政许可、处罚、禁入、复议

#for i in t:
#    content = i.a['title']
#    ref = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd' + i.a['href'][1:]
#    pub_date = i.span.text
#    report_i = ['证监会要闻', content, pub_date, ref]
#    report.loc[len(report)] = report_i
#
#url = 'http://www.csrc.gov.cn/pub/newsite/'
#soup = getSoup(url, head)
#t = soup.find_all('div', {'class': 'in_new'})[1].find('ul').find_all('li')
#for i in t:
#    content = i.a['title']
#    ref = 'http://www.csrc.gov.cn/pub' + i.a['href'][2:]
#    pub_date = i.span.text
#    report_i = ['证监会令', content, pub_date, ref]
#    report.loc[len(report)] = report_i
#
#t = soup.find_all('div', {'class': 'in_new'})[2].find('ul').find_all('li')
#for i in t:
#    content = i.a['title']
#    ref = 'http://www.csrc.gov.cn/pub' + i.a['href'][2:]
#    pub_date = i.span.text
#    report_i = ['证监会公告', content, pub_date, ref]
#    report.loc[len(report)] = report_i

########## 证监会投资者教育、非法活动警示、部门更新、派出机构更新
#type_dict = {'投资者教育': 'con5_1_1',
#             '风险警示': 'con5_1_2'
#             }
#for zjh_type, zjh_id in type_dict.items():
#    t = soup.find('div', {'id': zjh_id}).find('ul').find_all('li')
#    for i in t:
#        content = i.a['title']
#        ref = 'http://www.csrc.gov.cn/pub/newsite' + i.a['href'][1:]
#        pub_date = i.span.text
#        report_i = [zjh_type, content, pub_date, ref]
#        report.loc[len(report)] = report_i
#
#type_dict = {'机关部门': 'con2_1_1',
#             '派出机构': 'con2_1_2'
#             }
#for zjh_type, zjh_id in type_dict.items():
#    t = soup.find('div', {'id': zjh_id}).find('ul').find_all('li')
#    for i in t:
#        content = i.a.text
#        ref = 'http://www.csrc.gov.cn/pub' + i.a['href'][2:]
#        pub_date = i.span.text
#        report_i = [zjh_type, content, pub_date, ref]
#        report.loc[len(report)] = report_i


######### 证监会要闻、证监会令、证监会公告、证监会行政许可、处罚、禁入、复议
url = 'http://www.csrc.gov.cn'
soup = getSoup(url, head)
t = soup.find_all('div', {'class': 'tab-content'})[0].find_all('div', {'class': 'tab-list'})[0]
t1 = t.find('div', {'class': 'fl txt'})
content = t1.a.text
ref = url + t1.a['href']
pub_date = t1.span.text
report.loc[len(report)] = ['证监会要闻', content, pub_date, ref]
t2 = t.find_all('li', {'class': 'li-height'})
for i in t2:
    content = i.a.text
    ref = url + i.a['href']
    pub_date = '2021-'+i.span.text
    report_i = ['证监会要闻', content, pub_date, ref]
    report.loc[len(report)] = report_i
    

type_dict = {'证监会令': 12,
             '证监会公告': 13,
             # '政务信息': 14,
             '行政许可进度': 5,
             '发审委公告': 6,
             '行政许可结果': 7,
             ###上面需要减掉最后一个add-more
             '辖区监管动态': 2,
             '政务信息': 3,
             '监管指引': 4,
             '征求意见': 8
             }

for zjh_type, zjh_id in type_dict.items():
    if zjh_id in [12,13,14,5,6,7]:
        t = soup.find_all('div', {'class': 'tab-content'})[zjh_id].find_all('li')[:-1]
    else:
        t = soup.find_all('div', {'class': 'tab-content'})[zjh_id].find_all('li')
    for i in t:
        content = i.a.text
        ref = url + i.a['href']
        pub_date = '2021-'+ i.find('span', class_='time').text
        report_i = [zjh_type, content, pub_date, ref]
        report.loc[len(report)] = report_i

######### 上交所
url = 'http://www.sse.com.cn/aboutus/mediacenter/hotandd/'
soup = getSoup(url, head)
t = soup.find('div', {'id': 'sse_list_1'}).find_all('dd')
for i in t:
    content = i.a['title']
    ref = 'http://www.sse.com.cn' + i.a['href']
    pub_date = i.span.text
    report_i = ['上交所动态', content, pub_date, ref]
    report.loc[len(report)] = report_i

######### 深交所
url = 'http://www.szse.cn/aboutus/trends/news/index.html'
soup = getSoup(url, head)
t = soup.find('ul', {'class': 'newslist date-right'}).find_all('li')
for i in t:
    content = re.search('curTitle = .*?;', str(i)).group()[12:-2]
    ref = 'http://www.szse.cn/aboutus/trends/news' + re.search('curHref = .*?;', str(i)).group()[12:-2]
    pub_date = str.strip(i.span.text)
    report_i = ['深交所动态', content, pub_date, ref]
    report.loc[len(report)] = report_i       

######### 中金所
url = 'http://www.cffex.com.cn/jysdt/'
soup = getSoup(url, head)
t = soup.find('div', {'class': 'notice_list'}).find('ul').find_all('li')
for i in t:
    content = i.find_all('a')[0]['title']
    ref = 'http://www.cffex.com.cn/' + i.find_all('a')[0]['href']
    pub_date = i.find_all('a')[1].text
    report_i = ['中金所动态', content, pub_date, ref]
    report.loc[len(report)] = report_i

######### 中国结算
url = 'http://www.chinaclear.cn/zdjs/xtzgg/center_flist.shtml'
soup = getSoup(url, head)
t = soup.find('div', {'class': 'pageTabContent'}).find_all('li')
for i in t:
    content = i.a['title']
    ref = 'http://www.chinaclear.cn/' + i.a['href'][6:]
    pub_date = i.span.text
    report_i = ['中国结算动态', content, pub_date, ref]
    report.loc[len(report)] = report_i  


######### 基金业协会
url = 'https://www.amac.org.cn/aboutassociation/gyxh_xhdt/xhdt_xhtz/'
soup = getSoup(url, head)
t = soup.find('div', {'class': 'c-box'}).find_all('li')
for i in t:
    content = i.a.text
    ref = 'https://www.amac.org.cn/aboutassociation/gyxh_xhdt/xhdt_xhtz' + i.a['href'][1:]
    pub_date = str.strip(i.i.text)
    report_i = ['基金业协会动态', content, pub_date, ref]
    report.loc[len(report)] = report_i  

######### 证券业协会
url = 'https://www.sac.net.cn/ljxh/xhgzdt/'
soup = getSoup(url, head)
t1 = soup.find_all('td', {'class': 'pad_le30 hei_000'})
t2 = soup.find_all('td', {'width': '95'})
for i in range(len(t1)):
    content = t1[i].a['title']
    ref = 'https://www.sac.net.cn/ljxh/xhgzdt' + t1[i].a['href'][1:]
    pub_date = t2[i].text
    report_i = ['证券业协会动态', content, pub_date, ref]
    report.loc[len(report)] = report_i


###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\zjh\\regulation_news.xlsx'
report.to_excel(path,index=False,header=True)

import os
os.system(path)        
    
    
        
    
        
