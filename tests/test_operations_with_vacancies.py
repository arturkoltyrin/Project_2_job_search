import pytest

from src.operations_with_vacancies import (OperationsWithVacancies,
                                           SalaryOfVacancies)

mock_vacancies = [
    {
        "name": "Junior Python Developer",
        "employment": {"name": "Полная занятость"},
        "salary": {"currency": "RUR", "from": 50000, "to": 80000},
    },
    {
        "name": "Middle Python Developer",
        "employment": {"name": "Полная занятость"},
        "salary": {"currency": "RUR", "from": 80000, "to": 120000},
    },
    {
        "name": "Senior Python Developer",
        "employment": {"name": "Частичная занятость"},
        "salary": {"currency": "RUR", "from": 150000, "to": 200000},
    },
]


@pytest.fixture
def operations_instance():
    instance = OperationsWithVacancies(
        "python", "Junior", "Полная занятость", "RUR", 50000, 100000
    )
    instance._vacancies = mock_vacancies
    return instance


def test_operations_with_vacancies_initialization(operations_instance):
    assert operations_instance._keyword == "python"
    assert operations_instance._keyword_2 == "Junior"
    assert operations_instance._employment == "Полная занятость"
    assert operations_instance._currency == "RUR"
    assert operations_instance._pay_from == 50000
    assert operations_instance._pay_to == 100000
    assert operations_instance._sorted_vacancies == []


def test_filtered_vacancies(operations_instance):
    filtered_vacancies = operations_instance._filtered_vacancies()
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0]["name"] == "Junior Python Developer"


@pytest.fixture
def salary_instance():
    instance = SalaryOfVacancies(
        "python", "Junior", "Полная занятость", "RUR", 50000, 100000
    )
    instance._vacancies = mock_vacancies
    return instance


def test_avg_salary(salary_instance):
    avg_vacancies = salary_instance._avg()
    assert len(avg_vacancies) == 1
    assert "avg" in avg_vacancies[0]["salary"]
    assert avg_vacancies[0]["salary"]["avg"] == 65000.0


def test_highest_pay(salary_instance):
    highest_vacancy = salary_instance._highest_pay()
    assert highest_vacancy["name"] == "Junior Python Developer"


def test_get_max_avg_salary(salary_instance):
    max_avg_salary = salary_instance._get_max_avg_salary()
    assert max_avg_salary == 65000.0
