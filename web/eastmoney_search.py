# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:51:31 2021

@author: zengg
"""


import pandas as pd
from bs4 import BeautifulSoup
import time
import re
# import xlsxwriter
from selenium import webdriver
from web.getSoup import getSoup


def eastmoneySearch(url, page_no, kv, key_word):
    # 获取chrome的配置
    opt = webdriver.ChromeOptions()
    # 在运行的时候不弹出浏览器窗口
    # opt.set_headless()
    # 获取driver对象
    driver = webdriver.Chrome(chrome_options = opt)
    # 打开登录页面
    driver.get(url)
    # 设置等待时间为10s，超时则会报错
    # wait = WebDriverWait(browser,10)
    # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#inp-query')))
    
    path_1 = '//div[@class="main_body clearfix"]/div[@class="seach_header"]//li[@id="2"]'
    path_2 = '//div[@class="main_body clearfix"]/div[@class="seach_header"]//input[@placeholder="请输入关键字"]'
    # path_3 = '//div[@class="main_body clearfix"]/div[@class="seach_header"]//input[@value="股吧搜索"]'
    path_3 = '//a[text()="按时间排序"]'
    path_4 = '//a[text()=">"]'
    
    driver.find_elements_by_xpath(path_1)[0].click()
    driver.find_elements_by_xpath(path_2)[0].send_keys(key_word)
    driver.find_elements_by_xpath(path_2)[0].submit()
    # driver.find_elements_by_xpath(path_3)[0].click()
    # 获取当前页句柄
    n = driver.window_handles
    driver.switch_to.window (n[1])
    print (driver.current_url)
    driver.find_elements_by_xpath(path_3)[0].click()
    
    table = pd.DataFrame(columns=['证券', '标题', '内容', '发布时间', '阅读','转发','评论','点赞','链接'])
    m = 1
    while m <= page_no:
        try:
            print ('第'+str(m)+'页')
            print ('==============')
            time.sleep(1)
            # 获取页面源代码
            html_source = driver.page_source
            # html = lxml.html.fromstring(html_source)
            x = BeautifulSoup(html_source, "html.parser")
            t = x.find('div', {'class': 'article_list'}).find_all('div', {'class': 'article_item'})
            # i = t[0]
            for i in t:
                try:
                    sec = i.find('div', {'class': 'article_title'}).span.text
                    title = i.find('div', {'class': 'article_title'}).a.text
                    ref = i.find('div', {'class': 'article_title'}).a.get('href')
                    dtime = i.find('div', {'class': 'article_content'}).label.text
                    content = i.find('div', {'class': 'article_content'}).span.text
                    soup = getSoup(ref, kv)
                    
                    n_list = []
                    name_list = ['click','forward','comment','like']
                    
                    for i in name_list:
                        p = '"post_'+i+'_count":[0-9]*?,'
                        pattern = re.compile(p)
                        ret = pattern.search(str(soup)).group()
                        n_list.append(int(ret[ret.find(':')+1:-1]))
                    click, forward, comment, like = n_list                                    
                    table_i = [sec, title, content, dtime, click, forward, comment, like, ref]
                    table.loc[len(table)] = table_i
                    print (dtime+'|'+sec+'|'+title)
                    print ('----------------')
                except:
                    print ('运行出错，跳过')
                    print ('----------------')
        except:
            print ('运行出错，跳过本页')
            print ('----------------')
        driver.find_elements_by_xpath(path_4)[0].click()
        time.sleep(1)
        m+=1
    driver.quit()
    return table

if __name__ == '__main__':
    url = "https://guba.eastmoney.com/"
    page_no = 10
    kv = {'user-agent': 'Mozilla/5.0', 'Connection':'close'} 
    key_word ='许亚飞'
    x = eastmoneySearch(url, page_no, kv, key_word)

    ###################### 全部导出至excel文件 ######################
    path = 'D:\\tools\\python\\python\\web\\eastmoney_search_%s.xlsx'%(key_word)
    x.to_excel(path,index=False,header=True)
    
    import os
    os.system(path)

