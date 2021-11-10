# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 20:45:27 2021

@author: Administrator
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
# import re
import time
# import datetime as dt
import urllib3
urllib3.disable_warnings()
# from selenium import webdriver
# import xlsxwriter
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


url = 'https://gs.amac.org.cn/amac-infodisc/res/pof/person/personOrgList.html'
# 获取chrome的配置
opt = webdriver.ChromeOptions()
# 在运行的时候不弹出浏览器窗口
# opt.set_headless()
# 获取driver对象
driver = webdriver.Chrome(chrome_options = opt)
# 打开登录页面
# driver.set_window_size(1920, 1080)  # choose a resolution big enough
driver.maximize_window()
driver.get(url)
# 设置等待时间为10s，超时则会报错
time.sleep(3)
# wait = WebDriverWait(browser,10)
# input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#inp-query')))
path_1 = '//div[@class="dropdown"]/div[@class="dropselectbox"]'
#driver.find_elements_by_xpath(path_1)[0].click()
kw = driver.find_elements_by_xpath(path_1)[0]
x = kw.location.get('x')
y = kw.location.get('y')
ActionChains(driver).move_by_offset(x+200, y+30).click().perform()
time.sleep(2)
ActionChains(driver).move_by_offset(0, 260).click().perform()

path_2 = '//div[@class="query-btn button"]'
driver.find_elements_by_xpath(path_2)[0].click()

s1 = Select(driver.find_element_by_name('dvccFundList_length'))
s1.select_by_value('100')
time.sleep(3)
# s1 = Select(driver.find_element_by_id('orgType'))
# s1.select_by_value('smjjglr')

# for select in s1.options:
#     print (select.text)

source_html = driver.page_source
# print(driver.get_cookies())
# session = requests.Session()

x = BeautifulSoup(source_html, "html.parser")
t = x.find('div', {'id': 'dvccFundList_info'}).text
total_page = t[-4:-1]
page_no = 1

head = x.find('tr', {'id':'personColumns'}).find_all('th')
head_list = []
for i in head:
    head_list.append(i.text) 
head_list.append('url')
table = pd.DataFrame(columns=head_list)

while page_no <= int(total_page):
    print ('=============='+str(page_no)+' / '+total_page+' 页'+'===============')
    source_html_i = driver.page_source
    x_i = BeautifulSoup(source_html_i, "html.parser")
    body_i = x_i.find('table', {'id':'dvccFundList'}).find('tbody').find_all('tr', {'role':'row'})
    for i in body_i:
        j = i.find_all('td')
        body_list = []
        k = 0
        while k < 5:
            body_list.append(j[k].text)
            k += 1
        ref = 'https://gs.amac.org.cn/amac-infodisc/res/pof/person/'+j[1].a.attrs['href']
        body_list.append(ref)
        table.loc[len(table)] = body_list
    path_i = '//a[@class="paginate_button next"]'
    driver.find_elements_by_xpath(path_i)[0].click()
    time.sleep(1)
    page_no += 1

driver.quit()

###################### 全部导出至excel文件 ######################
path = 'D:\\tools\\python\\python\\web\\fund_member_private.xlsx'
table.to_excel(path,index=False,header=True)

#headers = {
#    'Accept': 'application/json,text/javascript,*/*; q=0.01',
#    'Accept-Encoding': 'gzip,deflate',
#    'Connection': 'keep-alive',
#    'Host': 'gs.amac.org.cn',
#    'Content-Type': 'application/json;charset=UTF-8',
#    'Origin': 'http://gs.amac.org.cn',
#    'X-Requested-With': 'XMLHttpRequest',
#    'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
#    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'
#}












