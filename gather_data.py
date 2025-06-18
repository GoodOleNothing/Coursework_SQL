import json
import requests
import psycopg2


def get_vacs(employer='Газпром банк', quantity=100):
    employer = employer.lower().capitalize()
    emps = {'Сбер': 3529,
            'Т-банк': 78638,
            'Газпром банк': 3388}

    response = requests.get('https://api.hh.ru/vacancies', params={'text': '', 'per_page': quantity, 'employer_id': emps[employer]})#, 'employer_id': (3529, 78638, 1740, 1122462, 3388)})
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
    response = requests.get('https://api.hh.ru/vacancies', params={'text': '', 'per_page': 50})#, 'employer_id': (3529)})
    resp = response.json()
    for r in resp['items']:
        print(r['employer'])


get_vacs()
#find_employer()