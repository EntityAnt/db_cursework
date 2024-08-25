from config import config
from src.db_manager import DBManager
from src.postgres_db import DBPostgres
from src.utils import main_menu


def user_interaction() -> None:
    """Основная функция по взаимодействию с пользователем"""

    print("Здравствуйте! \nЭта программа по поиску и сравнению вакансий на HeadHunter. \n")
    print("Выберите пункт меню ")
    while True:
        answer = main_menu()
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
            pass
        elif answer == 4:
            pass
        elif answer == 5:
            pass
        elif answer == 6:
            print("Благодарим за использование программы.\n      До свидания.")
            break