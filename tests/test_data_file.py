import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.data_file import JSONSaver
from src.user_interaction import Vacancy
from config import DATA_DIR


@pytest.fixture
def vacancy():
    """Создаем фикстуру для одной вакансии"""
    return Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1", requirement="Python", responsibility="Testing",
                   salary=70000)


@pytest.fixture
def json_saver():
    """Создает фикстуру для JSONSaver с мокированием файла"""
    with patch("builtins.open", mock_open(read_data=json.dumps([]))) as m:
        saver = JSONSaver(filename="test_vacancies.json")
        yield saver

def test_saver():
    saver = JSONSaver("test.json")
    vac = Vacancy("Разработчик", "https://hh", "требования", "обязанности")

    saver.add_vacancy(vac)
    file = os.path.join(DATA_DIR, "test.json")

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    assert data == [
        {
            "name": "Разработчик",
            "url": "https://hh",
            "requirement": "требования",
            "responsibility": "обязанности",
            "salary": 0,
        }
    ]

def test_add_vacancy_new(json_saver, vacancy):
    """Тест на добавление новой вакансии"""


    with patch.object(json_saver, '_JSONSaver__save_to_file') as mock_save:
        json_saver.add_vacancy(vacancy)

        mock_save.assert_called_once()


def test_add_vacancy_existing(json_saver, vacancy):
    """Тест на попытку добавления дублирующейся вакансии"""
    json_saver.add_vacancy(vacancy)

    with patch("builtins.open", mock_open(read_data=json.dumps([vacancy.to_dict()]))):
        json_saver.add_vacancy(vacancy)


        handle = mock_open(read_data=json.dumps([vacancy.to_dict()]))()
        data = json.loads(handle.read())

    assert len(data) == 1


def test_del_vacancy_existing(json_saver, vacancy):
    """Тест на удаление существующей вакансии"""
    json_saver.add_vacancy(vacancy)

    # Мокаем метод сохранения
    with patch.object(json_saver, '_JSONSaver__save_to_file') as mock_save:
        json_saver.del_vacancy(vacancy.url)


        mock_save.assert_called_once()

def test_del_vacancy_nonexistent(json_saver):
    """Тест на удаление несуществующей вакансии"""
    json_saver.del_vacancy("https://hh.ru/nonexistent_vacancy")


    with patch("builtins.open", mock_open(read_data=json.dumps([]))) as m:

        handle = m()
        data = json.loads(handle.read())

    assert len(data) == 0


def test_get_vacancy_by_vacancy_name_no_match(json_saver):
    """Тест получения вакансий по имени без совпадений"""
    vacancy = Vacancy(name="DevOps Engineer", url="https://hh.ru/vacancy2", requirement="AWS",
                      responsibility="Deployment", salary=80000)
    json_saver.add_vacancy(vacancy)

    result = json_saver.get_vacancy_by_vacancy_name("QA")
    assert len(result) == 0


def test_read_file_empty(json_saver):
    """Тест чтения пустого файла"""
    with patch("builtins.open", mock_open(read_data=json.dumps([]))):
        vacancies = json_saver._JSONSaver__read_file()
    assert vacancies == []


def test_json_decode_error(json_saver):
    """Тест на обработку ошибки JSONDecodeError"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        vacancies = json_saver._JSONSaver__read_file()
    assert vacancies == []


def test_save_to_file(json_saver):
    """Тестирование метода сохранения файла"""
    vacancy = Vacancy(name="QA",
                      url="https://hh.ru",
                      requirement="Знание Python",
                      responsibility="Тестирование ПО")
    json_saver.add_vacancy(vacancy)

