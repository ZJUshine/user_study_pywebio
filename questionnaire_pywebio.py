'''
FilePath: questionnaire_pywebio.py
Author: zjushine
Date: 2023-04-09 17:55:18
LastEditors: zjushine
LastEditTime: 2023-04-10 11:23:58
Description: 用pywebio实现一个语音助手的用户调查
Copyright (c) 2023 by ${zjushine}, All Rights Reserved. 
'''

from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import pywebio_battery
import pandas as pd
import librosa
import random
import numpy as np
import soundfile as sf
import os

# 语音助手的命令和回答
commands = {
    '你好': '你好啊！',
    '你叫什么名字': '我是一个语音助手，还没有名字呢。',
    '请告诉我现在的时间': '现在是2023年4月。',
    '请告诉我今天的天气': '今天的天气是晴天，最高温度为25摄氏度。',
    '请播放一首歌': '正在播放您的歌曲，请稍等片刻。',
    '请打开网页': '正在为您打开网页，请稍等片刻。',
    '请翻译一句话': '翻译结果为你好。',
    '请搜索一下教程': '正在为您搜索教程，请稍等片刻。',
    '请发一封邮件': '正在为您打开邮件客户端，请稍等片刻。',
    '请提醒我下午开会': '已为您设置下午开会的提醒。',
    '请关闭计算机': '正在为您关闭计算机，请稍等片刻。',
}

# 判断输入是否为负数
def check(number):
    if number < 0:
        return "不合法的输入"

# 判断输入是否为0或1
def check01(number):
    if number != 0 and number != 1:
        return "不合法的输入"

def survey():
    put_markdown("# User Study")
    put_text("感谢您参加本次调查，请回答以下问题：")
    xuehao = input("在这里填写你的学号：",type = NUMBER,help_text="便于后续发放奖励")
    shebei = input("填写你的智能音箱或语音助手",type = TEXT,help_text="例如siri、小爱同学、小度、小米AI音箱等")
    delay_time = input("请问您在使用智能音箱或语音助手时，感觉延迟多久？", type=NUMBER, help_text="请填写数字，单位为秒",validate = check)
    network_delay = select("请问您在使用智能音箱或语音助手时，通常网络卡顿的时候是几秒？", options=["1秒以内", "3秒以内", "5秒以内", "5-10秒"])
    put_markdown("以下是一些真实场景，请你考虑是否正常")
    normal = []
    delay_times = []
    for ask,answer in commands.items():
        audio1, sr1 = librosa.load(f"audio/ask/{ask}.mp3", sr=None, mono=True)
        audio2, sr2 = librosa.load(f"audio/answer/{answer}.mp3", sr=None, mono=True)
        # 生成随机长度的静音
        silence_length = random.randint(sr1, sr1 * 5)
        silence = np.zeros(silence_length, dtype=np.float32)
        result = np.concatenate([audio1, silence, audio2])
        # 保存音频文件
        sf.write("output.mp3", result, sr1)

        with open('output.mp3', 'rb') as f:
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
        df = pd.DataFrame(columns=["学号", "型号","延迟时间","网络卡顿",\
            "no0","delay_time0","no1","delay_time1","no2","delay_time2","no3","delay_time3",\
            "no4","delay_time4","no5","delay_time5","no6","delay_time6","no7","delay_time7"\
            ,"no8","delay_time8","no9","delay_time9","no10","delay_time10"])
    # 将信息存入表格的最后一行
    df.loc[len(df.index)] = [xuehao,shebei,delay_time,network_delay,\
        normal[0],delay_times[0],normal[1],delay_times[1],normal[2],delay_times[2],\
        normal[3],delay_times[3],normal[4],delay_times[4],normal[5],delay_times[5],\
        normal[6],delay_times[6],normal[7],delay_times[7],normal[8],delay_times[8],\
        normal[9],delay_times[9],normal[10],delay_times[10]]
    df.to_csv('questionnaire_result.csv',index=False)
    os.remove('output.mp3')
    # 显示感谢信息
    put_markdown("感谢您的参与！")

if __name__ == '__main__':
    start_server(survey, port=8080,debug=True)