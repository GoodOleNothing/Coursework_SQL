import psycopg2
import requests
import json
import tqdm


class DBManager:
    """Основной класс для работы с БД"""
    def __init__(self):  # подключение к pg
        self.connection = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='1303'
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.base_employers = {'СБЕР': 3529,
                               'Т-Банк': 78638,
                               'Газпром Банк': 3388,
                               'Альфа-Банк': 80,
                               'Банк ВТБ (ПАО)': 4181,
                               'Точка': 2324020,
                               'Почта Банк': 1049556,
                               'Россельхозбанк': 58320,
                               'Совкомбанк': 7944,
                               'Ozon': 2180}

    def create_db(self):  # Создание БД
        try:
            self.cursor.execute('DROP DATABASE IF EXISTS project_sql')
            self.cursor.execute('CREATE DATABASE project_sql')
        except Exception as e:
            print(e)
        self.connection.close()
        self.cursor.close()

    def create_tables(self):  # Создание таблиц
        self.connection = psycopg2.connect(
            host='localhost',
            database='project_sql',
            user='postgres',
            password='1303'
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        query_start_employers = """CREATE TABLE employers (
        employer_id serial PRIMARY KEY,
        employer_name varchar(30),
        number_of_vacancies int
        )"""
        query_start_vacancies = """CREATE TABLE vacancies (
        vacancy_id serial PRIMARY KEY,
        vacancy_name varchar(350),
        salary real,
        url varchar(350),
        employer_name varchar(30)

        CONSTRAINT chk_salary NOT NULL 
        )"""
        try:
            self.cursor.execute(query_start_employers)
            self.cursor.execute(query_start_vacancies)
        except Exception as e:
            print(e)
            pass

    def get_vacs(self):  # Сбор вакансий и заполнение таблиц
        for emp_name, emp_id in tqdm.tqdm(self.base_employers.items(), desc="Scaning employers"):
            results = []
            for i in range(0, 2):
                response = requests.get('https://api.hh.ru/vacancies', params={'page': i, 'per_page': 100,
                                                                               'only_with_salary': True,
                                                                               'employer_id': emp_id})
                data = response.json()
                results.extend(data.get('items', []))
            results_dict = {'items': results}
            with open('vacs.json', 'w') as f:
                json.dump(results_dict, f)
            with open('vacs.json') as f:
                vacs = json.load(f)

            self.cursor.execute(f'SELECT vacancy_name, url FROM vacancies')
            db_vacs = self.cursor.fetchall()
            new_vacs = {'items': [vac for vac in vacs['items'] if (vac['name'], vac['alternate_url']) not in db_vacs]}
            for vac in new_vacs['items']:
                if vac['salary'] is None:
                    pass
                elif vac['salary']['from'] is None:
                    pass
                else:
                    self.cursor.execute(f"INSERT INTO vacancies(vacancy_name,salary,url,employer_name) VALUES ('{vac['name']}', '{vac['salary']['from']}', '{vac['alternate_url']}', '{emp_name}')")
                    self.connection.commit()

            self.cursor.execute(f"SELECT COUNT(*) FROM vacancies WHERE employer_name = '{emp_name}'")
            counter = self.cursor.fetchone()[0]

            self.cursor.execute('SELECT * FROM employers')
            rows = self.cursor.fetchall()
            if not rows:
                self.cursor.execute(f"INSERT INTO employers(employer_name, number_of_vacancies) VALUES ('{emp_name}', '{counter}')")
                self.connection.commit()
            else:
                self.cursor.execute(f"SELECT employer_name FROM employers WHERE employer_name = '{emp_name}'")
                names = self.cursor.fetchall()
                if not names:
                    self.cursor.execute(f"INSERT INTO employers(employer_name, number_of_vacancies) VALUES ('{emp_name}', '{counter}')")
                    self.connection.commit()
                else:
                    pass

    def get_companies_and_vacancies_count(self):  # Получает список всех компаний и количество вакансий у каждой компании.
        self.cursor.execute('SELECT * FROM employers')
        employers = self.cursor.fetchall()
        for employer in employers:
            print(f'id: {employer[0]} - Название компании: {employer[1]} - Кол-во вакансий: {employer[2]}')
        print(f'\n')

    def get_all_vacancies(self):  # Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        self.cursor.execute('SELECT * FROM vacancies LEFT JOIN employers USING(employer_name) ORDER BY vacancy_id')
        vacancies = self.cursor.fetchall()
        for vacancy in vacancies:
            print(f'id: {vacancy[1]} - Вакансия: {vacancy[2]} - Зарплата: {vacancy[3]} - '
                  f'Ссылка: {vacancy[4]} - Название компании: {vacancy[0]}')
        print(f'\n')

    def get_avg_salary(self):  # Получает среднюю зарплату по вакансиям.
        self.cursor.execute('SELECT AVG(salary) FROM vacancies')
        avg_salary = self.cursor.fetchall()
        for salary in avg_salary:
            print(f'{salary[0]}')
        print(f'\n')

    def get_vacancies_with_higher_salary(self):  # Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        self.cursor.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
        high_salary = self.cursor.fetchall()
        for salary in high_salary:
            print(f'Высокая зарплата* id: {salary[0]} - Вакансия: {salary[1]} - Зарплата: {salary[2]}')
        print(f'\n')

    def get_vacancies_with_keyword(self): #получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        search_query = input('Ключевое слово: ')
        self.cursor.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{search_query}%' OR employer_name LIKE '%{search_query}%'")
        search_query = self.cursor.fetchall()
        for match in search_query:
            print(f'id: {match[0]} - Вакансия: {match[1]} - Зарплата: {match[2]}')
        print(f'\n')

    def exit(self):
        self.cursor.close()
        self.connection.close()
