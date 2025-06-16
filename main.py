import json

import requests
import psycopg2

#response = requests.get('https://api.hh.ru/vacancies', params={'text': 'Газпром нефть', 'per_page': 100})#, 'employer_id': 1122462})#, 'employer_id': (3529, 78638, 1740, 1122462, 3388)})
#with open('vacs.json', 'w') as f:
#    json.dump(response.json(),f)
##print(response.json())
#with open('vacs.json') as f:
#    vacs = json.load(f)
#for i in vacs['items']:
#    print(i['employer'])

connect = psycopg2.connect(
    host='localhost',
    database='Project 3',
    user='postgres',
    password='1303'
)

cursor = connect.cursor()
cursor.execute('SELECT * FROM employers')
rows = cursor.fetchall()
for row in rows:
    print(row)