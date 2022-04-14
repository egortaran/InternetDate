import pprint
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://e.mail.ru/login')

login = 'study.ai_172@mail.ru'
password = 'NextPassword172#'

iframe1 = driver.find_element(By.XPATH, "//iframe[@class='ag-popup__frame__layout__iframe']")
driver.switch_to.frame(iframe1)

wait = WebDriverWait(driver, 20)
elem_login = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
elem_login.send_keys(login + '\n')
time.sleep(3)
elem_password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
elem_password.send_keys(password + '\n')

letters = []
for i in range(20):
    url = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='llc llc_normal llc_new llc_new-selection "
                                                               "js-letter-list-item "
                                                               "js-tooltip-direction_letter-bottom']"
                                                               f"[{i + 1}]"
                                                     ))).get_attribute('href')
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    sender = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='letter-contact']"))).text
    date = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='letter__date']"))).text
    subject = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='thread-subject']"))).text
    text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-body'))).text

    letter = {
        'sender': sender,
        'date': date,
        'subject': subject,
        'text': text
    }
    driver.execute_script("window.history.go(-1)")

    letters.append(letter)

client = MongoClient('127.0.0.1')
db = client['mail.ru']
collection = db.get_collection('letters')
for let in letters:
    collection.insert_one(let)

