from src.user_interaction import Vacancy

class TestVacancy:
    def test_initialization_with_valid_salary(self):
        """Проверка успешной инициализации с валидной зарплатой"""
        vacancy = Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1",
                          requirement="Python", responsibility="Testing", salary=70000)
        assert vacancy.name == "QA Engineer"
        assert vacancy.url == "https://hh.ru/vacancy1"
        assert vacancy.requirement == "Python"
        assert vacancy.responsibility == "Testing"
        assert vacancy.salary == 70000

    def test_initialization_with_no_salary(self):
        """Проверка инициализации без указания зарплаты"""
        vacancy = Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1",
                          requirement="Python", responsibility="Testing")
        assert vacancy.salary == 0

    def test_salary_validation_with_none(self):
        """Проверка валидации зарплаты с None"""
        salary = Vacancy._Vacancy__salary_validation(None)
        assert salary == 0

    def test_salary_validation_with_valid_amount(self):
        """Проверка валидации с валидной зарплатой"""
        salary = Vacancy._Vacancy__salary_validation(50000)
        assert salary == 50000

    def test_str_method(self):
        """Проверка строкового представления вакансии"""
        vacancy = Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1",
                          requirement="Python", responsibility="Testing", salary=70000)
        assert str(vacancy) == (
            "QA Engineer (Зарплата: 70000).\n"
            "Требования: Python.\n"
            "Обязанности: Testing.\n"
            "Ссылка: https://hh.ru/vacancy1"
        )

    def test_eq_operator(self):
        """Проверка оператора равенства (==)"""
        vacancy1 = Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1",
                           requirement="Python", responsibility="Testing", salary=70000)
        vacancy2 = Vacancy(name="Senior QA Engineer", url="https://hh.ru/vacancy1",
                           requirement="Advanced Python", responsibility="Testing", salary=70000)
        assert vacancy1 == vacancy2

    def test_cast_to_object_list(self):
        """Проверка метода cast_to_object_list"""
        vacancies_data = [
            {"name": "QA Engineer", "url": "https://hh.ru/vacancy1", "requirement": "Python",
             "responsibility": "Testing", "salary": 70000},
            {"name": "Senior QA Engineer", "url": "https://hh.ru/vacancy1", "requirement": "Advanced Python",
             "responsibility": "Testing", "salary": 90000},
        ]
        vacancies = Vacancy.cast_to_object_list(vacancies_data)
        assert len(vacancies) == 2
        assert isinstance(vacancies[0], Vacancy)

    def test_to_dict_method(self):
        """Проверка метода to_dict"""
        vacancy = Vacancy(name="QA Engineer", url="https://hh.ru/vacancy1",
                          requirement="Python", responsibility="Testing", salary=70000)
        expected_dict = {
            "name": "QA Engineer",
            "url": "https://hh.ru/vacancy1",
            "requirement": "Python",
            "responsibility": "Testing",
            "salary": 70000
        }
        assert vacancy.to_dict() == expected_dict