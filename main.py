import os

from config import COMPANY_NAMES
from src.api import HHAPI
from src.utils import get_vacancies_from_hh
from src.vacancy import Vacancy


def main():
    get_vacancies_from_hh()

    # if vacancies:
    #     print(f"Найдено {len(vacancies)} вакансий:")
    #     for vacancy in vacancies:
    #         print(vacancy.__dict__)
    #         # print(vacancy)
    # else:
    #     print("Вакансий не найдено.")


if __name__ == "__main__":
    main()
