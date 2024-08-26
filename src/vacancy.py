class Vacancy:
    """Класс для создания вакансии."""

    def __init__(
        self,
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
    ):
        self.employer = employer
        self.employer_url = employer_url
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
        """Строковое представление вакансии."""
        return (
            f"Компания: {self.employer}, "
            f"Ссылка на компанию: {self.employer_url},"
            f"Вакансия: {self.title}, "
            f"Город: {self.city}, "
            f"Зарплата от: {self.salary_from} до: {self.salary_to} {self.currency}, "
            f"Требования: {self.requirement}, "
            f"Ответственность: {self.responsibility}, "
            f"График: {self.schedule}, "
            f"Занятость: {self.employment}, "
            f"Ссылка: {self.url}"
        )

    def __gt__(self, other) -> bool:
        """Сравнение вакансий."""
        if not isinstance(other, Vacancy):
            raise TypeError("Вакансию можно сравнивать только с вакансией!")
        return (self.salary_from, self.salary_to) > (other.salary_from, other.salary_to)
