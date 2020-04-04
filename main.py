import telepot
from Chatbot import Chatbot

telegram = telepot.Bot('1244173096:AAERbU6DN31LgxX2HKK961Os1NetLKCy-Po')

bot = Chatbot('C0r0n4Bot')

def receiveMsg(msg):
    print(msg['text'])
    ans = bot.send(text = msg['text'])
    typeMsg, typeChat, chatID = telepot.glance(msg)
    telegram.sendMessage(chatID, ans)

telegram.message_loop(receiveMsg)

while True:
    pass