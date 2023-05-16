import itertools
from copy import deepcopy


class Teacher:
    id_obj = itertools.count()

    def __init__(self, family: str, name: str, workload: int, abbreviation: str = ''):
        self.id = next(Teacher.id_obj)
        self.family: str = family
        self.name: str = name
        self.workload: int = workload
        self.abbreviation: str = abbreviation

        self.worktime = deepcopy(WorkTime.worktime)
        self.current_worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self) -> str:
        """
        Метод возвращает имя объекта
        """
        name = f'{str(self.family or "")} {str(self.name or "")}'
        return name

    def get_full_name(self) -> str:
        """
        Метод возвращает полное наименование объекта
        """
        string = f'{str(self.family or "")} {str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self) -> list:
        items = [f'{str(self.family or "")} {str(self.name or "")}',
                 self.abbreviation, self.lessons_count, self.workload]
        return items

    def update_data(self, family: str = '', name: str = '',
                    workload: int = None, abbreviation: str = '') -> None:
        self.family = family
        self.name = name
        self.workload = workload
        self.abbreviation = abbreviation
        return


class StudentClass:
    id_obj = itertools.count()

    def __init__(self, name: str, abbreviation: str = ''):
        self.id = next(StudentClass.id_obj)
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.worktime = deepcopy(WorkTime.worktime)
        self.current_worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self) -> str:
        """
        Метод возвращает имя объекта
        """
        name = f'{self.name}'
        return name

    def get_full_name(self) -> str:
        """
        Метод возвращает полное наименование объекта
        """
        string = f'{str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self) -> list:
        items = [self.name, self.abbreviation, self.lessons_count]
        return items

    def update_data(self, name: str = '', abbreviation: str = '') -> None:
        self.name = name
        self.abbreviation = abbreviation
        return


class Subject:
    id_obj = itertools.count()

    def __init__(self, name: str, abbreviation: str = ''):
        self.id = next(Subject.id_obj)
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self) -> str:
        """
        Метод возвращает имя объекта
        """
        name = f'{self.name}'
        return name

    def get_full_name(self) -> str:
        """
        Метод возвращает полное наименование объекта
        """
        string = f'{str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self) -> list:
        items = [self.name, self.abbreviation, self.lessons_count]
        return items

    def update_data(self, name: str = '', abbreviation: str = '') -> None:
        self.name = name
        self.abbreviation = abbreviation
        return


class Lesson:
    id_obj = itertools.count()

    def __init__(self, subject: Subject, teacher: Teacher, student_class: StudentClass, amount: int, duration: int = 1):
        self.id = next(Lesson.id_obj)
        self.subject: Subject = subject
        self.teachers: list[Teacher] = [teacher]
        self.student_class: StudentClass = student_class
        self.amount: int = amount
        self.duration: int = duration
        self.start_end_positions: list[dict] = []
        self._add_lesson_to_objects()

    def _add_lesson_to_objects(self) -> None:
        self.subject.lessons_count += self.amount * self.duration
        for teacher in self.teachers:
            teacher.lessons_count += self.amount * self.duration
        self.student_class.lessons_count += self.amount * self.duration
        return

    def delete_lesson(self) -> None:
        """
        Метод уменьшает количество уроков у каждого объекта, который содержится в данном lesson.
        """
        self.subject.lessons_count -= self.amount * self.duration
        for teacher in self.teachers:
            teacher.lessons_count -= self.amount * self.duration
        self.student_class.lessons_count -= self.amount * self.duration
        return

    def update_lesson_data(self, subject: Subject = None, teachers: list[Teacher] = None,
                           student_class: StudentClass = None, amount: int = None, duration: int = None) -> None:
        if subject is not None and self.subject != subject:
            self.subject.lessons_count -= self.amount * self.duration
            self.subject = subject
            self.subject.lessons_count += self.amount * self.duration
        if teachers is not None:
            for teach in self.teachers:
                teach.lessons_count -= self.amount * self.duration
            self.teachers.clear()
            for teach in teachers:
                teach.lessons_count += self.amount * self.duration
                self.teachers.append(teach)
        if student_class is not None and self.student_class != student_class:
            self.student_class.lessons_count -= self.amount * self.duration
            self.student_class = student_class
            self.student_class.lessons_count += self.amount * self.duration
        if duration is not None and self.duration != duration:
            self.delete_lesson()
            self.duration = duration
            self._add_lesson_to_objects()
        if amount is not None and self.amount != amount:
            self.delete_lesson()
            self.amount = amount
            self._add_lesson_to_objects()
        return

    def is_available(self, day, lesson) -> bool:
        """
        Метод возвращает значение bool, доступен ли урок по ограничениям или нет.
        :param day: День, в который проверяется доступность.
        :param lesson: Позиция урока, в который проверяется доступность.
        :return: Доступен или не доступен.
        """
        if lesson + self.duration - 1 >= len(self.subject.worktime[day]):
            return False
        for i in range(lesson, lesson + self.duration):
            s = self.subject.worktime[day][i]
            t = 1
            for teacher in self.teachers:
                t *= teacher.worktime[day][i]
            c = self.student_class.worktime[day][i]
            if s * t * c == 0:
                return False
        return True

    def current_available(self, day, lesson) -> bool:
        """
        Метод возвращает значение bool, доступен ли урок в данном расписании.
        :param day: День, в который проверяется доступность.
        :param lesson: Позиция урока, в который проверяется доступность.
        :return: Доступен или не доступен.
        """
        cur_av = True
        for i in range(lesson, lesson + self.duration):
            t = self._teacher_current_available(day, i)
            c = self._student_class_current_available(day, i)
            les = self.is_available_today(day)
            cur_av = cur_av and les and t and c
        return cur_av

    def _teacher_current_available(self, day, lesson) -> bool:
        for teacher in self.teachers:
            if teacher.current_worktime[day][lesson] == 0:
                return False
        return True

    def _student_class_current_available(self, day, lesson) -> bool:
        if self.student_class.current_worktime[day][lesson] == 0:
            return False
        return True

    def is_available_today(self, day) -> bool:
        for lesson in self.start_end_positions:
            if lesson['day'] == day:
                return False
        return True

    def set_unavailable(self, day, lesson) -> None:
        self.start_end_positions.append({'day': day, 'start': lesson, 'end': lesson + self.duration - 1})
        for i in range(lesson, lesson + self.duration):
            for teacher in self.teachers:
                teacher.current_worktime[day][i] = 0
            self.student_class.current_worktime[day][i] = 0
        return

    def set_available(self, day, lesson) -> None:
        start_end = self.get_start_end_lesson(day, lesson)
        for i in range(start_end['start'], start_end['end'] + 1):
            for teacher in self.teachers:
                teacher.current_worktime[day][i] = 1
            self.student_class.current_worktime[day][i] = 1
        self.start_end_positions.remove(start_end)
        return

    def get_start_end_lesson(self, day: int, start: int) -> dict:
        """
        Метод возвращает начало и конец урока по дню и позиции, в которой находится урок.
        """
        for lesson in self.start_end_positions:
            if lesson['day'] == day and lesson['start'] <= start <= lesson['end']:
                return lesson

    def get_full_name(self) -> str:
        """
        Метод возвращает полное наименование объекта
        """
        teachers = f'{self.teachers[0].get_full_name()}'
        for i in range(1, len(self.teachers)):
            teachers = teachers + ', ' + self.teachers[i].get_full_name()
        string = f'{self.subject.get_full_name()} {teachers}' \
                 f' {self.student_class.get_full_name()} {self.amount} {self.duration}'
        return string

    def get_attributes(self) -> list[str]:
        """
        Метод возвращает атрибуты объекта для вывода в таблицу списков
        """
        teachers = f'{str(self.teachers[0].family or "")} {str(self.teachers[0].name or "")}'
        for i in range(1, len(self.teachers)):
            teachers = teachers + ', ' + f'{str(self.teachers[i].family or "")} {str(self.teachers[i].name or "")}'
        items = [self.subject.name, teachers,
                 self.student_class.name, str(self.amount), str(self.duration)]
        return items

    def toJSON(self) -> dict:
        """
        Метод преобразует объекты в правильный для сохранения вид в виде словаря.
        :return: словарь всех объектов
        """
        lesson_tojson = {"id": self.id,
                         "subject": self.subject.id,
                         "teachers": [
                             {"teacher": teacher.id} for teacher in self.teachers
                         ],
                         "student_class": self.student_class.id,
                         "amount": self.amount,
                         "duration": self.duration,
                         "start_end_positions": [
                             {"day": item['day'],
                              "start": item['start'],
                              "end": item['end']
                              } for item in self.start_end_positions
                         ]
                         }
        return lesson_tojson


class WorkTime:
    worktime: list[list[int]] = []

    @staticmethod
    def set_worktime(amount_days: int, amount_lessons: int) -> None:
        WorkTime.worktime = [[1 for _ in range(amount_lessons)] for _ in range(amount_days)]
        return


class School:
    def __init__(self, name: str, amount_days: int, amount_lessons: int):
        self.name: str = name
        self.amount_days: int = amount_days
        self.amount_lessons: int = amount_lessons
        self.teachers: list[Teacher] = []
        self.subjects: list[Subject] = []
        self.student_classes: list[StudentClass] = []
        self.lessons: list[Lesson] = []
        self.timetable: list[list[list[Lesson]]] = [[[] for _ in range(self.amount_lessons)
                                                     ] for _ in range(self.amount_days)]
        self.unallocated: list[Lesson] = []
        WorkTime.set_worktime(amount_days, amount_lessons)
        self._reset_ids()

    @staticmethod
    def _reset_ids() -> None:
        """
        Метод сбрасывает id у всех классов списков School.
        """
        Subject.id_obj = itertools.count()
        Teacher.id_obj = itertools.count()
        StudentClass.id_obj = itertools.count()
        Lesson.id_obj = itertools.count()
        return

    def drop_current_time(self) -> None:
        """
        Метод сбрасывает текущее время у всех объектов из списков школы,
        а также длительность у каждого lesson.
        """
        for teacher in self.teachers:
            teacher.current_worktime = deepcopy(WorkTime.worktime)
        for student_class in self.student_classes:
            student_class.current_worktime = deepcopy(WorkTime.worktime)
        for lesson in self.lessons:
            lesson.start_end_positions = []
        return

    def pop_subject(self, position) -> None:
        """
        Метод удаляет subject из списка школы, а также все уроки, связанные с этим предметом.
        :param position: Позиция объекта subject в списке.
        """
        popped = self.subjects.pop(position)

        for i in range(position, len(self.subjects)):
            self.subjects[i].id = i
        Subject.id_obj = itertools.count(len(self.subjects))

        length = len(self.lessons)
        i = 0
        while i != length:
            if self.lessons[i].subject == popped:
                self.pop_lesson(i)
                length -= 1
            else:
                i += 1
        return

    def pop_class(self, position) -> None:
        """
        Метод удаляет student_class из списка школы, а также все уроки, связанные с этим предметом.
        :param position: Позиция объекта student_class в списке.
        """
        popped = self.student_classes.pop(position)

        for i in range(position, len(self.student_classes)):
            self.student_classes[i].id = i
        StudentClass.id_obj = itertools.count(len(self.student_classes))

        length = len(self.lessons)
        i = 0
        while i != length:
            if self.lessons[i].student_class == popped:
                self.pop_lesson(i)
                length -= 1
            else:
                i += 1
        return

    def pop_teacher(self, position) -> None:
        """
        Метод удаляет teacher из списка школы, а также все уроки, связанные с этим предметом.
        :param position: Позиция объекта teacher в списке.
        """
        popped = self.teachers.pop(position)

        for i in range(position, len(self.teachers)):
            self.teachers[i].id = i
        Teacher.id_obj = itertools.count(len(self.teachers))

        length = len(self.lessons)
        i = 0
        while i != length:
            if self.lessons[i].teachers == popped:
                self.pop_lesson(i)
                length -= 1
            else:
                i += 1
        return

    def pop_lesson(self, position) -> None:
        """
        Метод удаляет lesson из списка школы, а также все уроки, связанные с этим предметом.
        :param position: Позиция объекта lesson в списке.
        """
        self.lessons[position].delete_lesson()
        popped = self.lessons.pop(position)

        for i in range(position, len(self.lessons)):
            self.lessons[i].id = i
        Lesson.id_obj = itertools.count(len(self.lessons))

        # Удаляем все совпадающие уроки из расписания
        self.timetable = [[[lesson for lesson in les_pos if lesson != popped
                            ] for les_pos in day] for day in self.timetable]
        # Удаляем все совпадающие уроки из нераспределенных уроков
        self.unallocated = [lesson for lesson in self.unallocated if lesson != popped]
        return

    def validate_lesson_by_old(self, lesson: Lesson, old_subject: Subject,
                               old_student_class: StudentClass,
                               old_teachers: list[Teacher], old_amount: int, old_duration: int) -> None:
        """
        Метод валидации lesson после обновления по старым значениям.
        Удаляет или перемещает в нераспределенные уроки переданный объект.
        :param lesson: Объекта класса Lesson, у которого обновились данные.
        :param old_subject: Предыдущий объект класса Subject у lesson.
        :param old_student_class: Предыдущий объект класса StudentClass у lesson.
        :param old_teachers: Предыдущий объект класса Teacher у lesson.
        :param old_amount: Предыдущий amount у lesson.
        :param old_duration: Предыдущий duration у lesson.
        """
        not_changed = True
        not_changed = not_changed and (lesson.subject.id == old_subject.id)
        not_changed = not_changed and (lesson.student_class.id == old_student_class.id)
        not_changed = not_changed and self._update_lesson_teachers(lesson, old_teachers)
        if not not_changed:
            self._remove_lesson_from_timetable(lesson)
        self.update_lesson_amount(lesson, old_amount)
        self._update_lesson_duration(lesson, old_duration)
        return

    @staticmethod
    def _update_lesson_teachers(lesson: Lesson, old_teachers: list[Teacher]) -> bool:
        """
        Метод валидации lesson после обновления teachers.
        Проверяет, нужно ли обновлять положение урока по изменениям данных об учителях.
        """
        # Если количество учителей увеличилось, то обновлять нужно
        if len(lesson.teachers) > len(old_teachers):
            return False
        else:
            for teacher in lesson.teachers:
                olds = False
                for new_teacher in old_teachers:
                    if teacher.id == new_teacher.id:
                        olds = True
                # Если не был найден старый учитель, то обновлять нужно
                if not olds:
                    return False
        return True

    def _append_into_unallocated_list(self, lesson: Lesson, amount: int) -> None:
        """
        Помещает урок в список нераспределенных уроков.
        :param lesson: Урок, который необходимо поместить.
        :param amount: Количество урока, которое необходимо поместить.
        """
        for i in range(amount):
            self.unallocated.append(lesson)
        self.unallocated.sort(key=lambda x: x.id, reverse=False)

    def _remove_lesson_from_timetable(self, lesson: Lesson) -> None:
        """
        Удаляет все совпадающие уроки из расписания, после чего перемещает их в список нераспределенных уроков.
        :param lesson: Урок, который необходимо удалить и переместить.
        """
        for day in self.timetable:
            for les_pos in day:
                for located_lesson in les_pos:
                    if located_lesson == lesson:
                        les_pos.remove(located_lesson)
        self._append_into_unallocated_list(lesson, lesson.amount)
        return

    def _update_lesson_duration(self, lesson: Lesson, old_duration) -> None:
        """
        Метод валидации lesson после обновления duration.
        Перемещает в нераспределенные уроки переданный объект в случае увеличение длительности
        или удаляет часть объектов в случае уменьшения длительности.
        :param lesson: Объекта класса Lesson, у которого обновилось количество.
        :param old_duration: Предыдущий duration у lesson.
        """
        if lesson.duration == old_duration:
            return
        elif lesson.duration > old_duration:
            for day in self.timetable:
                for les_pos in day:
                    for located_lesson in les_pos:
                        if located_lesson == lesson:
                            les_pos.remove(located_lesson)
                            break
            for i in range(lesson.amount):
                self.unallocated.append(lesson)
            self.unallocated.sort(key=lambda x: x.id, reverse=False)
        else:
            for day in self.timetable:
                duration = lesson.duration
                for les_pos in day:
                    for located_lesson in les_pos:
                        if located_lesson == lesson:
                            if duration != 0:
                                duration -= 1
                            else:
                                les_pos.remove(located_lesson)
                            break
        return

    def update_lesson_amount(self, lesson: Lesson, old_amount) -> None:
        """
        Метод валидации lesson после обновления amount.
        Удаляет или перемещает в нераспределенные уроки переданный объект.
        :param lesson: Объекта класса Lesson, у которого обновилось количество.
        :param old_amount: Предыдущий amount у lesson.
        """
        amount = lesson.amount - old_amount
        if amount == 0:
            return
        elif amount > 0:
            self._append_into_unallocated_list(lesson, amount)
            return
        else:
            position = 0
            for i in range(len(self.unallocated)):
                if self.unallocated[position] == lesson:
                    self.unallocated.pop(position)
                    amount += 1
                    if amount == 0:
                        return
                else:
                    position += 1

            for day in self.timetable:
                for les_pos in day:
                    for located_lesson in les_pos:
                        if located_lesson == lesson:
                            les_pos.remove(located_lesson)
                            amount += 1
                            if amount == 0:
                                return
                            break
        return

    def get_lesson_conflicts(self, sender: Lesson, from_day: int = -1) -> (list[bool], list[list[list[Lesson]]]):
        """
        Метод возвращает список булевых значений. True - поместить урок в данное место возможно. False - невозможно.
        Воторой список - список конфликтных уроков, в случае, если поместить урок невозможно.
        :param sender: lesson, для которого необходимо найти конфликты.
        :param from_day: День, из которого перемещается lesson. Если lesson не распределён, оставить незаполненным.
        """

        times = [[sender.is_available(day, les_pos) for les_pos in range(self.amount_lessons)
                  ] for day in range(self.amount_days)]
        conflicts = [[[] for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]
        for day in range(self.amount_days):
            for les_pos in range(self.amount_lessons - sender.duration + 1):
                for d in range(sender.duration):
                    for receiver in self.timetable[day][les_pos + d]:
                        if receiver == sender and day != from_day and d == 0:
                            for pos in range(self.amount_lessons):
                                times[day][pos] = False
                                conflicts[day][pos].append(
                                    {"lesson": receiver, "day": day, "position": les_pos})
                            break

                        same_teachers = False
                        for teacher in sender.teachers:
                            for new_teacher in receiver.teachers:
                                if teacher == new_teacher:
                                    same_teachers = True
                                    break
                            if same_teachers:
                                break

                        if same_teachers:
                            if receiver.student_class != sender.student_class:
                                times[day][les_pos + d] = False
                                conflicts[day][les_pos].append(
                                    {"lesson": receiver, "day": day, "position": les_pos + d})
                                continue
        return times, conflicts

    def remove_duration(self, lesson: Lesson, day: int, les_pos: int) -> None:
        """
        Метод удаляет все смежные уроки в определенный день на определенной позиции,
         тем самым удаляя урок, учитывая его длительность.
        :param lesson: Урок, который хотим удалить.
        :param day: День, в который хотим удалить.
        :param les_pos: Одна из позиций урока, на которой он находится.
        """
        start_end = lesson.get_start_end_lesson(day, les_pos)
        for i in range(start_end['start'], start_end['end'] + 1):
            for j in range(len(self.timetable[day][i])):
                if self.timetable[day][i][j] == lesson:
                    self.timetable[day][i].remove(lesson)
                    break
        return

    def toJSON(self) -> dict:
        """
        Метод преобразует объекты в правильный для сохранения вид в виде словаря.
        :return: словарь всех объектов
        """
        school_tojson = {"name": self.name,
                         "amount_days": self.amount_days,
                         "amount_lessons": self.amount_lessons,
                         "teachers": [teacher.__dict__ for teacher in self.teachers],
                         "subjects": [subject.__dict__ for subject in self.subjects],
                         "student_classes": [student_class.__dict__ for student_class in self.student_classes],
                         "lessons": [lesson.toJSON() for lesson in self.lessons]
                         }
        return school_tojson
