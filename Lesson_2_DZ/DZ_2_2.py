"""Росконтроль"""
#импорт модулей
import pandas as pd
import lxml
from bs4 import BeautifulSoup
import requests

url = 'https://roscontrol.com/category/produkti/'

name_list = []
category_list = []
subcategory_list = []
safety_list = []
quality_list = []
total_score_list = []

response = requests.get(url).text
soup = BeautifulSoup(response, 'lxml')
category = soup.select('.catalog__category-item')

for category_item in category:
    subcategory_url = f"https://roscontrol.com{category_item['href']}"
    # """получение категории"""
    category_name = category_item.find(class_='catalog__category-name').string
    response_sub = requests.get(subcategory_url).text
    sub_soup = BeautifulSoup(response_sub, 'lxml')
    subcategory = sub_soup.select('.catalog__category-item')
    for subcategory_item in subcategory:
        items_url = f"https://roscontrol.com{subcategory_item['href']}"
    #     """получение подкатегории"""
        subcategory_name = subcategory_item.find(class_='catalog__category-name').string
        for i in range(1, 6):
            response_items = requests.get(items_url, params={'page':i}).text
            items_soup = BeautifulSoup(response_items, 'lxml')
            items = items_soup.select('.block-product-catalog__item')
            for item in items:
                item_url = f"https://roscontrol.com{item['href']}"
                """получение имени"""
                item_name = item.find(class_='product__item-link').string
                try:
                    response_item = requests.get(item_url).text
                    item_soup = BeautifulSoup(response_item, 'lxml')
                except: pass
                """получение значений рейтинга - безопасность, качество, общий рейтинг"""
                try:
                    total_score = item_soup.find(class_='total green').string
                    ratings = item_soup.select('.rate-item__value span')
                    safety = ratings[0].string
                    quality = ratings[3].string
                except: pass
                """запись значений в списки"""
                name_list.append(item_name)
                category_list.append(category_name)
                subcategory_list.append(subcategory_name)
                safety_list.append(safety)
                quality_list.append(quality)
                total_score_list.append(total_score)

"""формируем словарь"""

roscontrol_dict = {'Name':name_list,
              'Category':category_list,
              'Subcategory':subcategory_list,
              'Safety_rating':safety_list,
              'Quality_rating':quality_list,
              'Total_rating':total_score_list}

roscontrol_data = pd.DataFrame(roscontrol_dict)
roscontrol_data.to_csv('roscontrol_result.csv')