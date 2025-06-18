import json
import requests
import psycopg2

"""Служебный скрипт для заполнения базы данных"""
def get_vacs(employer='Ozon', quantity=100):
    emps = {'СБЕР': 3529,
            'Т-Банк': 78638,
            'Газпром Банк': 3388,
            'Альфа-Банк': 80,
            'Банк ВТБ (ПАО)': 4181,
            'Точка': 2324020,
            'Почта Банк': 1049556,
            'Россельхозбанк': 58320,
            'Совкомбанк': 7944,
            'Ozon': 2180}

    response = requests.get('https://api.hh.ru/vacancies', params={'per_page': quantity, 'only_with_salary': True,
                                                                   'employer_id': emps[employer]})
    with open('vacs.json', 'w') as f:
        json.dump(response.json(), f)

    connection = psycopg2.connect(
       host='localhost',
       database='Project 3',
       user='postgres',
       password='1303'
    )
    cursor = connection.cursor()

    with open('vacs.json') as f:
        vacs = json.load(f)

    cursor.execute(f"DELETE FROM vacancies WHERE employer_name = '{employer}'")
    connection.commit()
    counter = 0
    for i in vacs['items']:
        if i['salary'] is None:
            pass
        elif i['salary']['from'] is None:
            pass
        else:
            counter += 1
            cursor.execute(f"INSERT INTO vacancies(name,salary,url,employer_name) VALUES ('{i['name']}', '{i['salary']['from']}', '{i['alternate_url']}', '{employer}')")
            connection.commit()

    cursor.execute('SELECT * FROM employers')
    rows = cursor.fetchall()
    if not rows:
        cursor.execute(f"INSERT INTO employers(employer_name, number_of_vacancies) VALUES ('{employer}','{counter}')")
        connection.commit()
    else:
        cursor.execute(f"SELECT employer_name FROM employers WHERE employer_name = '{employer}'")
        names = cursor.fetchall()
        if not names:
            cursor.execute(f"INSERT INTO employers(employer_name, number_of_vacancies) VALUES ('{employer}','{counter}')")
            connection.commit()
        else:
            pass

    cursor.execute('SELECT * FROM employers')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connection.close()


def find_employer():
    response = requests.get('https://api.hh.ru/vacancies', params={'text': 'Мобильный менеджер в пространство Ozon Банка', 'per_page': 100})#, 'employer_id': 2324020})
    resp = response.json()
    for r in resp['items']:
        print(r['employer'])


get_vacs()
#find_employer()