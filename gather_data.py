import json
import requests
import psycopg2


def get_vacs(data, employer='сбер', quantity=100):
    emps = {'сбер': 3529,
            'т-банк': 78638}

    if data == 'new':
        response = requests.get('https://api.hh.ru/vacancies', params={'text': '', 'per_page': quantity, 'employer_id': emps[employer.lower()]})#, 'employer_id': (3529, 78638, 1740, 1122462, 3388)})
        with open('vacs.json', 'w') as f:
            json.dump(response.json(),f)

    connection = psycopg2.connect(
       host='localhost',
       database='Project 3',
       user='postgres',
       password='1303'
    )
    cursor = connection.cursor()

    if data == 'new':
        cursor.execute(f'INSERT INTO employers(name, number_of_vacancies) VALUES {employer,quantity}')
        connection.commit()

    cursor.execute('SELECT * FROM employers')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connection.close()


get_vacs('saved')
