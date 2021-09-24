from lxml import html
import requests
import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Lesson_4_DZ']
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 Safari/537.36 '
         }

yandex_news = 'https://yandex.ru/news/'


def main_news_yandex(url):
    response = requests.get(url, headers=header).text
    root = html.fromstring(response)
    articles = root.xpath('//*/div/article')
    for article in articles:
        news_source = article.xpath('.//*/span[1]/a/text()')[0]
        news_title = (article.xpath('.//*/a/h2/text()'))[0]
        news_link = article.xpath('.//*/a/@href')[0]
        news_time = f'{datetime.date.today()} {article.xpath(".//*/div/span[2]/text()")[0]}'
        serc = []
        for item in db.yandex_news.find({'Title': news_title}):
            serc.append(item)
        if not serc:
            db.yandex_news.insert_one(
                {'Title': news_title, 'Source': news_source, 'Link': news_link, 'Time': news_time})

main_news_yandex(yandex_news)