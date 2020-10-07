import telepot
from Chatbot import Chatbot

keySecret = '1244173096:AAERbU6DN31LgxX2HKK961Os1NetLKCy-Po'
telegram = telepot.Bot(keySecret)

bot = Chatbot('C0r0n4Bot')

def receiveMsg(msg):
    ans = bot.send(text = msg['text'])
    typeMsg, typeChat, chatID = telepot.glance(msg)
    telegram.sendMessage(chatID, ans)

telegram.message_loop(receiveMsg)

while True:
    pass
