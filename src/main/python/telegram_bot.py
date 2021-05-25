import telegram
import sys
import os
TOKEN = '1816846800:AAHstd6mrvJZxKLXi_0ucXCA4P0OoWDx2zY'
CHAT_ID = -1001445808075

def send_message():
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = 'Hey there!')
    
send_message()