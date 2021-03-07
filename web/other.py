# -*- coding: utf-8 -*-


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime as dt
import urllib3
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
        # r.encoding = 'utf-8'
        r.encoding = 'gbk'
        # print("status_code: " + str(r.status_code))
        # print("encoding: " + r.encoding)
    except:
        print("\n\n爬取失败\n\n")
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    # print ('\n\n防止爬取过快，休息1秒钟\n\n')
    time.sleep(0.1)
    return soup

def getContent(url_1, kv, page_no):
    table = pd.DataFrame(columns=['类型', '名称', '链接','发布时间','评论数','新评论数'])
    for n in range(page_no):
        print ('==========='+'第'+str(n+1)+'页===========')
        m = ['-'+str(n+1),''][n==0]
        url = url_1 + m
        soup = getSoup(url, kv)
        t = soup.find_all('div', {'class': 'acgiflists'})
        for i in t:
            j = i.find('div', {'class': 'acgiflisttitle'})
            k = i.find('div', {'class': 'acgiflistinfo cl'})
            l = i.find('div', {'class': 'acgifnums'})
            try:
                tp = j.em.text
                content = j.find('a', {'class': 's xst'}).text
                ref = 'https://www.gtloli.one/' + j.find('a', {'class': 's xst'}).get('href')
            except:
                tp = ''
                content = ''
                ref = ''
            try:
                pub_time = k.find('div', {'class': 'acgifby1'})
                pub_time = pub_time.find_all('span')
                pub_time = pub_time[1].text
            except:
                pub_time = ''
            try:
                comments = l.span.text
                n_commments = l.a.text
            except:
                comments = '0'
                n_commments = '0'
            table_i = [tp, content, ref, pub_time, comments, n_commments]
            table.loc[len(table)] = table_i
            print (content)
            print ('-------')
    return table


if __name__ == '__main__':
    url_1 = 'https://www.gtloli.one/f84'
    # url_1 = 'https://www.gtloli.one/f41'
    kv = {'user-agent': 'Mozilla/5.0',
          'Connection':'close'}
    page_no = 10 # 设置查多少页
    # n = 0
    ###################### 获取文件列表 ######################
    x = getContent(url_1, kv, page_no)
    
    x['评论数'] = x['评论数'].astype('int')
    x['新评论数'] = x['新评论数'].astype('int')
    x = x.sort_values(axis = 0, ascending = False, by=['评论数', '新评论数'])    

    ###################### 全部导出至excel文件 ######################
    x.to_excel('D:\\python\\work\\web\\other.xlsx',encoding='gbk', index=False,header=True)
    
        
    
        
