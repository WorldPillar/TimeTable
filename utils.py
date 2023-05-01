def column_to_days_lessons(column: int, amount_lessons: int) -> (int, int):
    """
    Функция для преобразования номера столбца в день и позицию урока в этом дне.
    :param column: номер столбца.
    :param amount_lessons: максимальное количество уроков в день.
    :return: кортеж дня и позиции урока, соответствующая переданному номеру столбца.
    """
    day = column // amount_lessons
    lesson_position = column % amount_lessons
    return day, lesson_position
