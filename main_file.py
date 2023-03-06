import telebot
from telebot import types
from config import open_weather_token, TOKEN, URL_HOROSCOPE
from weather import get_weather
# from goroskope import get_html, get_content, parser

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Функция запускается при вводе команды в телеграмме /start. Отправляется приветственное сообщение и
    появлется меню с выбором кнопки
    :param message: команда /start
    :return: две кнопки: погода в городе и гороскоп на сегодня
    """
    try:
        mess = f'Привет {message.from_user.first_name}'
        bot.send_message(message.chat.id, mess)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        weather = types.KeyboardButton('Погода в городе')
        horoscope = types.KeyboardButton('Гороскоп на сегодня')
        markup.add(weather, horoscope)
        bot.send_message(message.chat.id, 'Выберите: ', reply_markup=markup)
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, 'Повторите запрос командой "/start"')
        menu(message)


def menu(message):
    """
    Функция возвращает главное меню при завершения запроса.
    :param message: команда /start
    :return:две кнопки: погода в городе и гороскоп на сегодня
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    weather = types.KeyboardButton('Погода в городе')
    horoscope = types.KeyboardButton('Гороскоп на сегодня')
    markup.add(weather, horoscope)
    bot.send_message(message.chat.id, 'Выберите: ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    """
     Функция обрабатывает запрос пользователя и на основе выбора запрашивает название города либо выводит
     кнопки с вариантами знака зодиака. Далее вызываются соответствующие функции обработки запроса.
     :param message: погода в городе или гороскоп на сегодня
     :return: соответствующие клавиатуры для выбора значений
    """
    if message.text == 'Погода в городе':
        msg = bot.send_message(message.chat.id, 'Укажите город:')
        bot.register_next_step_handler(msg, weather_request)
    elif message.text == 'Гороскоп на сегодня':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        aries = types.KeyboardButton("Овен")
        telets = types.KeyboardButton("Телец")
        gemini = types.KeyboardButton("Близнецы")
        rak = types.KeyboardButton("Рак")
        lion = types.KeyboardButton("Лев")
        deva = types.KeyboardButton("Дева")
        vesy = types.KeyboardButton("Весы")
        scorpion = types.KeyboardButton("Скорпион")
        strelets = types.KeyboardButton("Стрелец")
        kozerog = types.KeyboardButton("Козерог")
        vodoley = types.KeyboardButton("Водолей")
        fishes = types.KeyboardButton("Рыбы")
        markup.add(aries, telets, gemini, rak, lion, deva, vesy, scorpion, strelets, kozerog, vodoley, fishes)
        sign = bot.send_message(message.chat.id, text="Укажите Ваш знак зодиака:", reply_markup=markup)
        bot.register_next_step_handler(sign, horoscope_request)
    else:
        bot.send_message(message.chat.id, 'Вы не выбрали один из предложенных вариантов.'
                                          'Повторите запрос командой "/start"')


def weather_request(message):
    """
     Функция получает в качестве аргумента название города и передает его в функцию парсера прогноза погоды
     :param message: название города
     :return: текущая погода в городе
    """
    city = message.text
    try:
        bot.send_message(message.chat.id, get_weather(city, open_weather_token))
        menu(message)
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, 'Город не найден. Повторите запрос')

        main_menu(message.text == 'Гороскоп на сегодня')

#
# def horoscope_request(message):
#     """
#      Функция получает в качестве аргумента название знака зодиака, извлекает все знаки зодиака с главной страницы и
#      ссылки на каждый знак зодиака для последующей передачи ссылки конкретного знака в функцию получения url.
#      :param message: Знак зодиака
#      :return: гороскоп на сегодня
#     """
#
#     try:
#         my_sign = message.text
#         html = get_html(URL_HOROSCOPE)
#         cards = get_content(html.text)
#
#         def get_url_sign(sign):
#             """
#              Функция получает в качестве аргумента название знака зодиака и выдает url страницы для передачи его парсеру
#              конкретной страницы данного знака зодиака
#              :return: url знака зодиака
#             """
#             for sign in cards:
#                 if my_sign.lower() == sign['Sign'].lower():
#                     url = str(sign['link'])
#                     return url
#                 else:
#                     pass
#
#         url_sign = (get_url_sign(my_sign))
#         html_sign = get_html(url_sign)
#         bot.send_message(message.chat.id, parser(html_sign))
#         telebot.types.ReplyKeyboardRemove()
#         menu(message)
#     except Exception as ex:
#         print(ex)
#         bot.send_message(message.chat.id, 'Повторите запрос и выберите один из предложенных знаков зодиака')
#         menu(message)


bot.polling(none_stop=True)