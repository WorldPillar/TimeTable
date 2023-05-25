class SchoolData:
    days = [{"Position": "1", "Name": "Понедельник", "Abb": "Пн"},
            {"Position": "2", "Name": "Вторник", "Abb": "Вт"},
            {"Position": "3", "Name": "Среда", "Abb": "Ср"},
            {"Position": "4", "Name": "Четверг", "Abb": "Чт"},
            {"Position": "5", "Name": "Пятница", "Abb": "Пт"},
            {"Position": "6", "Name": "Суббота", "Abb": "Сб"},
            {"Position": "7", "Name": "Воскресенье", "Abb": "Вс"}]
    """
    Дни недели
    """

    max_lessons_in_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    """
    Максимальное количество уроков в одном дне
    """

    max_lesson_in_week = ["1", "2", "3", "4", "5", "6", "7"]
    """
    Максимальное количество одного урока в неделю
    """

    headers = {"Subject": ["Имя", "Сокращение", "Уроков"],
               "Teacher": ["Имя", "Сокращение", "Уроков", "Нагрузка"],
               "Class": ["Имя", "Сокращение", "Уроков"],
               "Lesson": ["Предмет", "Учитель", "Класс", "Количество", "Длительность"]}
    """
    Заголовки таблиц списков школы
    """

    @staticmethod
    def get_max_lesson_in_week(days: int):
        """
        :param days: Количество дней в неделю.
        :return: Максимальное количество уроков в неделю.
        """
        return SchoolData.max_lesson_in_week[:days]

    @staticmethod
    def get_days_positions() -> list[str]:
        """
        :return: Метод возвращает список позиций всех дней.
        """
        days_positions = [day["Position"] for day in SchoolData.days]
        return days_positions

    @staticmethod
    def get_days_names() -> list[str]:
        """
        :return: Метод возвращает список имён всех дней.
        """
        days_names = [day["Name"] for day in SchoolData.days]
        return days_names

    @staticmethod
    def get_day_name(pos: int) -> str:
        """
        :param pos: Номер дня.
        :return: Имя дня по его номеру.
        """
        return SchoolData.days[pos]["Name"]

    @staticmethod
    def get_days_abb() -> list[str]:
        """
        :return: Метод возвращает список сокращений имён всех дней.
        """
        days_abb = [day["Abb"] for day in SchoolData.days]
        return days_abb

    @staticmethod
    def get_day_abb(pos: int) -> str:
        """
        :param pos: Номер дня.
        :return: Сокращение имени дня по его номеру.
        """
        return SchoolData.days[pos]["Abb"]
