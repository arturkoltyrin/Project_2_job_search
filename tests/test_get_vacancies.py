from src.get_vacancies import GetVacancies


def test_init_get_vacancies():
    keyword = "python"
    data = GetVacancies(keyword)
    assert data._keyword == keyword
