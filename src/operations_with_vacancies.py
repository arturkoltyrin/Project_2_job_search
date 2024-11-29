from abc import ABC, abstractmethod
from typing import Any, List

from src.get_vacancies import GetVacancies


class AbstractOperation(ABC):
    """Абстрактный класс для работы с полученными вакансиями"""

    @abstractmethod
    def _filtered_vacancies(self):
        """Метод, который должен быть в подклассе"""
        pass


class AbstractSalary(ABC):
    """Абстрактный класс для получения средней зарплаты в полученных вакансиях"""

    @abstractmethod
    def _avg(self) -> None:
        """Метод, который должен быть в дочернем классе"""
        pass


class OperationsWithVacancies(GetVacancies):
    """Класс для работы с вакансиями"""

    __slots__ = ("keyword", "keyword_2", "employment", "currency", "pay_from", "pay_to")

    def __init__(self, keyword: str, keyword_2: str, employment: str, currency: str, pay_from: int, pay_to: int):
        """Класс-конструктор, который получает атрибуты"""
        super().__init__(keyword)
        self._loading()
        self._keyword_2 = keyword_2
        self._employment = employment
        self._currency = currency
        if pay_from < 0:
            raise ValueError("Зарплата ОТ не должна быть отрицательной")
        self._pay_from = pay_from
        if pay_to < pay_from:
            raise ValueError("Зарплата ДО не должна быть меньше зарплаты ОТ")
        self._pay_to = pay_to
        self._sorted_vacancies: List = []

    def _filtered_vacancies(self) -> list:
        """Метод, который выбирает вакансии по фильтрам"""
        try:
            for vacancy in self._vacancies:
                if (
                    vacancy.get("salary") is None
                    or vacancy["salary"].get("to") is None
                    or vacancy["salary"].get("from") is None
                    or vacancy in self._sorted_vacancies
                ):
                    continue
                elif (
                    self._keyword_2 in vacancy.get("name")
                    and self._employment in vacancy["employment"].get("name")
                    and self._currency in vacancy["salary"].get("currency")
                    and vacancy["salary"].get("from", 0) >= self._pay_from
                    and vacancy["salary"].get("to", 0) <= self._pay_to
                ):
                    self._sorted_vacancies.append(vacancy)
                else:
                    continue
            return self._sorted_vacancies

        except Exception as e:
            print(e)
            print("Ошибка в классе OperationsWithVacancies")
            return []


class SalaryOfVacancies(OperationsWithVacancies):
    """Класс, работающий с зарплатами вакансий"""

    def _avg(self) -> list:
        """Метод, высчитывающий среднюю зарплату для каждой вакансии"""
        self._filtered_vacancies()
        for vacancy in self._sorted_vacancies:
            avg_pay = (vacancy["salary"].get("from") + vacancy["salary"].get("to")) / 2
            vacancy["salary"]["avg"] = avg_pay
        return self._sorted_vacancies

    def _comparison_pay(self) -> None | list:
        """Метод, сортирующий вакансии со средними зарплатами в порядке возрастания"""
        self._avg()
        if not self._sorted_vacancies:
            return None
        return sorted(self._sorted_vacancies, key=lambda x: x["salary"]["avg"], reverse=True)

    def _highest_pay(self) -> Any:
        """Метод, возвращающий вакансию с максимальной средней зарплатой"""
        self._avg()
        if not self._sorted_vacancies:
            return None
        return max(self._sorted_vacancies, key=lambda x: x["salary"]["avg"])

    def _get_max_avg_salary(self) -> float:
        """Метод возвращает максимальную среднюю зарплату в списке вакансий"""
        self._avg()
        highest_vacancy = self._highest_pay()
        return highest_vacancy["salary"]["avg"] if highest_vacancy else 0
