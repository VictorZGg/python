# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:13:54 2021

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
    time.sleep(0.5)
    return soup

def getContent(url_1, kv, page_no):
    table = pd.DataFrame(columns=['用户', '微博', '赞', '转发', '评论', '时间', '来源'])
    for n in range(page_no):
        print ('==========='+'第'+str(n+1)+'页===========')
        m = str(n+1)
        url = url_1 + str(m)
        soup = getSoup(url, kv)
        # t = soup.find_all('span', {'class': 'ctt'})
        # y = soup.find_all('span', {'class': 'ct'})
        t = soup.find_all('div', {'class': 'c'})
        i = t[1]
        for i in t:
            if i.has_attr('id'):
                try:
                    content = i.find('span', {'class': 'ctt'}).text
                    for j in i.find_all('a'):
                        k = j.text
                        if '赞' in k:
                            upvote = int(k[(k.find('[')+1):k.find(']')])
                        elif '转发' in k:
                            tran = int(k[(k.find('[')+1):k.find(']')])
                        elif '评论' in k:
                            comment = int(k[(k.find('[')+1):k.find(']')])   
                        else:
                            pass
                    dtime1 = i.find('span', {'class': 'ct'}).text
                    dtime = dtime1[:dtime1.find('来自')-1]
                    source = dtime1[dtime1.find('来自'):]
                    table_i = ['', content, upvote, tran, comment, dtime, source]
                    table.loc[len(table)] = table_i
                    print (content)
                    print ('--------')
                except:
                    print ('运行出错，跳过，相关字段取空值或0')
                    print ('!!!!!!!!')
            else:
                pass
    return table


if __name__ == '__main__':
    cookie = '_T_WM=12085690677; SUB=_2A25NpxOvDeRhGedH6lsT8yjPyz6IHXVva73nrDV6PUJbktB-LRLskW1NUNsoCpNoauJBwlVz5liNLOLGe3LikQvZ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWWX2ah3lQN.wLSG4GXG0Qh5NHD95Qp1K24eoece05EWs4DqcjLi--ci-88iKnNi--Xi-zRiKy2i--Ri-zfi-zNi--NiKLWiKnXgntt; SSOLoginState=1621320703; WEIBOCN_FROM=1110105030; MLOGIN=1; XSRF-TOKEN=6a7182; M_WEIBOCN_PARAMS=luicode=10000011&lfid=1076037293883188&fid=1005057293883188&uicode=10000011'
    url_1 = 'https://weibo.cn/u/7293883188?page='
    # url_1 = 'https://weibo.cn/u/1642088277?page='
    kv = {'user-agent': 'Mozilla/5.0',
          'Connection':'close',
          # 'Connection':'keep-alive',
          'Cookie': cookie
          } 
    page_no = 10 # 设置查多少页
    # end_date = '01-01'# 设置最早日期
    ###################### 获取文件列表 ######################
    x = getContent(url_1, kv, page_no)
    path = 'D:\\tools\\python\\python\\web\\weibo.xlsx'
    x.to_excel(path,index=False,header=True)

    import os
    os.system(path) 




