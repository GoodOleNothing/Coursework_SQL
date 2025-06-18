
import psycopg2


class DBManager:

    def __init__(self): #подключение к БД
        self.connection = psycopg2.connect(
        host='localhost',
        database='Project 3',
        user='postgres',
        password='1303'
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self): #получает список всех компаний и количество вакансий у каждой компании.
        self.cursor.execute('SELECT * FROM employers')
        employers = self.cursor.fetchall()
        for employer in employers:
            print(f'id: {employer[0]} - Название компании: {employer[1]} - Кол-во вакансий: {employer[2]}')
        print(f'\n')

    def get_all_vacancies(self):#получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        self.cursor.execute('SELECT * FROM vacancies LEFT JOIN employers USING(employer_name)')
        vacancies = self.cursor.fetchall()
        for vacancy in vacancies:
            print(f'id: {vacancy[1]} - Вакансия: {vacancy[2]} - Зарплата: {vacancy[3]} - Название компании: {vacancy[0]}')
        print(f'\n')

    def get_avg_salary(self): #получает среднюю зарплату по вакансиям.
        self.cursor.execute('SELECT AVG(salary) FROM vacancies')
        avg_salary = self.cursor.fetchall()
        for salary in avg_salary:
            print(f'Средняя зарплата - {salary[0]}')
        print(f'\n')

    def get_vacancies_with_higher_salary(self): #получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        self.cursor.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
        high_salary = self.cursor.fetchall()
        for salary in high_salary:
            print(f'Высокая зарплата* id: {salary[0]} - Вакансия: {salary[1]} - Зарплата: {salary[2]}')
        print(f'\n')

    def get_vacancies_with_keyword(self): #получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        search_query = input('Ключевое слово: ')
        self.cursor.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{search_query}%' ")
        search_query = self.cursor.fetchall()
        for match in search_query:
            print(f'id: {match[0]} - Вакансия: {match[1]} - Зарплата: {match[2]}')
        print(f'\n')


db = DBManager()
db.get_companies_and_vacancies_count()
db.get_all_vacancies()
db.get_avg_salary()
db.get_vacancies_with_higher_salary()
db.get_vacancies_with_keyword()
