# -*- coding: utf-8 -*-


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
table = pd.DataFrame(columns=['来源', '类型1', '类型2', '重要程度', '内容', '地址'])
n = 1

# 新华社时政
url_list = ['新华社', 'http://www.xinhuanet.com/politicspro/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('ul', {'class': 'phb_list'}).find_all('a')
for i in t:
    text = i.text
    ref = i['href']
    table_i = [web, '时政', '时政', '头条', text, ref]
    table.loc[len(table)] = table_i
    print ('第'+str(n)+'条：'+text)
    n += 1
    
# 新浪财经
url_list = ['新浪财经_要闻', 'https://finance.sina.com.cn/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('div', {'id': 'blk_hdline_01'}).find_all('a')
for i in t:
    text = i.text
    ref = i['href']
    table_i = [web, '财经', '财经', '头条', text, ref]
    table.loc[len(table)] = table_i
    print ('第'+str(n)+'条：'+text)
    n += 1   

url_list = ['新浪财经_股票', 'https://finance.sina.com.cn/stock/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t1 = soup.find('div', {'class': 'tabs-cont sto_cont0'}).find_all('div', {'class': 'hdline'})
for i in t1:
    J = i.find('h2').find_all('a')
    for j in J:
        try:
            text = j.text
            ref = j['href']
            table_i = [web, '财经', '股票', '头条', text, ref]
            table.loc[len(table)] = table_i
            print ('第'+str(n)+'条：'+text)
            n += 1
        except:
            pass

t2 = soup.find_all('ul', {'class': 'list01'})
for i in t2:
        J = i.find_all('a', {'style': False})
        for j in J:
            try:
                text = j.text
                ref = j['href']
                table_i = [web, '财经', '股票', '消息', text, ref]
                table.loc[len(table)] = table_i
                print ('第'+str(n)+'条：'+text)
                n += 1
            except:
                pass

url_list = ['新浪财经_港股', 'http://finance.sina.com.cn/stock/hkstock/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('div', {'id': 'fin_tabs0_c0'}).find_all('a')
for i in t:
    text = i.text
    ref = i['href']
    table_i = [web, '财经', '港股', '消息', text, ref]
    table.loc[len(table)] = table_i
    print ('第'+str(n)+'条：'+text)
    n += 1
    
url_list = ['新浪财经_美股', 'https://finance.sina.com.cn/stock/usstock/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('div', {'class': 'main-left-col2 fr'}).find_all(['h3','li'])
for i in t:
    try:
        text = i.text
        ref = i.find('a')['href']
        table_i = [web, '财经', '美股', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

url_list = ['新浪财经_基金', 'https://finance.sina.com.cn/fund/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('div', {'class': 'top_news_focus'}).find_all(['h3','li'])
for i in t:
    try:
        text = i.text
        ref = i.find('a')['href']
        table_i = [web, '财经', '基金', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

url_list = ['新浪财经_期货', 'https://finance.sina.com.cn/futuremarket/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t1 = soup.find('div', {'class': 'blk12'}).find('div', {'class': 'top dotbtm'}).find_all('a')
for i in t1:
    try:
        text = i.text
        ref = i['href']
        table_i = [web, '财经', '期货', '头条', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

t2 = soup.find('div', {'class': 'blk12'}).find('ul', {'class': 'dotbtm'}).find_all('li')
for i in t2:
    try:
        j = i.find('a', {'class': 'grey43'})
        text = j.text
        ref = j['href']
        table_i = [web, '财经', '期货', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

url_list = ['新浪财经_外汇', 'https://finance.sina.com.cn/forex/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t = soup.find('div', {'class': 'Center headline'}).find_all('a', {'class':False})
for i in t:
    try:
        text = i.text
        ref = i['href']
        table_i = [web, '财经', '外汇', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

url_list = ['新浪财经_黄金', 'https://finance.sina.com.cn/nmetal/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t1 = soup.find('div', {'class': 'headline'}).find('h2')
text = t1.a.text
ref = t1.a['href']
table.loc[len(table)] = [web, '财经', '黄金', '头条', text, ref]
n += 1

t2 = soup.find('div', {'class': 'top_news'}).find_all('a')
for i in t2:
    try:
        text = i.text
        ref = i['href']
        table_i = [web, '财经', '黄金', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass
   
url_list = ['新浪财经_债券', 'http://finance.sina.com.cn/bond/']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t1 = soup.find('div', {'class': 'blk_yw'}).find('h2')
text = t1.a.text
ref = t1.a['href']
table.loc[len(table)] = [web, '财经', '债券', '头条', text, ref]
n += 1

t2 = soup.find('ul', {'class': 'list list01 f14 pot'}).find_all('a')
for i in t2:
    try:
        text = i.text
        ref = i['href']
        table_i = [web, '财经', '债券', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

# CNBC新闻
'''
url_list = ['CNBC', 'https://www.cnbc.com/world/?region=world']
web, url = url_list
print ('======='+web+'======')
soup = getSoup(url, kv)
t1 = soup.find('div', {'id': 'HomePageInternational-FeaturedCard-5-0'}).find('h2')
text = t1.a.text
ref = t1.a['href']
table.loc[len(table)] = [web, '时政', '全球', '头条', text, ref]
n += 1

t2 = soup.find('div', {'class': 'SecondaryCardContainer-container'}).find_all('li')
for i in t2:
    try:
        j = i.find('div', {'class': 'SecondaryCard-headline'}).a
        text = j.text
        ref = j['href']
        table_i = [web, '时政', '全球', '头条', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass

t3 = soup.find('div', {'id': 'Home Page International-riverPlus'})
t3 = t3.find_all('div', {'class': 'RiverHeadline-headline RiverHeadline-hasThumbnail'})
for i in t3:
    try:
        text = i.a.text
        ref = i.a['href']
        table_i = [web, '时政', '全球', '消息', text, ref]
        table.loc[len(table)] = table_i
        print ('第'+str(n)+'条：'+text)
        n += 1
    except:
        pass
'''
###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\web\\news.xlsx'
table.to_excel(path,index=False,header=True)

import os
os.system(path) 

    
        
    
        
