'''
FilePath: audio_generate_tts.py
Author: zjushine
Date: 2023-04-09 17:22:17
LastEditors: zjushine
LastEditTime: 2023-04-10 10:53:02
Description: 根据语音内容生成语音问答对tts音频文件并保存
Copyright (c) 2023 by ${zjushine}, All Rights Reserved. 
'''

import pyttsx3

engine = pyttsx3.init()

# 根据chatpgt生成的一些语音助手的问答对
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
    '退出': '再见！'
}

# 生成语音问答对音频文件
for ask,answer in commands.items():
    # 生成问音频文件
    engine.say(ask)
    engine.runAndWait()
    engine.save_to_file(ask, f"./ask/{ask}.mp3")
    # 生成答音频文件
    engine.say(answer)
    engine.runAndWait()
    engine.save_to_file(answer, f"./answer/{answer}.mp3")
