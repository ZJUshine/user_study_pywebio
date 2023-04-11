'''
FilePath: template_pywebio.py
Author: zjushine
Date: 2023-04-11 14:41:03
LastEditors: zjushine
LastEditTime: 2023-04-11 14:54:47
Description: 
Copyright (c) 2023 by ${zjushine}, All Rights Reserved. 
'''

from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import pywebio_battery
import pandas as pd
import os

# 判断输入是否为不合法收入
def check(number):
    if number < 0:
        return "不合法的输入"

def survey():
    # markdown语法
    put_markdown("# User Study")
    # 输出文本
    put_text("感谢您参加本次调查，请回答以下问题：")
    # input用来输入NUMBER/TEXT等数据 输入信息存在xuehao中
    xuehao = input("在这里填写你的学号：",type = NUMBER,help_text="便于后续发放奖励")
    # clear用来清除页面
    clear()
    shebei = input("填写你的智能音箱或语音助手",type = TEXT,help_text="例如siri、小爱同学、小度、小米AI音箱等")
    delay_time = input("请问您在使用智能音箱或语音助手时，感觉延迟多久？", type=NUMBER, help_text="请填写数字，单位为秒",validate = check)
    # select用来选择选项 options为选项列表 结果存在network_delay中
    network_delay = select("请问您在使用智能音箱或语音助手时，通常网络卡顿的时候是几秒？", options=["1秒以内", "3秒以内", "5秒以内", "5-10秒"])
    
    with open("path", 'rb') as f:
        audio_data = f.read()
        # 展示音频
        pywebio_battery.put_audio(audio_data)
        no = input("请问你认为这个回答延时是否正常？", type=NUMBER, help_text="0正常，1不正常",validate = check01)
        # 计算延迟时间
        delay_times.append(silence_length/sr1)
        normal.append(no)
        clear()
    if os.path.exists("questionnaire_result.csv"):
        df = pd.read_csv("questionnaire_result.csv",header=None)
    else:
        # 创建一个表格存储信息
        df = pd.DataFrame(columns=["学号", "型号","延迟时间","网络卡顿"])
    # 将信息存入表格的最后一行
    df.loc[len(df.index)] = [xuehao,shebei,delay_time,network_delay]
    df.to_csv('questionnaire_result.csv',index=False)
    # 显示感谢信息
    put_markdown("# 感谢您的参与！")
    put_text("以下是奖励，请您扫码领取")
    # 展示图片
    img = open('reward.png', 'rb').read()  
    put_image(img)

if __name__ == '__main__':
    # 在8080端口启动服务
    start_server(survey, port=8080,debug=True)