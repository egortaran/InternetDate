import re

import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from transliterate import translit

base_url = 'https://omsk.hh.ru'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'

client = MongoClient('127.0.0.1', 27017)
db = client['hhru']
vacancies = db.vacancies

s_vacancy = translit(input('Название вакансии: '), 'ru', reversed=True).lower()
s_page = int(input('Количество страниц: '))

data = []
for page in range(s_page):
    url = base_url + '/vacancies/' + s_vacancy

    page_url = f'?page={page}&hhtmFrom=vacancy_search_catalog'
    if page != 0:
        url + page_url

    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url, headers=headers)

    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        link_new = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
        name_new = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
        payment = vacancy.find('span', {'class': 'bloko-header-section-3'})
        vacancy_company_link = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})['href']

        response2 = requests.get(base_url + vacancy_company_link, headers=headers)
        dom2 = bs(response2.text, 'html.parser')
        company_link_new = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})
        vac_id = re.search(r'\d+', link_new)

        if payment:
            vacancy_compensation = payment.getText().replace('\u202f', ' ').replace(' ', ' ')
        else:
            vacancy_compensation = None
        if company_link_new:
            company_link_new = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})['href']
        else:
            company_link_new = None
        vacancy_data['_id'] = vac_id[0]
        vacancy_data['salary'] = vacancy_compensation
        vacancy_data['link'] = link_new
        vacancy_data['name'] = name_new
        vacancy_data['company_site'] = company_link_new

        try:
            vacancies.insert_one(vacancy_data)
        except DuplicateKeyError:
            print(f"Document with id = {vacancy_data['_id']} already exist")

        vacancy_id = ''
        vacancy_compensation = ''
        link = ''
        name = ''
        company_link = ''
        print('--' * page * 10)
