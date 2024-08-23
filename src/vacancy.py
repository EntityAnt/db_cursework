class Vacancy:
    def __init__(self, employer, title, city, salary_from, salary_to, currency, requirement, responsibility, schedule,
                 employment, url):
        self.employer = employer
        self.title = title
        self.city: str = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility
        self.schedule = schedule
        self.employment = employment
        self.url = url

    def __str__(self):
        return (f"Компания: {self.employer}, "
                f"Вакансия: {self.title}, "
                f"Город: {self.city}, "
                f"Зарплата от: {self.salary_from} до: {self.salary_to} {self.currency}, "
                f"Требования: {self.requirement}, "
                f"Ответственность: {self.responsibility}, "
                f"График: {self.schedule}, "
                f"Занятость: {self.employment}, "
                f"Ссылка: {self.url}")

    def __gt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError("Вакансию можно сравнивать только с вакансией!")
        return (self.salary_from, self.salary_to) > (other.salary_from, other.salary_to)
