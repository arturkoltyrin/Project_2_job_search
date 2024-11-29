import json
import os
from abc import ABC, abstractmethod

from src.operations_with_vacancies import (OperationsWithVacancies,
                                           SalaryOfVacancies)


class AbstractSave(ABC):
    """Абстрактный класс, реализующий метод для добавления вакансий в файл"""

    @abstractmethod
    def _save_data(self):
        """Метод для добавления вакансий в файл"""
        pass


class AbstractGet(ABC):
    """Абстрактный класс, реализующий метод для получения данных из файла по указанным критериям"""

    @abstractmethod
    def _get_data(self):
        """Метод для получения данных из файла по указанным критериям"""
        pass


class AbstractDelete(ABC):
    """Абстрактный класс, реализующий метод для удаления информации о вакансиях"""

    @abstractmethod
    def _delete_data(self):
        """Метод для удаления информации о вакансиях"""
        pass


class SaveData(SalaryOfVacancies, OperationsWithVacancies, AbstractSave):
    """Класс для работы с добавления информации о вакансиях в JSON-файл"""

    def __init__(
        self,
        keyword: str,
        keyword_2: str,
        employment: str,
        currency: str,
        pay_from: int,
        pay_to: int,
        file: str = r"C:\Users\user\PycharmProjects\Project_2_job_search\data\vacancies.json",
    ):
        """Метод-конструктор"""
        super().__init__(keyword, keyword_2, employment, currency, pay_from, pay_to)
        self.__file = file

    def _save_data(self):
        """Метод для добавления вакансий в файл"""
        # Проверяем существует ли файл, если нет, создаем новый
        if not os.path.exists(self.__file):
            with open(self.__file, "w", encoding="utf-8") as f:
                json.dump([], f)  # Инициализируем файл пустым списком

        try:
            with open(self.__file, "r", encoding="utf-8") as file:
                try:
                    data_from_json_file = json.load(file)
                except json.decoder.JSONDecodeError:
                    data_from_json_file = []

            vacancies = self._comparison_pay()
            if vacancies is not None:
                for vacancy in vacancies:
                    if vacancy not in data_from_json_file:
                        data_from_json_file.append(vacancy)

                with open(self.__file, "w", encoding="utf-8") as f:
                    json.dump(data_from_json_file, f, ensure_ascii=False)
                return vacancies
            else:
                return []

        except Exception as e:
            print(f"Ошибка в классе SaveData: {e}")
            return None


class GetData(OperationsWithVacancies, AbstractGet):
    """Класс для получения информации из в JSON-файла"""

    def __init__(
        self,
        keyword: str,
        keyword_2: str,
        employment: str,
        currency: str,
        pay_from: int,
        pay_to: int,
        file: str = r"C:\Users\user\PycharmProjects\Project_2_job_search\data\vacancies.json",
    ):
        """Метод-конструктор"""
        super().__init__(keyword, keyword_2, employment, currency, pay_from, pay_to)
        self.__file = file

    def _get_data(self):
        """Метод для получения данных из файла по критериям"""
        if not os.path.exists(self.__file):
            return "Файл не найден"

        try:
            with open(self.__file, "r", encoding="utf-8") as file:
                data_from_json_file = json.load(file)

            vacations = []
            for vacancy in data_from_json_file:
                if (
                    self._keyword_2 in vacancy.get("name", "")
                    and self._employment in vacancy["employment"].get("name", "")
                    and self._currency in vacancy["salary"].get("currency", "")
                    and vacancy["salary"].get("from", 0) >= self._pay_from
                    and vacancy["salary"].get("to", 0) <= self._pay_to
                ):
                    vacations.append(vacancy)

            return vacations if vacations else "Работа не найдена"

        except Exception as e:
            print(f"Ошибка в классе GetData: {e}")
            return None


class DeleteData(OperationsWithVacancies, AbstractDelete):
    """Класс для очистки JSON-файла"""

    def __init__(
        self,
        keyword: str,
        keyword_2: str,
        employment: str,
        currency: str,
        pay_from: int,
        pay_to: int,
        file: str = r"C:\Users\user\PycharmProjects\Project_2_job_search\data\vacancies.json",
    ):
        """Метод-конструктор"""
        super().__init__(keyword, keyword_2, employment, currency, pay_from, pay_to)
        self.__file = file

    def _delete_data(self):
        """Метод для удаления информации о вакансиях"""
        if os.path.exists(self.__file):
            with open(self.__file, "w", encoding="utf-8") as file:
                json.dump([], file)  # Очищаем файл, записывая пустой список
            return f"Файл {self.__file} очищен"
        else:
            return f"Файл {self.__file} не найден"
