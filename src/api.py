import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self, company_name):
        self.company_name = company_name

    def get_vacancies(self):
        params = {
            'text': f'company:{self.company_name}',
            'area': 113,
            'per_page': 20,  # Количество вакансий на странице
            'page': 0  # Номер страницы
        }
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return []
