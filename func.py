import requests
from bs4 import BeautifulSoup
from constant import yandex_weather_token
import json
import pandas as pd
import random

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
}


def fin_info():
    """ Сводка фин. показателей (ключевая ставка, курс валют от ЦБ РФ) """
    url_crb = 'https://cbr.ru'

    req_cbr = requests.get(url_crb).text
    sp_cbr = BeautifulSoup(req_cbr, 'html.parser')
    indicators = sp_cbr.findAll('div', class_="main-indicator")
    rate = indicators[2].find('div', class_="main-indicator_value").get_text()
    # print(f'Текущая ключевая ставка: {rate}')

    exchange_rates = sp_cbr.findAll('div', class_="main-indicator_rate")
    exchange_rates_m1 = exchange_rates[0].findAll('div')
    # print(f'{exchange_rates_m1[0].get_text(strip=True)}: {exchange_rates_m1[1].get_text(strip=True)}')
    exchange_rates_m2 = exchange_rates[1].findAll('div')
    # print(f'{exchange_rates_m2[0].get_text(strip=True)}: {exchange_rates_m2[1].get_text(strip=True)}')
    exchange_rates_m3 = exchange_rates[2].findAll('div')
    # print(f'{exchange_rates_m3[0].get_text(strip=True)}: {exchange_rates_m3[1].get_text(strip=True)}')

    return f"""Текущая ключевая ставка: {rate}
Курс основных валют: 
{exchange_rates_m1[0].get_text(strip=True)}: {exchange_rates_m1[1].get_text(strip=True)}
{exchange_rates_m2[0].get_text(strip=True)}: {exchange_rates_m2[1].get_text(strip=True)}
{exchange_rates_m3[0].get_text(strip=True)}: {exchange_rates_m3[1].get_text(strip=True)}
"""

def space_news():
    ''' Выводит сводку новостей с первой страницы сайта Новости космонавтики, раздел Новости '''
    
    url_space_news = 'https://novosti-kosmonavtiki.ru/news/'
    req_space_news = requests.get(url_space_news, headers).text
    soup = BeautifulSoup(req_space_news, 'html.parser')
    news_cards = soup.findAll('article')
    news = []
    
    for card in news_cards:
        card_date = card.find('span', class_="entry-date").get_text()
        card_title = card.find('h2', class_="post-title").get_text()
        card_link = card.find('a', class_="read-more").get("href")
        news.append(f'{card_date} / {card_title} \n{card_link}\n')

    return news


def space_news2(key_word):
    ''' Выводит сводку новостей по искомому слову на последних 5 страницах
    сайта "Новости космонавтики", раздел "Новости" '''

    url_space_news = 'https://novosti-kosmonavtiki.ru/news/'
    news = ''
    
    for page in range(1, 6):
        url = url_space_news + f'page/{page}'
        # print(url) # check
        req = requests.get(url).text
        sp = BeautifulSoup(req, 'html.parser')
        articles = sp.findAll('article')
        for art in articles:
            art_title = art.find('h2', class_="post-title").get_text()
            # print(art_title) # check
            if key_word.lower() in art_title.lower():
                art_date = art.find('span', class_="entry-date").get_text()
                art_link = art.find('a', class_="read-more").get("href")
                # print(f'{art_date} / {art_title} \n{art_link}') # check
                news += f'{art_date} / {art_title} \n{art_link}\n'
    
    return news

def space_news_all():
    ''' Получает все новости с сайта Новости космонавтики '''
    
    url_space_news = 'https://novosti-kosmonavtiki.ru/news/'
    req_space_news = requests.get(url_space_news, headers).text
    soup = BeautifulSoup(req_space_news, 'html.parser')
    page_numbers = soup.findAll('a', class_='page-numbers')
    last_page = page_numbers[-2].get_text()
    news = ''
    for page in range(1, last_page+1):
        url = url_space_news + f'page/{page}'
        # print(url) # check
        req = requests.get(url).text
        sp = BeautifulSoup(req, 'html.parser')
        articles = sp.findAll('article')
        for art in articles:
            art_title = art.find('h2', class_="post-title").get_text()
            art_date = art.find('span', class_="entry-date").get_text()
            art_link = art.find('a', class_="read-more").get("href")
            news += f'{art_date} / {art_title} \n{art_link}\n'
    return news

def in_orbit():
    """ Выводит количество человек на орбите на сегодняшний день и их имена """
    url = 'https://novosti-kosmonavtiki.ru/mks/'

    req = requests.get(url, headers).text
    sp = BeautifulSoup(req, 'html.parser')
    cosmonauts = sp.findAll('h2', class_='post-title')
    output = f'На орбите сегодя {len(cosmonauts)} человек:\n'
    for c in cosmonauts:
        output += c.get_text() + "\n"
    return output


def launch():
    """ Выводит информацию о прошедшем пуске """
    # от чего-то они перестали указывать предстоящий
    url_rs = "https://www.roscosmos.ru"
    req_rs = requests.get(url_rs).text
    sp = BeautifulSoup(req_rs, 'html.parser')
    prev_launch = sp.find('div', class_="frame prev-frame")
    return f'Прошедший пуск состоялся {prev_launch.get_text(separator=" / ", strip=True)}'


def weather(name):
    """ Получение погоды для космодромов с Яндекс.Погоды """
    if name == "Восточный":
        lat = 51.884008
        lon = 128.334432
    if name == "Байконур":
        lat = 46.060493
        lon = 63.318439
    if name == "Плесецк":
        lat = 62.956901
        lon = 40.459387
    url_yaweather = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=u_RU&extra=true'
    yandex_req = requests.get(url_yaweather, headers={'X-Yandex-API-Key': yandex_weather_token})

    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }

    yandex_json = json.loads(yandex_req.text)
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    return f"""Температура: {yandex_json['fact']['temp']} , условия: {yandex_json['fact']['condition']}
давление: {yandex_json['fact']['pressure_mm']} влажность: {yandex_json['fact']['humidity']}"""

def fin_advice():
    ''' Выводит рандомный совет по фининсам из файла fin_advice.cvs '''
    df = pd.read_csv('fin_advice.cvs', sep=';')
    r = random.randint(0,len(df))
    adv = str(df['advice'][r])
    descr = str(df['descr'][r])
    return f'{adv}\n{descr}'
