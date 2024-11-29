class Vacancy:
    """Класс для представления вакансий"""
    __slots__ = ("name", "url", "requirement", "responsibility", "salary")

    def __init__(self, name: str, url: str, requirement: str, responsibility: str, salary=None):
        """Инициализатор класса Vacancy"""
        self.name = name
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility
        self.salary = self.__salary_validation(salary)

    @staticmethod
    def __salary_validation(salary: int):
        """Валидация зарплаты"""
        if salary:
            return salary
        return 0

    @classmethod
    def cast_to_object_list(cls, vacancies: list[dict]):
        """Возвращает список экземпляров Vacancy из списка словарей"""

        return [cls(**vac) for vac in vacancies]

    def __str__(self):
        """Метод строкового предсиавления вакансий"""

        return (f"{self.name} (Зарплата: {self.salary if self.salary else 'не указана'}).\nТребования: {self.requirement}.\n"
                f"Обязанности: {self.responsibility}.\nСсылка: {self.url}")

    @classmethod
    def __verify_data(cls, other):
        """Проверка типа данных"""
        if not isinstance(other, (float, Vacancy)):
            raise TypeError

        return other if isinstance(other, float) else other.salary

    def __eq__(self, other):
        """Метод сравнения вакансий (=)"""
        sal = self.__verify_data(other)
        return self.salary == sal

    def __lt__(self, other):
        """Метод сравнения вакансий (<)"""
        sal = self.__verify_data(other)
        return self.salary < sal

    def __le__(self, other):
        """Метод сравнения вакансий (<=)"""
        sal = self.__verify_data(other)
        return self.salary <= sal

    def to_dict(self):
        """Возвращает словарь с данными о вакансии из экземпляра класса Vacancy"""
        return {"name": self.name, "url": self.url, "requirement": self.requirement,
                "responsibility": self.responsibility, "salary": self.salary}
