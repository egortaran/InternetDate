from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
from transliterate import translit


def main():
    # s_vacancy = translit(input('Название вакансии: '), 'ru', reversed=True).lower()
    # create_html(s_vacancy)

    with open('response.html', 'r', encoding='utf-8') as f:
        html_file = f.read()

    dom = bs(html_file, 'html.parser')

    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    vacancies_list = []
    for vacancy in vacancies:
        name = vacancy.find('a', {'class': 'bloko-link'}).getText()
        link = vacancy.find('a', {'class': 'bloko-link'})['href']

        f_salary = vacancy.find('span', {'class': 'bloko-header-section-3'})
        salary = find_salary(f_salary)

        vacancies_list.append({'Вакансия': name, 'Зарплата': salary, 'Ссылка': link, })
    pprint(vacancies_list)


def find_salary(f_salary):
    salary = {
        'min': '',
        'max': '',
        'currency': ''
    }

    if f_salary is not None:
        f_salary = f_salary.getText()
        fn_salary = f_salary.replace(' ', ' ').replace(' ', '')
        dash = fn_salary.find('–')

        # Поиск последнего числа в строке
        last_d = 0
        for d in range(len(fn_salary)):
            if fn_salary[d].isdigit():
                last_d = d

        if dash != -1:  # Пример: 30 000 – 180 000 руб.
            salary['min'] = int(fn_salary[:dash])
            salary['max'] = int(fn_salary[dash + 1:last_d + 1])
        elif fn_salary.find('от') != -1:  # Пример: от 70 000 руб
            salary['min'] = int(fn_salary[:last_d + 1].replace('от', ''))
        elif fn_salary.find('до') != -1:  # Пример до 45 000 руб.
            salary['max'] = int(fn_salary[:last_d + 1].replace('до', ''))
        salary['currency'] = fn_salary[last_d + 1:]
        
    return salary


def create_html(s_vacancy):
    base_url = 'https://omsk.hh.ru'
    url = base_url + '/vacancies/' + s_vacancy

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }

    response = requests.get(url, headers=headers)
    with open('response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # print(response)


if __name__ == '__main__':
    main()
