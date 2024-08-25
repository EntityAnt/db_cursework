from config import config
from src.db_manager import DBManager
from src.postgres_db import DBPostgres
from src.utils import submenu


def user_interaction() -> None:
    """Основная функция по взаимодействию с пользователем"""

    print("Здравствуйте! \nЭта программа по поиску вакансий с HeadHunter. \n")
    print("Выберите пункт меню ")
    while True:
        answer = submenu()
        if answer == 1:
            params = config()
            db = DBPostgres('hh_db', params)
            db.create_db()
            db.save_data_to_db()
            print("\nДанные получены и записаны в БД!")
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
            print("Благодарим за использование программы.\n      До свидания.")
            break