class DBManager:
    """ Класс для получения данных и БД """

    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """ Возвращает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self) -> list[dict]:
        """ Возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self) -> list[dict]:
        """ Возвращает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_keyword(self) -> list[dict]:
        """ Возвращает список всех вакансий, в названии которых содержатся переданные в
        метод слова, например python."""
        pass
