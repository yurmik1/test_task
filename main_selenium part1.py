
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import pandas as pd
from selenium import webdriver
import time



os.chdir(r'C:\py_project\pythonProject\Chromedriver')
os.getcwd()

url = 'https://www.moex.com/'
url_1 = 'https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=CAD_RUB'
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36')

s = Service('C:/py_project/pythonProject/Chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)

# Драйвер готов, начинаем кликать в браузере. Забираем таблицу USD
try:
    driver.get(url=url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="redesign-2021"]/div[3]/div[2]/div/div/div[2]/nav/span[1]/button').click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, 'Срочный рынок').click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, 'Согласен').click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, 'Индикативные курсы').click()
    time.sleep(3)
    # С помощью Pandas принимаем от Selenium веб страницу и находим в ней таблицу
    html1 = driver.page_source
    table1 = pd.read_html(html1, match='Курс промежуточного клиринга')
    table1 = pd.DataFrame(table1[0])
    table1.columns = ['Дата', 'Значение курса промежуточного клиринга', 'Время', 'Значение курса основного клиринга',
                      'Время']
    # С помощью Pandas принимаем от Selenium веб страницу и находим в ней таблицу
    print("взяли первую таблицу")
    print(table1)
    # Забираем вторую таблицу
    time.sleep(3)
    driver.get(url=url_1)
    time.sleep(3)
    #driver.find_element(By.LINK_TEXT, 'Согласен').click()
    #time.sleep(3)
    html2 = driver.page_source
    table2 = pd.read_html(html2, match='Курс промежуточного клиринга')
    table2 = pd.DataFrame(table2[0])
    table2.columns = ['Дата', 'Значение курса промежуточного клиринга', 'Время', 'Значение курса основного клиринга', 'Время']
    # Добавляем столбец
    table2 = table2.assign(Изменение="")
    print("взяли вторую таблицу")
    print(table1)
    # Объединяем фреймы и сохраняем в EXCEL. Переходим в Part2
    table_full = pd.concat([table1, table2], sort=False, axis=1)
    table_full.to_excel('export.xlsx', index=False)
    print("Сохранили в EXCEL")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

