import pytest
from src.operations_with_vacancies import Vacancy, get_vacancies_by_salary_from, sort_vacancies_by_salary, get_top_vacancies

@pytest.fixture
def vacancies():
    return [
        Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1", requirement="Python", responsibility="Testing", salary=70000),
        Vacancy(name="Senior QA Engineer", url="https://hh.ru/vacancy2", requirement="Python", responsibility="Testing", salary=90000),
        Vacancy(name="Junior QA Engineer", url="https://hh.ru/vacancy3", requirement="Python", responsibility="Testing", salary=50000),
        Vacancy(name="DevOps Engineer", url="https://hh.ru/vacancy4", requirement="AWS", responsibility="Deployment", salary=80000),
    ]

def test_get_vacancies_by_salary_from(vacancies):
    result = get_vacancies_by_salary_from(vacancies, salary_from=60000)
    assert len(result) == 3
    assert all(vac.salary >= 60000 for vac in result)

def test_get_vacancies_by_salary_from_no_match(vacancies):
    result = get_vacancies_by_salary_from(vacancies, salary_from=100000)
    assert len(result) == 0

def test_get_vacancies_by_salary_from_all_match(vacancies):
    result = get_vacancies_by_salary_from(vacancies, salary_from=50000)
    assert len(result) == 4
    assert all(vac.salary >= 50000 for vac in result)

def test_sort_vacancies_by_salary(vacancies):
    sorted_vacancies = sort_vacancies_by_salary(vacancies)
    assert sorted_vacancies[0].salary == 90000
    assert sorted_vacancies[1].salary == 80000
    assert sorted_vacancies[2].salary == 70000
    assert sorted_vacancies[3].salary == 50000

def test_sort_vacancies_by_salary_empty_list():
    sorted_vacancies = sort_vacancies_by_salary([])
    assert len(sorted_vacancies) == 0

def test_sort_vacancies_by_salary_one_item():
    single_vacancy = [Vacancy(name="Single QA", url="https://hh.ru/vacancy5", requirement="Python", responsibility="Testing", salary=60000)]
    sorted_vacancies = sort_vacancies_by_salary(single_vacancy)
    assert len(sorted_vacancies) == 1
    assert sorted_vacancies[0].salary == 60000

def test_get_top_vacancies(vacancies):
    top_vacancies = get_top_vacancies(vacancies, top_n=2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].salary == 90000
    assert top_vacancies[1].salary == 80000

def test_get_top_vacancies_more_than_available(vacancies):
    top_vacancies = get_top_vacancies(vacancies, top_n=10)
    assert len(top_vacancies) == 4

def test_get_top_vacancies_empty_list():
    top_vacancies = get_top_vacancies([], top_n=3)
    assert len(top_vacancies) == 0

def test_get_top_vacancies_one_item():
    single_vacancy = [Vacancy(name="Single QA", url="https://hh.ru/vacancy5", requirement="Python", responsibility="Testing", salary=60000)]
    top_vacancies = get_top_vacancies(single_vacancy, top_n=1)
    assert len(top_vacancies) == 1
    assert top_vacancies[0].salary == 60000


def test_get_vacancies_by_salary_from_negative_salary(vacancies):
    result = get_vacancies_by_salary_from(vacancies, salary_from=-1000)
    assert len(result) == 4


def test_sort_vacancies_by_salary_equal_salary(vacancies):
    vacancies.append(
        Vacancy(name="Equal Salary QA", url="https://hh.ru/vacancy6", requirement="Python", responsibility="Testing",
                salary=70000))
    sorted_vacancies = sort_vacancies_by_salary(vacancies)
    assert sorted_vacancies[0].salary == 90000
    assert sorted_vacancies[1].salary == 80000
    assert sorted_vacancies[2].salary == 70000
    assert sorted_vacancies[3].salary == 70000
    assert sorted_vacancies[4].salary == 50000


def test_get_top_vacancies_with_equal_salary(vacancies):
    vacancies.append(
        Vacancy(name="Top Salary QA", url="https://hh.ru/vacancy7", requirement="Python", responsibility="Testing",
                salary=90000))
    top_vacancies = get_top_vacancies(vacancies, top_n=2)
    assert len(top_vacancies) == 2
    assert all(vac.salary >= 90000 for vac in top_vacancies)


def test_vacancy_with_none_fields():
    vacancy_with_none = Vacancy(name=None, url=None, requirement=None, responsibility=None, salary=0)
    assert vacancy_with_none.name is None
    assert vacancy_with_none.url is None
    assert vacancy_with_none.requirement is None
    assert vacancy_with_none.salary == 0
