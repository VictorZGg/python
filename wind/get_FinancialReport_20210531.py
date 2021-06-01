# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:34:52 2021

@author: zengg
"""

import pandas as pd
import urllib
import time
import os

def get_h_FinancialReport(sec_list):  
    for i in range(len(sec_list)):
        sec_id = sec_list['sec_cde'][i]
        sec_id = ('000000'+str(sec_id))[-6:]
        sec_abbr = sec_list['sec_name'][i]
        path = 'D:\\tools\\python\\python\\wind\\financial_reports\\'+sec_id+'_lrb.csv'
        if os.path.exists(path):
            print ('存在重名文件，跳过证券：%s'%sec_id)
            pass
        else:
            # sec_abbr = str(sec_list['sec_name'][i])
            url = 'http://quotes.money.163.com/service/lrb_'+sec_id+'.html'
            while True:
                try:
                    content = urllib.request.urlopen(url,timeout=2).read()
                    print(sec_id+'  |  '+sec_abbr)
                    print('--------------')
                    with open('D:\\tools\\python\\python\\wind\\financial_reports\\'+sec_id+'_lrb.csv','wb') as f:
                        f.write(content)
                    time.sleep(1)
                    break
                except Exception as e:
                    if str(e) =='HTTP Error 404: Not Found':
                        break
                    else:
                        print(e)
                        continue


if __name__ == '__main__':
    sec_list = pd.read_excel('D:\\tools\\python\\python\\wind\\sec_list.xlsx', sheet_name='Sheet1')
    get_h_FinancialReport(sec_list)
