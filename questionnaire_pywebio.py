'''
FilePath: questionnaire_pywebio.py
Author: zjushine
Date: 2023-04-09 17:55:18
LastEditors: zjushine
LastEditTime: 2023-04-11 15:07:20
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
from flask import request
# 语音助手的命令和回答
commands = {
    "What's the weather like today": "The weather today is partly cloudy with a high of 72 degrees Fahrenheit and a low of 60 degrees Fahrenheit",
    "Set a timer for 10 minutes": "Okay, I've set a timer for 10 minutes. Your timer will go off in 10 minutes",
    "Play some music": "Sure, here is a curated playlist for you to enjoy",
    "What's on my calendar for today": "You have a meeting with John at 2 pm and a dentist appointment at 4 pm",
    "What's the latest news": "Here are the top headlines",
    "How do I get to the nearest gas station": "According to your location, the nearest gas station is 2 miles away. Would you like me to give you directions",
    "What's the definition of 'serendipity'": "Serendipity means the occurrence and development of events by chance in a happy or beneficial way",
    "What's the exchange rate between USD and EUR": "The current exchange rate between USD and EUR is 0.83",
    "What's the population of New York City": "According to the latest census data, the population of New York City is approximately 8.4 million",
    "Remind me to call John at 3 pm": "Okay, I'll remind you to call John at 3 pm"
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
    forwarded_ips = request.headers.getlist("X-Forwarded-For")
    ip = forwarded_ips[0] if forwarded_ips else None
    clear()
    shebei = input("填写你的智能音箱或语音助手",type = TEXT,help_text="例如siri、小爱同学、小度、小米AI音箱等")
    delay_time = input("请问您在使用智能音箱或语音助手时，感觉延迟多久？", type=NUMBER, help_text="请填写数字，单位为秒",validate = check)
    network_delay = select("请问您在使用智能音箱或语音助手时，通常网络卡顿的时候是几秒？", options=["1秒以内", "3秒以内", "5秒以内", "5-10秒"])
    
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
        sf.write(f"output{ip}.mp3", result, sr1)

        with open(f'output{ip}.mp3', 'rb') as f:
            audio_data = f.read()
        # 展示音频
        put_markdown("以下是一些真实场景，请你考虑是否正常")
        put_markdown("# Ask")
        put_text(ask)
        put_markdown("# Answer")
        put_text(answer)
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
            ,"no8","delay_time8","no9","delay_time9"])
    # 将信息存入表格的最后一行
    df.loc[len(df.index)] = [ip,shebei,delay_time,network_delay,\
        normal[0],delay_times[0],normal[1],delay_times[1],normal[2],delay_times[2],\
        normal[3],delay_times[3],normal[4],delay_times[4],normal[5],delay_times[5],\
        normal[6],delay_times[6],normal[7],delay_times[7],normal[8],delay_times[8],\
        normal[9],delay_times[9]]
    df.to_csv('questionnaire_result.csv',index=False)
    os.remove(f'output{ip}.mp3')
    # 显示感谢信息
    put_markdown("# 感谢您的参与！")
    put_text("以下是奖励，请您扫码领取")
    img = open('reward.png', 'rb').read()  
    put_image(img)

if __name__ == '__main__':
    start_server(survey, port=8080,debug=True)