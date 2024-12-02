import pytest
from unittest.mock import Mock, patch
from src.get_vacancies import HeadHunterAPI


@patch('requests.get')
def test_load_vacancies_http_error(mock_get):
    """Тест для обработки HTTP ошибок"""
    api_response = Mock()
    api_response.status_code = 404
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    vacancies = parser.load_vacancies("QA")

    assert len(vacancies) == 0

@patch('requests.get')
def test_load_vacancies_empty_response(mock_get):
    """Тест для обработки пустого ответа от API"""
    api_response = Mock()
    api_response.status_code = 200
    api_response.json.return_value = {"items": []}
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    vacancies = parser.load_vacancies("QA")

    assert len(vacancies) == 0


@patch('requests.get')
def test_api_connect_success(mock_get):
    """Тест успешного подключения к API."""
    api_response = Mock()
    api_response.status_code = 200
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    response = parser._HeadHunterAPI__api_connect()

    assert response == api_response


@patch('requests.get')
def test_api_connect_failure(mock_get):
    """Тест для обработки ошибки подключения к API."""
    api_response = Mock()
    api_response.status_code = 404
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    response = parser._HeadHunterAPI__api_connect()

    assert response is None

@patch('requests.get')
def test_load_vacancies_no_salary(mock_get):
    """Тест загрузки вакансий без указания зарплаты."""
    api_response = Mock()
    api_response.status_code = 200
    api_response.json.return_value = {
        "items": [
            {
                "name": "QA Engineer",
                "alternate_url": "https://hh.ru/vacancy/12345",
                "snippet": {
                    "requirement": "Знание Python",
                    "responsibility": "Тестирование ПО"
                },
                "salary": None
            }
        ]
    }
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    vacancies = parser.load_vacancies("QA")

    assert len(vacancies) == 20
    assert vacancies[0]["salary"] == 0


@patch('requests.get')
def test_load_vacancies_empty_response(mock_get):
    """Тест для обработки пустого ответа от API."""
    api_response = Mock()
    api_response.status_code = 200
    api_response.json.return_value = {
        "items": []
    }
    mock_get.return_value = api_response

    parser = HeadHunterAPI()
    vacancies = parser.load_vacancies("QA")

    assert len(vacancies) == 0


@pytest.fixture
def api_client():
    """Создание экземпляра HeadHunterAPI"""
    return HeadHunterAPI()


@patch('src.get_vacancies.requests.get')
def test_api_connect_success(mock_get, api_client):
    """Тест успешного подключения к API"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    response = api_client._HeadHunterAPI__api_connect()
    assert response is not None
    assert response.status_code == 200


@patch('src.get_vacancies.requests.get')
def test_api_connect_failure(mock_get, api_client):
    """Тест неуспешного подключения к API"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    response = api_client._HeadHunterAPI__api_connect()
    assert response is None



@patch('src.get_vacancies.requests.get')
def test_load_vacancies_no_results(mock_get, api_client):
    """Тест загрузки вакансий при отсутствии результатов"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'items': []
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    vacancies = api_client.load_vacancies('Nonexistent Keyword')
    assert vacancies == []