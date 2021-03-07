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

def getContent(url_1, kv, page_no):
    table = pd.DataFrame(columns=['名称','链接','发布时间','评论数','浏览数'])
    for n in range(page_no):
        print ('==========='+'第'+str(n+1)+'页===========')
        m = str(n+1)
        url = url_1+m+'.html'
        soup = getSoup(url, kv)
        t = soup.find_all('th', {'class': ['common', 'new']})
        for i in t:
            j = i.find('a', {'class': 's xst'})
            content = j.text
            ref = 'https://www.deepfun.net/' + j.get('href')
            
            k = i.find('div', {'class': 'deanfby1'}).span
            pub_time = k.text
            
            l = i.find('div', {'class': 'deanfnums'})
            comments = l.a.text
            views = l.em.text
            
            table_i = [content, ref, pub_time, comments, views]
            table.loc[len(table)] = table_i
            print (content)
    return table

n = 1
if __name__ == '__main__':
    url_1 = 'https://www.deepfun.net/forum-36-'
    kv = {'user-agent': 'Mozilla/5.0',
          'Connection':'close'}
    page_no = 20 # 设置查多少页
    ###################### 获取文件列表 ######################
    x = getContent(url_1, kv, page_no)
    
    x['评论数'] = x['评论数'].astype('int')
    x['浏览数'] = x['浏览数'].astype('int')
    x = x.sort_values(axis = 0, ascending = False, by=['评论数', '浏览数'])    

    ###################### 全部导出至excel文件 ######################
    x.to_excel('ns_game.xlsx',index=False,header=True)
    
        
    
        
