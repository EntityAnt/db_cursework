import os

import psycopg2

from config import config, COMPANY_NAMES
from src.api import HHAPI


def get_vacancies_from_hh() -> list[dict]:
    vacancies_data = []
    for company_name in COMPANY_NAMES:
        for page in range(1):
            hh_api = HHAPI(company_name, page)
            vacancies_data += hh_api.get_vacancies()
    return vacancies_data


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
            cur.execute("CREATE TABLE companies (company_id SERIAL PRIMARY KEY, company_name VARCHAR(255) NOT NULL)")

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


if __name__ == '__main__':
    params = config()
    db = DBPostgres('hh_db', params)
    db.create_db()
