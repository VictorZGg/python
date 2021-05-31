# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:49:01 2021

@author: zengg
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
import re
# import xlsxwriter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from web.getSoup import getSoup


def get_Ashares():
    kv = {'user-agent': 'Mozilla/5.0', 'Connection':'close'}     
    path = 'D:\\ZG\\tools\\python\\python\\web'
    print ('==================获取沪市A股==================')    
    url_h = "http://www.sse.com.cn/assortment/stock/list/share/"
    xpath_1 = '//div[@class="sse_table_title2"]//a[text()="下载"]'
    
    # 0禁止弹出下载窗口
    # download.default_directory设置下载路径
    opt = webdriver.ChromeOptions()
    prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": path}
    opt.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get("http://www.sse.com.cn/assortment/stock/list/share/")
    WebDriverWait(driver,5,0.2).until(lambda x:x.find_element_by_xpath(xpath_1)).text
    driver.find_elements_by_xpath(xpath_1)[0].click()
    table_h_1 = pd.read_csv(path+'\\主板A股.csv')
  
    driver.quit()
    
    
    import os
    os.system(path+'\\主板A股.xls')
    
    
    
    
    
    
    
    
    
    
    soup = getSoup(url_h, kv)
    t = soup.find('a', {'class': 'download-export js_download-export'}).p.a
    
    
    
    page_no = 10
    






