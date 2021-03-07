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
    #time.sleep(0.1)
    return soup

def getContent(url_1, kv, ups , up_list, max_page):
    table = pd.DataFrame(columns=['吧名', '作者', '标题', '阅读量', '评论量', '发布时间', '最新评论时间', '链接'])
    for up in ups:
        code = up_list[up]
        print ('up主：'+up)
        n = 0
        while n <= max_page:
            print ('==========='+'第'+str(n+1)+'页===========')
            m = str(n+1)
            url = url_1+code+'/video?tid=0&page='+m+'&keyword=&order=pubdate'
            soup = getSoup(url, kv)
            t = soup.find('div', {'id': 'submit-video-list'}).find_all('li')        
            for i in t:
                try:
                    j = i.find_all('cite')
                    read = j[0].text
                    comments = j[1].text
                    name = j[2].text
                    pub_time = j[3].text
                    last_time = j[4].text
                    k = i.find('span').find_all('a')
                    sec = k[0].text
                    # sec_ref = 'https://guba.eastmoney.com/' + k[0].get('href')
                    title = k[1].text
                    ref = 'https://guba.eastmoney.com/' + k[1].get('href')
                    table_i = [sec, name, title, read, comments, pub_time, last_time, ref]
                    table.loc[len(table)] = table_i
                    print (title)
                    print ('--------')
                except:
                    print ('运行出错，跳过，相关字段取空值或0')
                    sec, name, title, pub_time, last_time, ref = ['']*6
                    read, comments = [0]*2
            if  int(table_i[5][:2]) <= int(end_date[:2]) and int(table_i[5][3:5]) < int(end_date[3:5]):
                print ('===========到达指定日期：' + end_date + '，结束===========')
                break
        return table

def getUplist():
    up_list = {'泛式': '63231'
            }
    return up_list


up = ups[0]

if __name__ == '__main__':
    url_1 = 'https://space.bilibili.com/'
    kv = {'user-agent': 'Mozilla/5.0',
          'Connection':'close'} 
    
    ups = ['泛式']
    up_list = getUplist()
    max_page = 10 # 设置查多少页
    end_date = '01-01'# 设置最早日期
    ###################### 获取文件列表 ######################
    x = getContent(url_1, kv, page_no, end_date)
    
    for i in range(len(x)):
        x.loc[i, '阅读量'] = x.loc[i, '阅读量'].replace(' ', '')
        x.loc[i, '评论量'] = x.loc[i, '评论量'].replace(' ', '')
    
    x['阅读量'] = x['阅读量'].astype('int')
    x['评论量'] = x['评论量'].astype('int')
    x = x.sort_values(axis = 0, ascending = False, by=['阅读量', '评论量'])   
    
#    
#    from pyecharts import options as opts
#    from pyecharts.charts import Scatter
#    from pyecharts.commons.utils import JsCode
#
#
#    c = (
#        Scatter()
#        .add_xaxis(list(x['发布时间']))
#        .add_yaxis(
#            "股吧阅读量分布",
#            [list(z) for z in zip(list(x['阅读量']), list(x['作者']))],
#            label_opts=opts.LabelOpts(
#                formatter=JsCode(
#                    "function(params){return params.value[1] +' : '+ params.value[2];}"
#                )
#            ),
#        )
#        .set_global_opts(
#            title_opts=opts.TitleOpts(title="Scatter-多维度数据"),
#            tooltip_opts=opts.TooltipOpts(
#                formatter=JsCode(
#                    "function (params) {return params.name + ' : ' + params.value[2];}"
#                )
#            ),
#            visualmap_opts=opts.VisualMapOpts(
#                type_="color", max_=150, min_=20, dimension=1
#            ),
#        )
#        .render("D:\\python\work\\\web\\eastmoney_heat_scatter.html")
#    )
#     
#    
    
    
    
    

    ###################### 全部导出至excel文件 ######################
    x.to_excel('D:\\python\work\\\web\\eastmoney_heat.xlsx',index=False,header=True)
    

    
        
    
        
