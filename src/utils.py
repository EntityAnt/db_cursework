import os

import psycopg2

from config import config, COMPANY_NAMES
from src.api import HHAPI
from src.vacancy import Vacancy


def get_vacancies_from_hh() -> list[dict]:
    """ Возвращает список словарей с вакансиями с hh.ru.
      В список попадут только те вакансии, компании которых есть в списке COMPANY_NAMES"""
    vacancies_data = []
    for company_name in COMPANY_NAMES:
        for page in range(1):
            hh_api = HHAPI(company_name, page)
            vacancies_data += hh_api.get_vacancies()

    vacancies = []
    for item in vacancies_data:
        employer = item.get('employer')['name']
        for company_name in COMPANY_NAMES:
            if company_name.lower() in employer.lower():
                title = item['name']
                city = item.get("area")["name"]
                employment = item.get('employment')['name']
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
                requirement = item.get('snippet')['requirement']
                responsibility = item.get('snippet')['responsibility']
                schedule = item.get('schedule')['name']
                url = item['alternate_url']
                vacancy = Vacancy(employer, title, city, salary_from, salary_to, currency, requirement, responsibility,
                                  schedule, employment, url)
                # print(vacancy)
                vacancies.append(vacancy)
    return vacancies


class DBPostgres:
    """ Класс для создания и заполнения БД PostgresSQL. """

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def create_db(self):
        """ Создает базу данных и таблицы. """

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.db_name};")
        cur.execute(f"CREATE DATABASE {self.db_name};")

        conn.close()

        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE companies (company_id SERIAL PRIMARY KEY, company_name VARCHAR(255) NOT NULL)")

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        company_id INT REFERENCES companies(company_id),
                        vacancy_name VARCHAR NOT NULL,
                        city VARCHAR(100) NOT NULL,
                        salary_from INT,
                        salary_to INT,
                        currency VARCHAR(5),
                        requirement TEXT,
                        responsibility TEXT,
                        schedule VARCHAR(30),
                        employment VARCHAR(30),
                        url TEXT
                    )""")
        conn.commit()
        conn.close()

    def save_data_to_db(self):
        """ Записывает данные в базу данных."""
        vacancies = get_vacancies_from_hh()
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            for vacancy in vacancies:
                vac_dict = vacancy.__dict__

                employer = vac_dict.get('employer')
                cur.execute("INSERT INTO companies (company_name) VALUES (%s) RETURNING company_id", employer)
                company_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO vacancies (
                    vacancy_name,
                    city,
                    salary_from,
                    salary_to,
                    currency,
                    requirement,
                    responsibility,
                    schedule,
                    employment,
                    url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                vac_dict.get('title'),
                                vac_dict.get('city'),
                                vac_dict.get('salary_from'),
                                vac_dict.get('salary_to'),
                                vac_dict.get('currency'),
                                vac_dict.get('requirement'),
                                vac_dict.get('responsibility'),
                                vac_dict.get('schedule'),
                                vac_dict.get('employment'),
                                vac_dict.get('url')
                            )
                            )
        conn.commit()
        conn.close()


if __name__ == '__main__':
    params = config()
    db = DBPostgres('hh_db', params)
    db.create_db()
    db.save_data_to_db()
