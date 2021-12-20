# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 20:45:27 2021

@author: Administrator
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
import urllib3
urllib3.disable_warnings()
from selenium import webdriver


url = 'http://www.csrc.gov.cn/csrc/c101971/zfxxgk_zdgk.shtml'

opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options = opt)
driver.maximize_window()
driver.get(url)
time.sleep(3)

source_html = driver.page_source
x = BeautifulSoup(source_html, "html.parser")
t = x.find('div', {'id': 'codeId_list'}).ul.table.tbody.find_all('tr')

head_list = []
for i in t[0].find_all('th'):
    head_list.append(i.text)
head_list.append('url')
table = pd.DataFrame(columns=head_list)
head_len = len(head_list)

path_1 = '//div[@id="page_div"]/a[@class="nextbtn"]'
# 下一页
# driver.find_elements_by_xpath(path_1)[0].click()
# 上一页
# path_2 = '//div[@id="page_div"]/a[@class="prebtn"]'
# driver.find_elements_by_xpath(path_2)[0].click()

page_no = 1
total_page = x.find('div', {'id': 'page_div'}).b.text

while page_no <= int(total_page):
    print ('=============='+str(page_no)+' / '+total_page+' 页'+'===============')
    source_html_i = driver.page_source
    x_i = BeautifulSoup(source_html_i, "html.parser")
    body_i = x.find('div', {'id': 'codeId_list'}).ul.table.tbody.find_all('tr')[1:]
    for i in body_i:
        j = i.find_all('td')
        body_list = []
        for k in range(head_len-1):
            body_list.append(j[k].text)
        ref = j[1].a.attrs['href']
        body_list.append(ref)
        table.loc[len(table)] = body_list
    driver.find_elements_by_xpath(path_1)[0].click()
    time.sleep(1)
    page_no += 1

driver.quit()


###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\zjh\\zjh_enforcement.xlsx'
table.to_excel(path,index=False,header=True)










