import requests
import time
import random
# Обработка запросов http/https
from bs4 import BeautifulSoup
import lxml
# selenium - для подгрузки динамическиз элементов(карточек вайлдбериз) с использованием JS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# Для добавления времени ожидания
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# ChromeDriverManager необходим, чтобы "ходить" по странице
from webdriver_manager.chrome import ChromeDriverManager

last_year_serials_dict = {}


# Вход на сайт будто бы ты пользователь, а не питон
# from fake_useragent import UserAgent


def recommend_film():
    # ЗА ПОСЛЕДНИЙ ГОД
    url = 'https://kinogo.biz/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Настройка параметров Chrome

    driver.get(url)
    lenta_filmov = driver.find_element(By.CLASS_NAME, 'owl-stage')  # Используем find_element, а не find_elements
    filmy = lenta_filmov.find_elements(By.TAG_NAME, 'a')  # Находим все ссылки внутри lenta_filmov
    hrefs = [film.get_attribute('href') for film in filmy]

    film_info = {}

    def find_film_info(random_film):
        # Парсим информацию о фильме с каждой страницы <href>
        driver.get(random_film)
        content = driver.find_element(By.ID, "dle-content")

        # Имя
        fullstory__title = content.find_element(By.CLASS_NAME, 'fullstory__title')
        name = fullstory__title.find_element(By.TAG_NAME, 'h1').text
        # print(name)
        # Страна
        main_info = content.find_element(By.CLASS_NAME, 'main__info')
        spans = main_info.find_elements(By.TAG_NAME, 'span')
        country = spans[1].text.split(':').pop(-1)
        # print(country)
        # Ссылка на сайт
        link = random_film
        # print(link)
        # Картинка(ссылка)
        main__poster = content.find_element(By.CLASS_NAME, 'main__poster')
        picture = main__poster.find_element(By.TAG_NAME, 'img').get_attribute('src')
        # print(picture)
        # Описание
        description__block = content.find_element(By.CLASS_NAME, 'description__block')
        description = description__block.text
        # print(description)
        film_info[name] = [country, link, description, picture]
        return film_info

    random_film = str(random.sample(hrefs, 1)[0])
    return find_film_info(random_film)


if __name__ == '__main__':
    recommend_film()
