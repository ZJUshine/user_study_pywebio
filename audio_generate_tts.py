'''
FilePath: audio_generate_tts.py
Author: zjushine
Date: 2023-04-09 17:22:17
LastEditors: zjushine
LastEditTime: 2023-04-11 14:23:44
Description: 根据语音内容生成语音问答对tts音频文件并保存
Copyright (c) 2023 by ${zjushine}, All Rights Reserved. 
'''

import pyttsx3

engine = pyttsx3.init()
# 根据chatpgt生成的一些语音助手的问答对
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
    "Remind me to call John at 3 pm": "Okay, I'll remind you to call John at 3 pm",
    "How many calories are in a slice of cheese pizza": "A typical slice of cheese pizza contains approximately 250-300 calories"
}

# 生成语音问答对音频文件
for ask,answer in commands.items():
    # 设置男声音色
    male_voice = engine.getProperty('voices')[0]
    engine.setProperty('voice', male_voice.id)
    
    # 生成问音频文件
    engine.say(ask)
    engine.runAndWait()
    engine.save_to_file(ask, f"./audio/ask/{ask}.mp3")

    # 设置女声音色
    female_voice = engine.getProperty('voices')[1]
    engine.setProperty('voice', female_voice.id)
    
    # 生成答音频文件
    engine.say(answer)
    engine.runAndWait()
    engine.save_to_file(answer, f"./audio/answer/{answer}.mp3")
