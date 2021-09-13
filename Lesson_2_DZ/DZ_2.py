import pandas as pd
import lxml
from bs4 import BeautifulSoup
import requests

url = 'https://rskrf.ru/ratings/produkty-pitaniya/'

name_list = []
category_list = []
subcategory_list = []
safety_list = []
quality_list = []
total_score_list = []

response = requests.get(url).text
soup = BeautifulSoup(response, 'lxml')
category = soup.select('.category-item a')

for category_item in category:
    subcategory_url = f"https://rskrf.ru{category_item['href']}"
    """получение категории"""
    category_name = category_item.find(class_='h5').string
    response_sub = requests.get(subcategory_url).text
    sub_soup = BeautifulSoup(response_sub, 'lxml')
    subcategory = sub_soup.select('.category-item a')
    for subcategory_item in subcategory:
        items_url = f"https://rskrf.ru{subcategory_item['href']}"
        """получение подкатегории"""
        subcategory_name = subcategory_item.find(class_='d-xl-block d-none').string

        response_items = requests.get(items_url).text
        items_soup = BeautifulSoup(response_items, 'lxml')
        items = items_soup.select('noscript a')
        for item in items:
            item_url = f"https://rskrf.ru{item['href']}"
            """получение имени"""
            item_name = item.string[:-8]

            response_item = requests.get(item_url).text
            item_soup = BeautifulSoup(response_item, 'lxml')
            ratings = item_soup.select('.rating-item span')
            """получение значений рейтинга - безопасность, качество, общий рейтинг"""
            safety = ratings[5].string
            quality = ratings[7].string
            total_score = ratings[1].string
            """запись значений в списки"""
            name_list.append(item_name)
            category_list.append(category_name)
            subcategory_list.append(subcategory_name)
            safety_list.append(safety)
            quality_list.append(quality)
            total_score_list.append(total_score)
"""формируем словарь"""

rskrf_dict = {'Name':name_list,
              'Category':category_list,
              'Subcategory':subcategory_list,
              'Safety_rating':safety_list,
              'Quality_rating':quality_list,
              'Total_rating':total_score_list}

rskrf_data = pd.DataFrame(rskrf_dict, index=False)
rskrf_data.to_csv('rskrf_result.csv')

