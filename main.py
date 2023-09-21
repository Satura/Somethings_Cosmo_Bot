import telebot
import func
from telebot import types
from constant import telegram_token
import webbrowser
from currency_converter import CurrencyConverter

bot = telebot.TeleBot(telegram_token)
amount = 0
c = CurrencyConverter()
all_news = ''


@bot.message_handler(commands=['start'])
def main(message):
    ''' Приветственное сообщение и переход по разделам '''
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu_btn1 = types.KeyboardButton('Всяко-разно')
    menu_btn2 = types.KeyboardButton('Космо')
    reply_markup.add(menu_btn1, menu_btn2)
    bot.send_message(message.chat.id, 'Приветствую.\n'
                                      'Бот умеет выводить цифры от ЦБ РФ, '
                                      'покажет какой-нибудь совет по финансам и подскажет ресурсы с разными пооезностями, '
                                      'может помочь с конвертацией валют, '
                                      'а так же что-то отобразит на тему космонавтики', reply_markup=reply_markup)


@bot.message_handler(commands=['converter'])
def converter(message):
    ''' Начало работы с конвертером '''
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, go_convert)


@bot.message_handler(commands=['site_fin_cult'])
def site_fin_cult(message):
    ''' Сводка с полезностями '''
    advice = func.fin_advice()
    info = f'''Совет дня: {advice}\n
а так же
    * много разного полезного от ЦБ РФ: Финансовая культура  https://fincult.info
    * о самом разном: Тинькофф-Журнал https://journal.tinkoff.ru
    * об инвестициях: InvestFuture https://investfuture.ru'''

    bot.send_message(message.chat.id, info)
    # webbrowser.open('https://fincult.info') # это работало,
    # отказалась от идеи каждый раз принудительно "пользвателю" открывать страницу


@bot.message_handler(commands=['space_news'])
def space_news(message):
    ''' Отображение последних 25 статей с сайта "Новости космонавтики" '''
    output = ''
    last_news_page = func.space_news()
    for i in range(25):
        output += last_news_page[i]
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['space_news_keyword'])
def space_news_keyword(message):
    ''' Задание ключевого слова для поиска новостей '''
    bot.send_message(message.chat.id, 'О чем желаете найти новости?')
    bot.register_next_step_handler(message, search_in_news)


@bot.message_handler()
def navigate(message):
    ''' Сводка и навгация по "разделам" деньги/космос '''
    markup = types.InlineKeyboardMarkup()
    fin_btn1 = types.InlineKeyboardButton('Конвертер валют', callback_data='converter')
    fin_btn2 = types.InlineKeyboardButton('Полезность', callback_data='site_fin_cult')
    cosmo_btn1 = types.InlineKeyboardButton('Сейчас на орбите', callback_data='orbit')
    cosmo_btn2 = types.InlineKeyboardButton('Новости космонавтики', callback_data='space_news')
    cosmo_btn3 = types.InlineKeyboardButton('Новости по ключевому слову', callback_data='space_news_keyword')

    if message.text == 'Всяко-разно':
        # Сводка от ЦБ, дальнейшая навигация 
        brief = func.fin_info()
        markup.add(fin_btn1, fin_btn2)
        bot.send_message(message.chat.id, brief, parse_mode='HTML', reply_markup=markup)

    if message.text == 'Космо':
        # Сводка по космонавтике, дальнейшая навигация
        brief = (f'{func.launch()}\n'
                 f'\n--- Погода на космодромах ---\n'
                 f'\nБайконур: \n{func.weather("Байконур")}\n'
                 f'\nВосточный: \n{func.weather("Восточный")}\n'
                 f'\nПлесецк: \n{func.weather("Плесецк")}')
        markup.add(cosmo_btn1, cosmo_btn2)
        markup.add(cosmo_btn3)
        bot.send_message(message.chat.id, brief, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # навигация по Inline-кнопкам
    if callback.data == 'site_fin_cult':
        site_fin_cult(callback.message)

    if callback.data == 'converter':
        converter(callback.message)

    if callback.data == 'orbit':
        bot.send_message(callback.message.chat.id, func.in_orbit())

    if callback.data == 'space_news':
        space_news(callback.message)

    if callback.data == 'space_news_keyword':
        space_news_keyword(callback.message)


def search_in_news(message):
    ''' Ищет и отображает новости по заданному слову '''
    keyword = message.text.strip()
    output = func.space_news2(keyword)
    bot.send_message(message.chat.id, output)


def go_convert(message):
    ''' Получает от пользователя сумму, которую требуется конвертировать ''' 
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Введите целое положительное число')
        bot.register_next_step_handler(message, go_convert)

    if amount > 0:
        bot.send_message(message.chat.id, 'Введите валюты через слэш (пр.: "cny/usd")')
        bot.register_next_step_handler(message, take_currency)
    else:
        bot.send_message(message.chat.id, 'Введите положительное число')
        bot.register_next_step_handler(message, go_convert)


def take_currency(message):
    ''' Разбирает какую пару валют пользователь запрашивает '''
    currencies = message.text.upper().split('/')
    try:
        result = round(c.convert(amount, currencies[0], currencies[1]), 2)
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{e}\nВведите другую пару валют')
        bot.register_next_step_handler(message, take_currency)


bot.polling(none_stop=True)
