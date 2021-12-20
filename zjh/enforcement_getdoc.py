# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:26:39 2021

@author: zengg
"""

import pandas as pd
from docx import Document
from docx.oxml.ns import qn
import os
print (os.getcwd())
os.chdir('D:\\tools\\python\\python\\zjh')


origin_table = pd.read_excel(io = 'enforcement_table.xlsx')
table_len = len(origin_table)
# i = 0
doc = Document()
doc_cnt = 1

for i in range(table_len):
    print ('=========== 进度：'+str(round((i+1)/table_len*100,2))+'% ===========')
    table_i = origin_table.loc[i]
    run = doc.add_heading('',level=1).add_run(table_i['发文日期']+'——'+table_i['名称'])
    # run.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run.font.name=u'宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体') 
    doc.styles['Normal'].font.name = u'仿宋'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋')
    p = doc.add_paragraph('发文日期：'+table_i['发文日期'])
    # p.add_run('文号：'+report.loc[1,'文号'])
    p.add_run(table_i['内容'])
    if cnt == 100:
        doc.save('zjh_enforcement'+.docx')#保存到工程目录下
    print ('----------文件导出完毕--------------')

    
        
    
        
