import telebot
from telebot import types
from random import randint
from datetime import datetime

token = "5257020489:AAEYW436khopoS-QtyQRN3aJDAmYppOESLY"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Новости", "Расписание", "Погода", "Какой сегодня день?", "/eu", "/help", "/roll")
    bot.send_message(message.chat.id, "Привет! Что бы ты хотел узнать?", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'roll - случайное число от 1 до 6 \neu - вход в электронный университет \nhelp - описание команд')

@bot.message_handler(commands=['roll'])
def roll(message):
    bot.send_message(message.chat.id, randint(1,6))

@bot.message_handler(commands=['eu'])
def eu(message):
    bot.send_message(message.chat.id, "https://lms.mtuci.ru/lms/login/index.php")

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "новости":
        bot.send_message(message.chat.id, "Тогда тебе сюда https://mtuci.ru/")
    if message.text.lower() == "расписание":
        bot.send_message(message.chat.id, "Тогда тебе сюда https://mtuci.ru/time-table/")
    if message.text.lower() == "погода":
        bot.send_message(message.chat.id, "Тогда тебе сюда https://gismeteo.ru")
    if message.text.lower() == "какой сегодня день?":
        bot.send_message(message.chat.id, datetime.now().date())

bot.infinity_polling()