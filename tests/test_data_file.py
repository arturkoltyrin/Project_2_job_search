import json
import pytest
from unittest.mock import mock_open, patch
from src.data_file import GetData, SaveData


def test_save_data_json_decode_error():
    save_data_instance = SaveData("keyword", "keyword_2", "employment", "currency", 0, 100000)
    m = mock_open(read_data="invalid json")

    with patch("builtins.open", m):
        with patch("json.dump") as mock_dump:
            with patch.object(save_data_instance, "_comparison_pay",
                              return_value=[{"vacancy": "Developer", "salary": 50000}]):
                result = save_data_instance._save_data()

            mock_dump.assert_called_once()
            assert result == [{"vacancy": "Developer", "salary": 50000}]


@pytest.fixture
def get_data_instance():
    keyword = "Python"
    keyword_2 = "Разработчик"
    employment = "Полная занятость"
    currency = "RUB"
    pay_from = 80000
    pay_to = 120000
    return GetData(keyword, keyword_2, employment, currency, pay_from, pay_to)


def test_get_data_success(get_data_instance):
    mock_data = json.dumps(
        [
            {
                "name": "Разработчик Python",
                "employment": {"name": "Полная занятость"},
                "salary": {"currency": "RUB", "from": 80000, "to": 120000},
            },
            {
                "name": "Junior Python Developer",
                "employment": {"name": "Стажировка"},
                "salary": {"currency": "RUB", "from": 30000, "to": 50000},
            },
        ]
    )

    m = mock_open(read_data=mock_data)
    with patch("builtins.open", m):
        result = get_data_instance._get_data()

    expected_result = [
        {
            "name": "Разработчик Python",
            "employment": {"name": "Полная занятость"},
            "salary": {"currency": "RUB", "from": 80000, "to": 120000},
        }
    ]
    assert result == expected_result
