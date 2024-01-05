import requests
import time
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

last_year_films_dict = {}


# Вход на сайт будто бы ты пользователь, а не питон
# from fake_useragent import UserAgent


def find_5films_lastyear():
    # ЗА ПОСЛЕДНИЙ ГОД
    url = 'https://kinogo.biz/xfsearch/year-teg-xfsearch/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Настройка параметров Chrome

    driver.get(url)

    def find_last_year():

        nav_panel = driver.find_element(By.CLASS_NAME, 'leftblok_contener')
        leftblok_contener2 = nav_panel.find_element(By.CLASS_NAME, 'leftblok_contener2')
        leftblok2 = leftblok_contener2.find_element(By.CLASS_NAME, 'leftblok2')
        right_block = leftblok2.find_element(By.CLASS_NAME, 'miniblock')
        miniblock = right_block.find_element(By.CLASS_NAME, 'mini')
        return miniblock

    def recheck_choosed_category(miniblock):
        kateg_name = ''
        for i in find_last_year().text:
            kateg_name += str(i)
            if i == '\n':
                if kateg_name.strip() == 'По году':
                    return kateg_name
                else:
                    return False

    def find_link_to_go_to_films() -> str:
        # Ищем новую ссылку
        link = find_last_year().find_elements(By.TAG_NAME, 'a')
        last_link = link[-1]
        # Новое подключение к поиску последнего года
        url_20xx = last_link.get_attribute('href')
        return url_20xx

    # Переход по новой ссылке и поиск фильма
    url_20xx_year = find_link_to_go_to_films() + 'page/{}'

    def find_info_about_films(shortstories):
        # Собираем фильмы со страницы
        for films in shortstories:

            # Ищем имя
            film_title = films.find_element(By.CLASS_NAME, 'shortstory__title')
            film_name = film_title.find_element(By.TAG_NAME, 'h2').text.strip()
            if '(2023)' in film_name:
                film_name = film_name.replace(' (2023)', '')

            # Ищем страну
            shortstory__body = films.find_element(By.CLASS_NAME, 'shortstory__body')
            shortstory_info_wrapper = shortstory__body.find_elements(By.TAG_NAME, 'span')
            country = shortstory_info_wrapper[
                1].find_element(By.TAG_NAME, 'a').text

            # Ищем ссылку
            link = films.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Ищем описание фильма
            shortstory__body = films.find_element(By.CLASS_NAME, 'shortstory__body')
            descriprion = shortstory__body.find_element(By.CLASS_NAME, 'excerpt')
            descriprion = descriprion.get_attribute('innerHTML')

            # Ищем ссылку картинки(отправка пользователю)
            shortstory__body = films.find_element(By.CLASS_NAME, 'shortstory__body')
            shortstory__poster = shortstory__body.find_element(By.CLASS_NAME, 'shortstory__poster')
            picture_link = 'https://kinogo.biz/' + shortstory__poster.find_element(By.TAG_NAME,
                                                                                   'img').get_attribute(
                'data-src')
            # Запись данных в словарь
            last_year_films_dict[film_name] = [country, link, descriprion, picture_link]

        return last_year_films_dict

    def filters_on():

        def click_button(xpath):
            # Настраиваем сайт, включая все нужные фильтры по фильмам
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", button)

        print('Начало выполнения установки кнопок фильтрации...')

        # print('Ищем кнопку Сортировка')
        click_button('//button[normalize-space()="ТОП за 3 дня"]')
        # print('Нашли нажали')

        # print('Ищем кнопку Тип')
        click_button('//button[normalize-space()="Тип"]')
        # print('Нашли нажали')

        #         print('Ищем кнопку Фильмы')
        click_button('//button[normalize-space()="Фильм"]')
        #         print('Нашли нажали')

        #         print('Ищем кнопку Применить')
        click_button('//button[normalize-space()="Применить"]')
        print('Нашли нажали\n\n//ИТЕРРАЦИЯ ОКОНЧЕНА...\n\n')

    try:
        filters_on()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    for counter in range(1, 6):
        driver.get(url_20xx_year.format(counter))
        print(url_20xx_year.format(counter))
        time.sleep(0.3)

        films_pan = driver.find_element(By.ID, 'dle-content')
        shortstories = films_pan.find_elements(By.CLASS_NAME, 'shortstory')

        find_info_about_films(shortstories)

    last_year_films = find_info_about_films(shortstories)
    # print(last_year_films)
    return last_year_films


if __name__ == '__main__':
    find_5films_lastyear()
