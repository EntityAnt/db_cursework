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
                employer_url = item.get('employer')['alternate_url']
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
                vacancy = Vacancy(employer, employer_url, title, city, salary_from, salary_to, currency, requirement,
                                  responsibility, schedule, employment, url)
                vacancies.append(vacancy)
    return vacancies
