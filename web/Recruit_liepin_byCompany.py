# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 15:37:28 2021

@author: zengg
"""

import pandas as pd
# from bs4 import BeautifulSoup
import time
import random
from web.getSoup import getSoup

# n = 0
def get_liepin_byCompany(base_url, agents, company_list):
    table = pd.DataFrame(columns = ['职位', '薪水', '最低', '最高', '地区', '学历', '工作年限', '公司', '公司描述', '备注', '网址'])
    for i in company_list.keys():
        print ('============'+i+'============')
        n = 1
        while True:
            # i = '嘉实基金'
            url = base_url+company_list[i]+'/pn%s/'%n
            header_1 = {'user-agent': agents[random.randint(0,len(agents))], 'Connection':'keep-alive'} 
            soup = getSoup(url, header_1)
            
            t1 = soup.find('div', {'class': 'name-right'})
            comp_name = t1.find('span', {'data-selector': 'company-name'}).text.strip()
            comp_memo = t1.p.text.strip()
            
            t2 = soup.find('div', {'data-selector': 'pager-box'})
            t2_1 = t2.ul.find_all('li')
            for j in t2_1:
                # j = t2_1[0]
                job_title = j.find('a', {'.get_text().strip()
                
                
            
        # i = t[0]
        for i in t:
            try:
                job_info = i.find('div', {'class': 'job-info'})
                salary, area, edu, work_year = job_info.find('p', {'class': 'condition clearfix'}).get('title').split('_')
                job_title = job_info.h3.a.get_text().strip()
                ref = job_info.h3.a.get('href')
                
                comp_name = i.find('p', {'class': 'company-name'}).text.strip()
                comp_field = i.find('p', {'class': 'field-financing'}).text.strip()
                comp_memo = i.find('p', {'class': 'temptation clearfix'}).text.strip()
                
                # time.sleep(1)
                # header_2 = {'user-agent': agents[random.randint(0,len(agents))], 'Connection':'close'} 
                # soup2 = getSoup(ref, header_2)
                # content = soup2.find('div', {'class': 'content content-word'}).text.strip()
                
                table_i = [job_title,salary,'','',area, edu, work_year,comp_name,comp_field,comp_memo,ref]
                table.loc[len(table)] = table_i
                print (job_title+'|'+comp_name+'|'+salary)
                print ('------------------------')
            except:
                print ('读取失败，跳过')
                print ('------------------------')
    for j in range(len(table)):
        # j = 0
        if table['薪水'][j] == '面议':
            table['最低'][j] = '面议'
            table['最高'][j] = '面议'
        else:
           table['最低'][j] = table['薪水'][j][:table['薪水'][j].find('-')]+'k'
           table['最高'][j] = table['薪水'][j][table['薪水'][j].find('-')+1:]
    return table

    
if __name__ == '__main__':
    base_url = 'https://www.liepin.com/company-jobs/'
    company_list = {'嘉实基金': '8231620',
                     '国金证券': '4750556',
                     '安信证券': '8135788',
                     '中信证券': '9616987',
                     '天风证券': '6907566',
                     '中金公司': '4580900'}
    
    
    
    
    agents = ["Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"]
    
    x = get_liepin(base_url, agents, page_no)
    
    ###################### 全部导出至excel文件 ######################
    path = 'D:\\tools\\python\\python\\web\\liepin.xlsx'
    x.to_excel(path,index=False,header=True)
    
    import os
    os.system(path)
