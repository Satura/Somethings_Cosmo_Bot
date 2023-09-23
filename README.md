# Somethings&CosmoBot
Бот для отображения различной информации о финансах и космонавтике.

### Бот умеет:
- отображать сведения с сайтов ЦБ РФ, ГК «Роскосмос», портала «Новости космонавтики», в том числе новости по ключевому слову
- выводить случайный совет из подборки в приложенном CVS-фале
- конвертировать валюты
- выводить сведения о погоде на космодромах с Яндекс.Погоды
- показывать погоду с Яндекс.Погода по запросу пользователя (получает координаты с Яндекс.Карт)

### Использует дополнительные библиотеки: 
- telebot
- CurrencyConverter
- requests
- BeautifulSoup
- pandas
- json
- yandex_geocoder

Для работы в файле `constant.py` прописываются токены: _telegram_token_, _yandex_weather_token_ и _yandex_maps_token_

### Скриншоты

<details>
  <summary>Запуск, меню команд</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/01_start.png)
   
</details>

<details>
  <summary>Приветствие. Сводки основных "разделов", дальнейшая навигаия</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/02_%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B.png)
   
</details>

<details>
  <summary>Конвертер валют</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/03_%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D0%B5%D1%80.png)
   
</details>

<details>
  <summary>"Полезность"</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/04_%D0%BF%D0%BE%D0%BB%D0%B5%D0%B7%D0%BD%D0%BE%D1%81%D1%82%D1%8C.png)
   
</details>

<details>
  <summary>Сводка по космонавтике, информация кто на орбите</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/05_%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%20%D0%BA%D0%BE%D1%81%D0%BC%D0%BE%20(%D1%81%D0%B2%D0%BE%D0%B4%D0%BA%D0%B0%20%2B%20%D0%BD%D0%B0%20%D0%BE%D1%80%D0%B1%D0%B8%D1%82%D0%B5).png)
   
</details>

<details>
  <summary>Поиск новостей по ключевому слову с сайта</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/06_%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8%20%D0%BF%D0%BE%20%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B2%D0%BE%D0%BC%D1%83%20%D1%81%D0%BB%D0%BE%D0%B2%D1%83.png)
   
</details>

<details>
  <summary>Все последние новости с сайта</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/07_%D0%B2%D1%81%D0%B5%20%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B5%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8.png)
   
</details>

<details>
  <summary>Прогноз погоды</summary>
  
  ![](https://github.com/Satura/Finance_Space_Bot/blob/main/screenshots/07_%D0%B2%D1%81%D0%B5%20%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B5%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8.png)
   
</details>