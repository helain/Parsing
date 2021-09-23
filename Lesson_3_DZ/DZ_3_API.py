import json
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Lesson_3_DZ']

url = 'https://api.hh.ru/vacancies/'
site_url = 'https://hh.ru/'
headers = {'User-agent': 'Chrome/93.0.4577.82'}

"""функция 1го поиска. Ограничение API: 2000 результатов. Параметр area=1 выводит вакансии по Москве"""


def search_vacancies(f_url, f_site_url):
    for i in range(20):
        response = requests.get(f_url, headers=headers, params={'per_page': 100, 'page': i, 'area':1})
        data = json.loads(response.text)
        for item in data['items']:
            name = item['name']
            if item['salary']:
                min_salary = item['salary']['from']
                max_salary = item['salary']['to']
            else:
                min_salary = None
                max_salary = None
            vacancy_url = item['alternate_url']
            site_id = item['id']
            db.hh_vacancies.insert_one(
                {'name': name, 'min_salary': min_salary, 'max_salary': max_salary, 'vacancy_url': vacancy_url,
                 'site_url': f_site_url, 'site_id': site_id})


def search_by_min_salary(value):
    for item in db.hh_vacancies.find({'$and': [{'max_salary': {'$gt': value}}, {'min_salary': {'$gt': value}}]}):
        print(item)


"""функция добавления новых документов. Ограничение API: 2000 результатов. Параметр area=2 выводит вакансии по Санкт-Петербургу"""
def add_new_vacancy(f_url, f_site_url):
    count = 0
    for i in range(20):
        response = requests.get(f_url, headers=headers, params={'per_page': 100, 'page': i, 'area':2})
        data = json.loads(response.text)
        for item in data['items']:
            name = item['name']
            if item['salary']:
                min_salary = item['salary']['from']
                max_salary = item['salary']['to']
            else:
                min_salary = None
                max_salary = None
            vacancy_url = item['alternate_url']
            site_id = item['id']
            serc = []
            for item in db.hh_vacancies.find({'site_id': site_id}):
                serc.append(item)
            if not serc:
                db.hh_vacancies.insert_one(
                {'name': name, 'min_salary': min_salary, 'max_salary': max_salary, 'vacancy_url': vacancy_url,
                 'site_url': f_site_url, 'site_id': site_id})
                count += 1
    print(f'Добавлено {count} документов')

# search_vacancies(url, site_url)
# search_by_min_salary(500000)
# add_new_vacancy(url, site_url)


