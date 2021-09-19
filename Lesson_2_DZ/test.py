from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml

item_url = 'https://rskrf.ru/goods/sushki-malyshka-prostye-08d976/'
response_item = requests.get(item_url).text
item_soup = BeautifulSoup(response_item, 'lxml')
ratings = item_soup.select('.rating-item span')
safety = ratings[5].string
quality = ratings[7].string
total_score = ratings[1].string
print(ratings)
print(safety, quality, total_score)

