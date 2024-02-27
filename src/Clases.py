import csv
from abc import ABC, abstractmethod
import requests


class AbstractApi(ABC):
    @abstractmethod
    def get_vacancies(self, key_word):
        pass


class HeadHunterAPI(AbstractApi):
    def __init__(self):
        self._vacancy = []
        self._json_vacancy = []

    def get_vacancies(self, key_word):
        url = 'https://api.hh.ru/vacancies'
        params = {'text': key_word, 'area': 113, 'per_page': 3}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            vacancies = response.json()
            self._json_vacancy = vacancies["items"]
            return vacancies
        else:
            print(f"Ошибка при запросе к API HeadHunter: {response.status_code}")
            return None

    def convert_to_vacancy(self):
        currency = {"RUR": " руб.", "EUR": " евро.", "USD": " доллар."}
        for vacancies in self._json_vacancy:
            try:
                salary_from = vacancies["salary"]["from"]
            except:
                salary_from = None
            try:
                salary_to = vacancies["salary"]["to"]
            except:
                salary_to = None
            if salary_from is None and salary_to is None:
                salary = ""
            elif salary_from is None:
                salary = str(vacancies["salary"]["to"]) +\
                          currency[vacancies["salary"]["currency"]]
            elif salary_to is None:
                salary = str(vacancies["salary"]["from"]) +\
                          currency[vacancies["salary"]["currency"]]
            else:
                salary = (str(vacancies["salary"]["from"]) + "-"
                          + str(vacancies["salary"]["to"])
                          + currency[vacancies["salary"]["currency"]])
            self._vacancy.append(Vacancy(vacancies["name"],
                                         vacancies["url"],
                                         salary,
                                         vacancies["snippet"]["requirement"]))

    def show_vacancy(self):
        for vacancy in self._vacancy:
            print(vacancy)

    def send_vacancies(self):
        return self._vacancy


class Vacancy(object):
    def __init__(self, name, link, salary, info):
        self._name = name
        self._link = link
        self._salary = salary
        self._info = info

    def __str__(self):
        return f"{self._name}, {self._link}, {self._salary}, {self._info}"

    def get_data(self):
        return {"Ваканcия": self._name,
                "Ссылка": self._link,
                "Зарплата": self._salary,
                "Требования": self._info}


class AbstractJson(ABC):
    @abstractmethod
    def read(self, path):
        pass

    @abstractmethod
    def write(self, path):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary):
        pass


class JSONSaver(AbstractJson):
    def __init__(self):
        self._vacancies = []

    def read(self, path):
        pass

    def write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            fieldnames = ["Ваканcия", "Ссылка", "Зарплата", "Требования"]
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Запись заголовка
            csv_writer.writeheader()
            for vacancy in self._vacancies:
                print(vacancy.get_data())
                csv_writer.writerow(vacancy.get_data())

    def add_vacancy(self, vacancies):
        self._vacancies = vacancies

    def delete_vacancy(self, vacancy):
        pass

    def get_vacancies_by_salary(self, salary):
        pass






hh_api = HeadHunterAPI()
hh_vacancies = hh_api.get_vacancies("Python")
hh_api.convert_to_vacancy()
hh_api.show_vacancy()
js = JSONSaver()
js.add_vacancy(hh_api.send_vacancies())
js.write("123.csv")