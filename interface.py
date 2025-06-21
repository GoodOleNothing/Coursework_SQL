from main import DBManager


def interface():
    """Функция создания интерфейса для пользователя"""
    print(f'Выберите действие\n1 - Получить список всех компаний и количество вакансий у каждой компании\n'
          f'2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n'
          f'3 - Получить среднюю зарплату по вакансиям\n'
          f'4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
          f'5 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова\n'
          f'создать - Создать БД\n'
          f'обновить - Обновить БД\n'
          f'Для выхода введите "выход"')
    user_input = input('Ввод: ')

    options = ['1', '2', '3', '4', '5', 'выход', 'обновить', 'создать']
    db = DBManager()
    while user_input.lower() != 'выход':
        if user_input == '1':
            print('Список всех компаний и количество вакансий у каждой компании')
            db.get_companies_and_vacancies_count()
        elif user_input == '2':
            print('Список всех вакансий с указанием названия компании, '
                  'названия вакансии и зарплаты и ссылки на вакансию')
            db.get_all_vacancies()
        elif user_input == '3':
            print('Средняя зарплата по вакансиями')
            db.get_avg_salary()
        elif user_input == '4':
            print('Список всех вакансий, у которых зарплата выше средней по всем вакансиям')
            db.get_vacancies_with_higher_salary()
        elif user_input == '5':
            print('Список всех вакансий, в названии которых содержатся переданные в метод слова')
            db.get_vacancies_with_keyword()
        elif user_input == 'создать':
            print('Создать БД')
            db.create_db()
            db.create_tables()
        elif user_input == 'обновить':
            try:
                print('Обновить БД')
                db.get_vacs()
            except Exception as e:
                print(e)
        elif user_input.lower() not in options:
            print('Выберите номер из списка или введите "выход"')
        user_input = input('Выберите действие\nВвод: ')
    else:
        db.exit()


interface()
