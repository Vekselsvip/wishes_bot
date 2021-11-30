import telebot
from config import *
import time
from flask import Flask, request
import os


app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

with open('wishes.txt', encoding='utf-8') as file:
    wishes = [item.split('\n') for item in file]
sti = open('stick/sticker.webp', 'rb')



@bot.message_handler(commands='start')
def start_message(message):
    bot.send_message(message.chat.id, START)


@bot.message_handler(commands='sleep')
def sleep_message(message):
    for i in wishes:
        bot.send_message(message.chat.id, f'<i>{i[0]}</i>', parse_mode='HTML')
        bot.send_sticker(message.chat.id, sti)
        time.sleep(3)


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 25-11-2022", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://wishes-bot.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
