import telebot
from telebot import types
from random import randint
from datetime import datetime
import requests

token = "5257020489:AAEYW436khopoS-QtyQRN3aJDAmYppOESLY"

city = None
appid = 'ae97c65bf76cef416ac3b8aeb6e4cac0'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    # keyboard.row("Новости", "Расписание", "Погода", "Какой сегодня день?", "/eu", "/help", "/roll")
    keyboard.row("/weather")
    bot.send_message(message.chat.id, "Привет! Что бы ты хотел узнать?", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'roll - случайное число от 1 до 6 \neu - вход в электронный университет \nhelp - описание команд')


@bot.message_handler(commands=['roll'])
def roll(message):
    bot.send_message(message.chat.id, randint(1, 6))


@bot.message_handler(commands=['eu'])
def eu(message):
    bot.send_message(message.chat.id, "https://lms.mtuci.ru/lms/login/index.php")


@bot.message_handler(commands=['weather'])
def weather(message):
    msg = bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(msg, get_city)


def get_city(message):
    global city
    city = message.text
    msg = bot.send_message(message.chat.id,
                           'На какой промежуток времени вы бы хотели узнать прогноз?(на сутки/на неделю')
    bot.register_next_step_handler(msg, get_weather)


def get_weather(message):
    if requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'q': city, 'APPID': appid}).status_code != 404:
        if message.text == 'на сутки':
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            # with open('weather.html', 'w', encoding='utf-8') as file:
            #   file.write(res.text)
            bot.send_message(message.chat.id,
                             f'Город: {city} \nПогодные условия: {data["weather"][0]["description"]} '
                             f'\nТемпература: {data["main"]["temp"]} \nМинимальная температура: {data["main"]["temp_min"]} '
                             f'\nМаксимальная температура: {data["main"]["temp_max"]}'
                             f'\nВидимость: <{data["visibility"] / 1000} км >'
                             f'\nСкорость ветра: <{data["wind"]["speed"]} м/с >')
        elif message.text == 'на неделю':
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid}, )
            data = res.json()
            bot.send_message(message.chat.id, "Прогноз погоды на неделю:")
            for i in range(0, len(data['list']), 8):
                bot.send_message(message.chat.id, f"Дата <{data['list'][i]['dt_txt']}>"
                                                  f"\r\nТемпература <{'{0:+3.0f}'.format(data['list'][i]['main']['temp'])}>"
                                                  f"\r\nПогодные условия <{data['list'][i]['weather'][0]['description']}>"
                                                  f"\r\nВидимость <{data['list'][i]['visibility'] / 1000} км >"
                                                  f"\r\nСкорость ветра <{data['list'][i]['wind']['speed']} м/с>")
            bot.send_message(message.chat.id, f"Дата <{data['list'][-1]['dt_txt']}>"
                                              f"\r\nТемпература <{'{0:+3.0f}'.format(data['list'][-1]['main']['temp'])}>"
                                              f"\r\nПогодные условия <{data['list'][-1]['weather'][0]['description']}>"
                                              f"\r\nВидимость <{data['list'][-1]['visibility'] / 1000} км >"
                                              f"\r\nСкорость ветра <{data['list'][i]['wind']['speed']} м/с>")
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так...')


def get_weather_daily(message):
    # city = message.text
    # bot.send_message(message.chat.id, f'(test)your city:{city}')
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    # with open('weather.html', 'w', encoding='utf-8') as file:
    #    file.write(res.text)
    bot.send_message(message.chat.id,
                     f'Город: {city} \nПогодные условия: {data["weather"][0]["description"]} '
                     f'\nТемпература: {data["main"]["temp"]} \nМинимальная температура: {data["main"]["temp_min"]} '
                     f'\nМаксимальная температура: {data["main"]["temp_max"]}')


def get_weather_weekly(message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid}, )
        data = res.json()
        # with open('weather.html', 'w', encoding='utf-8') as file:
        #    file.write(res.text)
        bot.send_message(message.chat.id, "Прогноз погоды на неделю:")
        for i in range(0, len(data['list']), 8):
            bot.send_message(message.chat.id, f"Дата <{data['list'][i]['dt_txt']}>"
                                              f"\r\nТемпература <{'{0:+3.0f}'.format(data['list'][i]['main']['temp'])}>"
                                              f"\r\nПогодные условия <{data['list'][i]['weather'][0]['description']}>"
                                              f"\r\nВидимость <{data['list'][i]['visibility'] / 1000} км >"
                                              f"\r\nСкорость ветра <{data['list'][i]['wind']['speed']} м/с>")
            print("____________________________")
            if i + 8 > 39:
                bot.send_message(message.chat.id, f"Дата <{data['list'][-1]['dt_txt']}>"
                                                  f"\r\nТемпература <{'{0:+3.0f}'.format(data['list'][-1]['main']['temp'])}>"
                                                  f"\r\nПогодные условия <{data['list'][-1]['weather'][0]['description']}>"
                                                  f"\r\nВидимость <{data['list'][-1]['visibility'] / 1000} км >"
                                                  f"\r\nСкорость ветра <{data['list'][i]['wind']['speed']} м/с>")
                print("____________________________")
    except Exception:
        bot.send_message(message.chat.id, 'Wrong city')


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
