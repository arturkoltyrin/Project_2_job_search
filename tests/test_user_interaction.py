import pytest
from unittest.mock import patch
from src.user_interaction import top_vacations

mock_data = [
    {
        "name": "Junior Python Developer",
        "area": {"name": "Пермь"},
        "salary": {"from": 20000, "to": 50000, "currency": "RUB"},
        "alternate_url": "https://api.hh.ru/vacancies"
    },
    {
        "name": "Middle Python Developer",
        "area": {"name": "Санкт-Петербург"},
        "salary": {"from": 80000, "to": 100000, "currency": "RUB"},
        "alternate_url": "https://api.hh.ru/vacancies"
    },
]

@patch('src.get_vacancies.GetVacancies._loading', return_value=mock_data)
def test_top_vacations(mock_loading):
    result = top_vacations("python", "2")

    assert len(result) == 2
    assert result[0]['имя вакансии'] == "Junior Python Developer"
    assert result[1]['имя вакансии'] == "Middle Python Developer"
