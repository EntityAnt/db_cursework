from config import config
from src.db_manager import DBManager
from src.postgres_db import DBPostgres
from src.utils import submenu, main_menu, check_database_exists


def interaction_main_menu() -> DBPostgres:
    while True:
        answer = main_menu()

        if answer == 1:
            db_name = input('Введите название БД: ')
            params = config()

            if check_database_exists(db_name):
                print(f'База данных с именем {db_name} уже существует!')
                print('*' * 50)
            else:
                db = DBPostgres(db_name, params)
                db.create_db()
                db.create_tables()
                print('*' * 50)
                print(f'Создана база данных с именем {db_name}!')
                print('+' * 50)
                return db

        elif answer == 2:
            db_name = input('Введите название БД: ')

            if not check_database_exists(db_name):
                print(f'База данных с именем {db_name} не существует!')
                print('*' * 50)
            else:
                params = config()
                db = DBPostgres(db_name, params)
                print(f'Вы подключились к базе данных с именем {db_name}!')
                print('*' * 50)
                return db


def user_interaction() -> None:
    """Основная функция по взаимодействию с пользователем"""

    print("Здравствуйте! \nЭта программа по поиску вакансий с HeadHunter. \n")
    print("Выберите пункт меню ")
    db = interaction_main_menu()

    while True:
        answer = submenu()
        if answer == 1:
            db.save_data_to_db()
            print("\nДанные получены и записаны в БД!")
            print('*' * 50)
        elif answer == 2:
            db = DBManager()
            db.get_companies_and_vacancies_count()
        elif answer == 3:
            db = DBManager()
            db.get_all_vacancies()
        elif answer == 4:
            db = DBManager()
            db.get_avg_salary()
        elif answer == 5:
            db = DBManager()
            db.get_vacancies_with_higher_salary()
        elif answer == 6:
            keywords = input('Введите слова через запятую: ').split(',')
            db = DBManager()
            db.get_vacancies_with_keyword(keywords)
        elif answer == 7:
            db = interaction_main_menu()
        elif answer == 8:
            print("Благодарим за использование программы.\n      До свидания.")
            break
