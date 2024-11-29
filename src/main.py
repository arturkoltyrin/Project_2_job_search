from src.data_file import DeleteData, GetData, SaveData
from src.get_vacancies import GetVacancies
from src.operations_with_vacancies import (OperationsWithVacancies,
                                           SalaryOfVacancies)
from src.user_interaction import (get_vacations_with_keyword, search,
                                  top_vacations)


def main():
    # Общие параметры для вакансий
    language = "python"
    level = "Junior"
    employment_type = "Полная занятость"
    currency = "RUR"
    salary_from = 50_000
    salary_to = 100_000

    # Получение вакансий
    data = GetVacancies(language)
    print(data._loading())

    # Фильтрация вакансий
    filtered_vacancies = OperationsWithVacancies(
        "java", level, employment_type, currency, salary_from, salary_to
    )
    print(filtered_vacancies._filtered_vacancies())

    # Анализ зарплат
    salary_info = SalaryOfVacancies(
        language, level, employment_type, currency, salary_from, salary_to
    )
    print(salary_info._highest_pay())

    # Сохранение данных о вакансиях
    data_to_file = SaveData(
        language, level, employment_type, currency, salary_from, salary_to
    )
    print(data_to_file._save_data())

    # Получение данных из файла
    data_from_file = GetData(
        language, level, employment_type, currency, salary_from, salary_to
    )
    print(data_from_file._get_data())

    # Пользовательский ввод
    input_data = input(
        "Введите информацию через запятую (ЯП, уровень, форма занятости, валюта, зарплата от, до): "
    )
    key_word, name, employment, currency, pay_from, pay_to = map(
        str.strip, input_data.split(",")
    )
    n = input("Введите количество вакансий: ")

    # Поиск вакансий по пользовательским критериям
    vacations = search(key_word, name, employment, currency, pay_from, pay_to)
    for vacancy in vacations:
        print(vacancy)

    # Вывод топ-вакансий и вакансий по ключевому слову
    print(top_vacations(key_word, n))
    print(get_vacations_with_keyword(key_word))


if __name__ == "__main__":
    main()
