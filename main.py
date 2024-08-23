import os

from config import COMPANY_NAMES
from src.api import HHAPI
from src.utils import get_vacancies_from_hh
from src.vacancy import Vacancy


def main():
    vacancies_data = get_vacancies_from_hh()

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
                vacancies.append(
                    Vacancy(employer, title, city, salary_from, salary_to, currency, requirement, responsibility,
                            schedule,
                            employment, url))

    if vacancies:
        print(f"Найдено {len(vacancies)} вакансий:")
        for vacancy in vacancies:
            print(vacancy)
    else:
        print("Вакансий не найдено.")


if __name__ == "__main__":
    main()
