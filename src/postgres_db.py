import psycopg2

from src.utils import get_vacancies_from_hh


class DBPostgres:
    """Класс для создания и заполнения БД PostgresSQL."""

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def create_db(self):
        """Создает базу данных."""

        """ Подключаемся к  PostgreSQL"""
        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        """ Создаем базу данных """
        cur.execute(f"DROP DATABASE IF EXISTS {self.db_name};")
        cur.execute(f"CREATE DATABASE {self.db_name};")
        conn.close()

    def create_tables(self):
        """Создает таблицы в базе данных."""
        # Подключаемся к БД
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """ CREATE TABLE companies (
                    company_id SERIAL PRIMARY KEY, 
                    company_name VARCHAR(255) NOT NULL UNIQUE,
                    company_url TEXT
                )"""
            )

        with conn.cursor() as cur:
            cur.execute(
                """
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
                    )"""
            )
        conn.commit()
        conn.close()

    def save_data_to_db(self):
        """Записывает данные в базу данных."""
        vacancies = get_vacancies_from_hh()
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            try:
                for vacancy in vacancies:
                    print(vacancy)
                    vac_dict = vacancy.__dict__
                    company_name = vac_dict.get("employer")
                    employer_url = vac_dict.get("employer_url")
                    """ Заполняем таблицу companies"""
                    cur.execute(
                        """
                        INSERT INTO companies (company_name, company_url)
                        VALUES (%s, %s)
                        ON CONFLICT (company_name) DO NOTHING
                        RETURNING company_id;
                        """,
                        (
                            company_name,
                            employer_url,
                        ),
                    )
                    try:
                        company_id = cur.fetchone()[0]
                    except Exception:
                        pass

                    """ Заполняем таблицу vacancies"""
                    cur.execute(
                        """INSERT INTO vacancies (
                        company_id,
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
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            company_id,
                            vac_dict.get("title"),
                            vac_dict.get("city"),
                            vac_dict.get("salary_from"),
                            vac_dict.get("salary_to"),
                            vac_dict.get("currency"),
                            vac_dict.get("requirement"),
                            vac_dict.get("responsibility"),
                            vac_dict.get("schedule"),
                            vac_dict.get("employment"),
                            vac_dict.get("url"),
                        ),
                    )
                    conn.commit()
            except Exception as ex:
                print(ex)
                conn.rollback()
            finally:
                conn.close()
