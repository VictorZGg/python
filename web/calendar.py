# -*- coding: utf-8 -*-
"""
Created on Wed May 26 14:15:24 2021

@author: zengg
"""


import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def calendarDisplay(url, month_count):
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
    
    path_1 = '//div[@class="calHeaderTop"]//span[text()="月历"]'   
    path_2 = '//div[@class="calendar__monthbar"]//a[@class="calendar__month-item"]'
    path_3 = '//div[@class="calendar__monthbar"]//a[@class="calendar__month-next"]'
    
    # 等待页面出现相关元素
    WebDriverWait(driver,5,0.2).until(lambda x:x.find_element_by_xpath('//*[text()="月历"]')).text
    
    driver.find_elements_by_xpath(path_1)[0].click()
    time.sleep(3)
    table = pd.DataFrame(columns=['日期', '时间', '国家', '内容'])
    m = 0
    page_count = 1
    
    while page_count <= month_count:
        # 向下滚动屏幕
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(2)
        # 等待页面出现相关元素
        # driver.implicitly_wait(30)
        WebDriverWait(driver,5,0.2).until(lambda x:x.find_element_by_xpath('//*[@class="month-table__month"]')).text       
        # 获取页面源代码
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser") 
        month_date = soup.find('div', {'class': 'month-table__month'}).text.strip()
        print (month_date)
        print ('=====================')
        
        t = soup.find_all('div', {'class': 'col-container'})
        # i = t[1]
        for i in t:
            try:
                day_date = str(int(i.find('div', {'class': 'col-date'}).text.strip()))
                ddate = month_date+day_date+'日'
                try:
                    t2 = i.find_all('div', {'class': 'col-event'})
                    # j = t2[0]
                    for j in t2:
                        dtime = j.find('span', {'class': 'event-time'}).text.strip()
                        country = j.find('span', {'class': 'event-country'}).text.strip()
                        title = j.find('div', {'class': 'event-title'}).text.strip()
                        table_i = [ddate, dtime, country, title]
                        table.loc[len(table)] = table_i
                        print(ddate+dtime+'|'+country+'|'+title)
                        print ('------------------')
                except:
                    table_i = [month_date, day_date, '', '', '']
                    table.loc[len(table)] = table_i
                    print(ddate+'|'+'无事件')
                    print ('------------------')
            except:
                print ('------------------')
        # 进入下一个月
        driver.execute_script('window.scrollBy(0,-1000)')
        time.sleep(2)
        try:
            driver.find_elements_by_xpath(path_2)[m].click()
            m += 1
        except:
            driver.find_elements_by_xpath(path_3)[0].click()
            m = 0
            driver.find_elements_by_xpath(path_2)[m].click()
        time.sleep(2)
        page_count += 1
    driver.quit()
    return table

def calendarAnalysis(table):
    dict = {''}


if __name__ == '__main__':
    url = 'https://wallstreetcn.com/calendar'
    month_count = 5
    x = calendarDisplay(url, month_count)

    ###################### 全部导出至excel文件 ######################
    path = 'D:\\tools\\python\\python\\web\\calendar_display.xlsx'
    x.to_excel(path,index=False,header=True)
    
    import os
    os.system(path)
    



















