# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:34:52 2021

@author: zengg
"""

import pandas as pd
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from web.getSoup import getSoup









header = {'user-agent': 'Mozilla/5.0', 'Connection':'close'} 

soup = getSoup(url, header)



def get_h_FinancialReport(sec_list, year, header):
    
    sec_list_h = sec_list[sec_list['mkt_sort']=='h']
    sec_list_h = sec_list_h.reset_index()
    
    # 获取chrome的配置
    opt = webdriver.ChromeOptions()
    # 在运行的时候不弹出浏览器窗口
    # opt.set_headless()
    # 获取driver对象
    driver = webdriver.Chrome(chrome_options = opt)
    
    for i in range(len(sec_list_h)):
        sec_id = str(sec_list_h['sec_cde'][i])
        sec_abbr = str(sec_list_h['sec_name'][i])
        url = 'http://listxbrl.sse.com.cn/companyInfo/toCompanyInfo.do?\
            stock_id=%s.SS&report_year=%s&report_period_id=5000'%(sec_id, str(year))        

        # 打开登录页面
        driver.get(url)
        # path_0 = '//div[@class="main_search"]//input[@value="请输入股票代码或简称"]'
        
        report_names = ['资产负债表', '利润表', '现金流量表']
        for j in report_names:
            path_1 = '//div[@class="main_content"]//a[text()="%s"]'%(j)
            # driver.find_elements_by_xpath(path_0)[0].clear()
            #driver.find_elements_by_xpath(path_0)[0].send_keys('600001')
            driver.find_elements_by_xpath(path_1)[0].click()
 
            # 获取页面源代码
            html_source = driver.page_source
            x = BeautifulSoup(html_source, "html.parser")
            t = 
        

    
if __name__ == '__main__':
    sec_list = pd.read_excel('D:\\tools\\python\\python\\wind\\sec_list.xlsx', sheet_name='Sheet1')
    year = '2020'
