# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 21:22:38 2021

@author: Administrator
"""


import pyautogui
from datetime import datetime
# 阻塞当前进程的调整器
from apscheduler.schedulers.blocking import BlockingScheduler
# blocking类型调度器会阻塞当前进程，若你想要后台运行的调度器，可以使用以下代码：
# from apscheduler.schedulers.background import BackgroundScheduler

def main():
    pyautogui.PAUSE = 1 # 设置每一步操作的间隔（秒），可防止操作太快
    
    # 然后我们登录微信，最小化。
    # 接下来我们把鼠标放到微信的任务栏图标上，运行以下语句，获取此时光标的坐标，返回一个Point对象：
    # print(pyautogui.position()) # 打印坐标，Point(x=286, y=1065)
    # icon_position = pyautogui.position() # Point(x=286, y=1065)
    icon_position = pyautogui.position(x=286, y=1065)
    
    # 打开微信，选择回话窗口，将鼠标放在输入框上，同样获取光标坐标，为了将焦点锁定到输入框以方便待会的输入
    # print(pyautogui.position()) # 打印坐标，Point(x=978, y=764)
    # entry_position = pyautogui.position() # Point(x=978, y=764)
    entry_position = pyautogui.position(x=978, y=764) # Point(x=978, y=764)
    
    # 分别控制程序点击两个点
    pyautogui.click(icon_position) # 默认左键单击
    pyautogui.click(entry_position)
    
    # 输入文本
    # pyautogui.typewrite(['o', 'n', 'e', 'enter'])
    # pyautogui.typewrite('You can type multiple letters in this way')
    pyautogui.typewrite([*list('zhengzai '), *list('jinxing '), *list('weixinzidongfasong'), *list('shiyan '), ',', '2021-08-29 21:51', *list('zhunshifasong '), 'enter'], 0.1) # 第一个参数是输入文本，第二个是输入每个字符的间隔时间
    
    # 移动鼠标的代码，可视化强
    # pyautogui.moveTo(icon_position, duration=2) # duration为执行时长，可选
    # pyautogui.click(icon_position)
    # pyautogui.moveTo(entry_position, duration=2)
    # pyautogui.click(entry_position)
    # pyautogui.typewrite([*list('zhengzai '), *list('jinxing '), 'shift', *list('pyautogui'), 'shift', *list('shiyan '), 'enter'], 0.1) # 第二个参数为按下每一个字母的间隔，可选

    # 复制操作
    # pyautogui.click(entry_position)
    # pyperclip.copy('快去睡觉')
    # pyautogui.hotkey('ctrl', 'v')
    # pyautogui.press('enter')


##### 设定定时任务
scheduler = BlockingScheduler() # 实例化一个调度器
scheduler.add_job(main, 'date', run_date=datetime(2021, 8, 29, 21, 51, 00)) # 添加任务
scheduler.start()







