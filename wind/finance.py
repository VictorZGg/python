# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:09:33 2021

@author: zengg
"""

import pandas as pd
from WindPy import w
import datetime as dt

w.start() 
w.isconnected()

# 获取全部A股
rtday = dt.datetime.today() - dt.timedelta(days=1) # 获取日期
rtday = rtday.strftime('%Y-%m-%d') # 转换日期格式

a_shares = w.wset("sectorconstituent","date="+rtday+";sectorid=a001010100000000")
sec_cde = a_shares.Data[1]
sec_name = a_shares.Data[2]
sec_info = dict(zip(sec_cde, sec_name))

# 设置报告日期
s_year = 2018
e_year = 2020

rpt_dates = []
y = range(s_year, e_year)
m = ['0331', '0630', '0930', '1231']
for i in y:
    for j in m:
        rpt_dates.append(str(i)+j)

# 分报告日期查询财务数据
table = pd.DataFrame()
for rpt_date in rpt_dates:
    print ('----------报告期'+rpt_date+'：正在查询'+'----------')
    rt_data = w.wss(sec_cde, "monetary_cap,tradable_fin_assets,acctandnotes_rcv","unit=1;rptDate="+rpt_date+";rptType=1")
    codes = rt_data.Codes
    names = []
    index = rt_data.Fields
    for i in codes:
        names.append(sec_info[i]) # 获取codes对应的证券名称
    # 建立表格table_i并录入数据
    table_i = pd.DataFrame()    
    for i in range(len(index)):
            table_j = pd.DataFrame({'sec_cde': codes,
                            'sec_name': names,
                            'rpt_date': rpt_date,
                            'index': index[i],
                            'amt': rt_data.Data[i]})  
            print ('+++指标：'+index[i]+'查询完毕+++')
            table_i = table_i.append(table_j)
    # 将table_i并入table
    print ('----------报告期'+rpt_date+'：查询完毕'+'----------')
    table = table.append(table_i)

# 画图

from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

x = table[table['rpt_date']=='20191231']


c = (
    Scatter()
    .add_xaxis(list(x['index']))
    .add_yaxis(
        "报告期：20191231",
        [list(z) for z in zip(list(x['amt']/100000000), list(x['sec_name']))],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                "function(params){return params.value[1] +' : '+ params.value[2];}"
            )
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Scatter-多维度数据"),
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode(
                "function (params) {return params.name + ' : ' + params.value[2];}"
            )
        ),
        visualmap_opts=opts.VisualMapOpts(
            type_="color", max_=150, min_=20, dimension=1
        ),
    )
    .render("D:\\ZG\\tools\\python\\windfinance_scatter.html")
)
 