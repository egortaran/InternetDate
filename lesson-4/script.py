from datetime import datetime
from lxml import html
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit / 537.36(KHTML, like Gecko) '
                  'Chrome / 79.0.3945.130Safari / 537.36'
}


def find_news_mail_ru():
    url = 'https://news.mail.ru/'
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    title = dom.xpath("//span[@class='newsitem__title-inner']/text()")
    link = dom.xpath("//a[@class='newsitem__title link-holder']/@href")
    date_publication = dom.xpath("//span[@class='newsitem__param js-ago']/@datetime")
    name_sourse = dom.xpath("//span[@class='newsitem__param']/text()")

    result = []
    for i in range(len(title)):
        date = datetime.strptime(date_publication[i], "%Y-%m-%dT%H:%M:%S%z")
        res = {
            'title': title[i],
            'link': link[i],
            'date_publication': date.strftime("%m/%d/%Y, %H:%M:%S"),
            'name_sourse': name_sourse[i],
        }
        result.append(res)
    return result


def find_news_lenta():
    url = 'https://lenta.ru'
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    title = dom.xpath("//span[@class='card-mini__title']/text()")
    link = dom.xpath("//div[@class='last24']/a/@href")

    result = []
    for i in range(len(link)):
        next_page_response = requests.get(url + link[i], headers=header)
        next_page_dom = html.fromstring(next_page_response.text)

        date_publication = next_page_dom.xpath("//time[@class='topic-header__item topic-header__time']/text()")
        name_sourse = next_page_dom.xpath("//a[@class='topic-authors__author']/text()")

        res = {
            'title': title[i],
            'link': url + link[i],
            'date_publication': date_publication[0],
            'name_sourse': name_sourse[0],
        }
        result.append(res)
    return result


def find_news_yandex():
    url = 'https://yandex.ru/news/'
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    title = dom.xpath("//h2[@class='mg-card__title']/a/text()")
    link = dom.xpath("//a[@class='mg-card__source-link']/@href")
    date_publication = dom.xpath("//span[@class='mg-card-source__time']/text()")
    name_sourse = dom.xpath("//a[@class='mg-card__source-link']/text()")

    result = []
    for i in range(len(title)):
        res = {
            'title': title[i],
            'link': link[i],
            'date_publication': date_publication[i],
            'name_sourse': name_sourse[i],
        }
        result.append(res)
    return result


if __name__ == '__main__':
    t_file = [find_news_yandex(), find_news_mail_ru(), find_news_lenta()]
