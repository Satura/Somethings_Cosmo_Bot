import time

import telebot
import func
from telebot import types
from constant import telegram_token

bot = telebot.TeleBot(telegram_token)
amount = 0
locations = []
news_index = 0
keyword_news_index = 0
all_kw_news = []
base_cur = ''
cur_list = []

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
                                      'может помочь с конвертацией валют и показать прогноз погоды, '
                                      'а так же что-то отобразит на тему космонавтики', reply_markup=reply_markup)


@bot.message_handler(commands=['converter'])
def converter(message):
    ''' Начало работы с конвертером '''
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, go_convert)


@bot.message_handler(commands=['fin_wisdom'])
def fin_wisdom(message):
    ''' Сводка с полезностями '''
    advice = func.fin_advice()
    adv = str(advice[0])
    descr = str(advice[1])
    markup = types.InlineKeyboardMarkup(row_width=2)
    url_btn1 = types.InlineKeyboardButton('FincultInfo', url='https://fincult.info')
    url_btn2 = types.InlineKeyboardButton('Тинькофф-Журнал', url='https://journal.tinkoff.ru')
    url_btn3 = types.InlineKeyboardButton('InvestFuture', url='https://investfuture.ru')
    url_btn4 = types.InlineKeyboardButton('SMART-LAB', url='https://smart-lab.ru')
    markup.add(url_btn1, url_btn2, url_btn3, url_btn4)
    bot.send_message(message.chat.id, f'''💸 *{adv}*\n{descr}
\n👛*Полезные ресурсы:* 
_FincultInfo_ — информационно-просветительский ресурс, созданный ЦБ РФ. Его цель — формирование финансовой культуры граждан.
_Тинькофф Журнал_ — издание про деньги и жизнь
_InvestFuture_. Digital-media об инвестициях и личных финансах
_SMART-LAB_. Мы делаем деньги на бирже''', reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(commands=['space_news'])
def space_news(message):
    """ Отображение последних 5 статей с сайта "Новости космонавтики" выбор дальнейшего шага"""
    # TODO: сброс индекса "порции" новостей через какое-то время, если пользователь забыл или проигнорировал кнопку "Хватит"
    global news_index
    output = ''
    markup = types.InlineKeyboardMarkup()
    more_btn = types.InlineKeyboardButton('Больше', callback_data='more_news')
    exit_btn = types.InlineKeyboardButton('Хватит', callback_data='exit_news')
    markup.add(more_btn, exit_btn)

    all_news = func.space_news_all()
    for i in range(news_index, news_index + 6):
        try:
            output += all_news[i]
        except IndexError:
            output += 'Дальше совсем уже не новости'
            break
    bot.send_message(message.chat.id, output, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['space_news_keyword'])
def space_news_keyword(message):
    """ Задание ключевого слова для поиска новостей """
    bot.send_message(message.chat.id, 'О чем желаете найти новости?')
    bot.register_next_step_handler(message, search_in_news)


@bot.message_handler(commands=['get_weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Введите название населенного пункта')
    bot.register_next_step_handler(message, get_weather)


@bot.message_handler()
def navigate(message):
    """ Сводка и навгация по "разделам" деньги/космос """
    markup = types.InlineKeyboardMarkup()
    some_btn1 = types.InlineKeyboardButton('Конвертер валют', callback_data='converter')
    some_btn2 = types.InlineKeyboardButton('Фин. мудрость', callback_data='fin_wisdom')
    some_btn3 = types.InlineKeyboardButton('Прогноз погоды', callback_data='weather')
    cosmo_btn1 = types.InlineKeyboardButton('Сейчас на орбите', callback_data='orbit')
    cosmo_btn2 = types.InlineKeyboardButton('Новости космонавтики', callback_data='space_news')
    cosmo_btn3 = types.InlineKeyboardButton('Новости по ключевому слову', callback_data='space_news_keyword')

    if message.text == 'Всяко-разно':
        # Сводка от ЦБ, дальнейшая навигация 
        brief = func.fin_info()
        markup.add(some_btn1, some_btn2)
        markup.add(some_btn3)
        bot.send_message(message.chat.id, brief, reply_markup=markup)

    if message.text == 'Космо':
        # Сводка по космонавтике, дальнейшая навигация
        brief = (f'{func.launch()}\n'
                 f'\n--- Погода на космодромах ---\n'
                 f'\nБайконур: \n{func.weather("Байконур")}\n'
                 f'\nВосточный: \n{func.weather("Восточный")}\n'
                 )
        markup.add(cosmo_btn1, cosmo_btn2)
        markup.add(cosmo_btn3)
        bot.send_message(message.chat.id, brief, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # навигация по Inline-кнопкам
    if callback.data == 'fin_wisdom':
        fin_wisdom(callback.message)

    if callback.data == 'converter':
        converter(callback.message)

    if callback.data == 'weather':
        weather(callback.message)

    if callback.data == 'orbit':
        bot.send_message(callback.message.chat.id, func.in_orbit(), parse_mode='Markdown')

    if callback.data == 'space_news':
        space_news(callback.message)

    if callback.data == 'space_news_keyword':
        space_news_keyword(callback.message)

    global news_index, keyword_news_index

    if callback.data == 'more_news':
        news_index += 5
        space_news(callback.message)

    if callback.data == 'exit_news':
        news_index = 0
        bot.send_message(callback.message.chat.id, 'ok')

    if callback.data == 'more_kw_news':
        keyword_news_index += 3
        print_3_kw_news(callback.message)

    if callback.data == 'exit_kw_news':
        keyword_news_index = 0
        bot.send_message(callback.message.chat.id, 'ok')


def search_in_news(message):
    """ Ищет и отображает новости по заданному слову """
    global all_kw_news
    keyword = message.text.strip()
    all_kw_news = func.space_news2(keyword)
    if len(all_kw_news) == 0:
        bot.send_message(message.chat.id, 'Нет новостей об этом')
    else:
        print_3_kw_news(message)


def print_3_kw_news(message):
    global all_kw_news, keyword_news_index
    # TODO: сброс индекса "порции" новостей через какое-то время, если пользователь забыл или проигнорировал кнопку "Хватит"
    output = ''
    markup = types.InlineKeyboardMarkup()
    more_btn = types.InlineKeyboardButton('Больше', callback_data='more_kw_news')
    exit_btn = types.InlineKeyboardButton('Хватит', callback_data='exit_kw_news')
    markup.add(more_btn, exit_btn)

    for i in range(keyword_news_index, keyword_news_index + 3):
        try:
            output += all_kw_news[i]
        except IndexError:
            output += 'Дальше новости совсем не свежие и не загружались\n'
            break

    bot.send_message(message.chat.id, output, reply_markup=markup, parse_mode='Markdown')


def go_convert(message):
    """ Получает от пользователя сумму, которую требуется конвертировать """
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Введите целое положительное число')
        bot.register_next_step_handler(message, go_convert)

    if amount > 0:
        bot.send_message(message.chat.id, 'Введите сообщение в виде: "<базовая валюта> <валюта1>,<валюта2>,...<валютаN>"')
        bot.register_next_step_handler(message, take_currency)
    else:
        bot.send_message(message.chat.id, 'Введите положительное число')
        bot.register_next_step_handler(message, go_convert)


def take_currency(message):
    """ Разбирает какие пары валют пользователь запрашивает """
    global base_cur, cur_list

    currencies = message.text.upper().split(" ", 1)
    if len(currencies) >= 2:
        base_cur = currencies[0]
        cur_list = currencies[1].replace(" ", "").split(',')

    else:
        bot.send_message(message.chat.id, f'Забыли целевую валюту. Введите  запрос заного (базовая-пробел-целевые(через запятую)))')
        bot.register_next_step_handler(message, take_currency)
        return
    try:
        result = func.new_converter(amount, base_cur, cur_list)
        bot.send_message(message.chat.id, result, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{e}\nВведите другую пару валют')
        bot.register_next_step_handler(message, take_currency)


def get_weather(message):
    """ Получает координаты и погоду (если найден только один пункт с таким названием) """

    name = message.text
    global locations  # , lon, lat
    locations = func.search_loc(name)

    if len(locations) == 1:
        lon, lat = locations[0]['GeoObject']['Point']['pos'].split()
        bot.send_message(message.chat.id, func.get_weather_coord(lon, lat), parse_mode='Markdown')
    #
    if len(locations) > 1:
        all_locs = ''
        for l in range(len(locations)):
            all_locs += f"{l} - {locations[l]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']}\n"

        bot.send_message(message.chat.id, f'Найдено несколько населенных пунктов с таким названием. '
                                          f'Выберите номер локации: \n{all_locs}')
        bot.register_next_step_handler(message, choose_location)


def choose_location(message):
    """ Принимает номер выбранной локации и выводит погоду """
    global locations  # , lon, lat
    num = int(message.text)
    lon, lat = locations[num]['GeoObject']['Point']['pos'].split()
    bot.send_message(message.chat.id, func.get_weather_coord(lon, lat), parse_mode='Markdown')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(f'There is an error: {e} at {time.time()}')


# bot.polling(none_stop=True)
