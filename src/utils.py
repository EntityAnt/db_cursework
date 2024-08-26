import psycopg2
from psycopg2 import sql

from config import COMPANY_NAMES, config
from src.api import HHAPI
from src.vacancy import Vacancy


def get_vacancies_from_hh() -> list[dict]:
    """Возвращает список словарей с вакансиями с hh.ru.
    В список попадут только те вакансии, компании которых есть в списке COMPANY_NAMES"""
    vacancies_data = []
    for company_name in COMPANY_NAMES:
        for page in range(1):
            hh_api = HHAPI(company_name, page)
            vacancies_data += hh_api.get_vacancies()

    vacancies = []
    for item in vacancies_data:
        employer = item.get("employer")["name"]
        for company_name in COMPANY_NAMES:
            if company_name.lower() in employer.lower():
                employer_url = item.get("employer")["alternate_url"]
                title = item["name"]
                city = item.get("area")["name"]
                employment = item.get("employment")["name"]
                if item["salary"]:
                    salary = item["salary"]
                    currency = salary.get("currency")
                    if salary["from"]:
                        salary_from = salary["from"]
                    else:
                        salary_from = 0
                    if salary["to"]:
                        salary_to = salary["to"]
                    else:
                        salary_to = 0
                else:
                    salary_from = 0
                    salary_to = 0
                    currency = "RUR"
                requirement = item.get("snippet")["requirement"]
                responsibility = item.get("snippet")["responsibility"]
                schedule = item.get("schedule")["name"]
                url = item["alternate_url"]
                vacancy = Vacancy(
                    employer,
                    employer_url,
                    title,
                    city,
                    salary_from,
                    salary_to,
                    currency,
                    requirement,
                    responsibility,
                    schedule,
                    employment,
                    url,
                )
                vacancies.append(vacancy)
    return vacancies


def check_database_exists(db_name: str) -> bool:
    """Принимает имя БД, возвращает True если БД существует, False если нет."""
    try:
        # Подключение к серверу PostgreSQL без указания конкретной базы данных
        params = config()
        connection = psycopg2.connect(**params)
        connection.autocommit = True
        cursor = connection.cursor()

        # Выполнение запроса для проверки существования базы данных
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name]
        )
        exists = cursor.fetchone() is not None

        cursor.close()

        return exists
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных:", e)
        return False
    finally:
        if connection:
            connection.close()


def valid_input(message: str) -> int | None:
    """Если возможно, переводит str в int, иначе предлагает ввести число."""
    while True:
        count = input(message).strip()
        if count.isdigit():
            return int(count)
        else:
            print("Можно ввести только целое число")


def main_menu() -> int:
    """Реализация главного меню, возвращает номер меню"""
    print("1 - Создать базу данных и таблицы.\n" "2 - Подключится к существующей БД \n")
    while True:
        answer = input("Выберите действие: ").strip()
        if answer.isdigit():
            answer = int(answer)
            if 1 <= answer <= 2:
                break
            else:
                print("Можно ввести только число от 1 до 2!")
        else:
            print("Можно ввести только целое число")
    print("*" * 50)
    return answer


def submenu() -> int:
    """Реализация подменю, возвращает номер меню"""

    print(
        "1 - Получить вакансии с hh.ru и записать их в БД.\n"
        "2 - Получить список всех компаний и количество вакансий у каждой компании. \n"
        "3 - Получить список всех вакансий.\n"
        "4 - Получить среднюю зарплату по вакансиям.\n"
        "5 - Получить список всех вакансий, у которых зарплата выше средней.\n"
        "6 - Получить список вакансий по ключевым словам.\n"
        "7 - Предыдущее меню.\n"
        "8 - Выход.\n"
    )

    while True:
        answer = input("Выберите действие: ").strip()
        if answer.isdigit():
            answer = int(answer)
            if 1 <= answer <= 8:
                break
            else:
                print("Можно ввести только число от 1 до 8!")
        else:
            print("Можно ввести только целое число")
    print("*" * 50)
    return answer
