import json
import os.path
from abc import ABC, abstractmethod
from json import JSONDecodeError

from config import DATA_DIR
from src.user_interaction import Vacancy


class BaseSaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy_by_vacancy_name(self, word):
        pass

    @abstractmethod
    def del_vacancy(self, vacancy):
        pass


class JSONSaver(BaseSaver):

    def __init__(self, filename="vacancies.json"):
        """Инициализатор класса JSONSaver"""
        self.__file_path = os.path.join(DATA_DIR, filename)

    def __save_to_file(self, vacancies: list[dict]) -> None:
        """Сохраняет данные в json-файл"""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False)

    def __read_file(self) -> list[dict]:
        """Считывает данные из json-файла"""
        try:
            with open(self.__file_path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        except JSONDecodeError:
            data = []

        return data

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл"""
        vacancies_list = self.__read_file()

        if vacancy.url not in [vac["url"] for vac in vacancies_list]:
            vacancies_list.append(vacancy.to_dict())
            self.__save_to_file(vacancies_list)

    def add_vacancies(self, vacancies: list[dict]) -> None:
        """Добавляет вакансии в файл"""
        self.__save_to_file(vacancies)

    def del_vacancy(self, url: str) -> None:
        """Удаляет вакансию из файла"""
        vacancies_list = self.__read_file()
        for index, vac in enumerate(vacancies_list):
            if vac["url"] == url:
                vacancies_list.pop(index)

        self.__save_to_file(vacancies_list)

    def get_vacancy_by_vacancy_name(self, word: str) -> list[Vacancy]:
        """Возвращает список вакансий по ключевому слову в названии вакансии"""
        found_vacancies = []

        for vac in self.__read_file():
            if word in vac.get("name").lower():
                found_vacancies.append(vac)

        return Vacancy.cast_to_object_list(found_vacancies)
