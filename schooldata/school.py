import itertools
from copy import deepcopy


class Teacher:
    id_obj = itertools.count()

    def __init__(self, family: str, name: str, workload: int, abbreviation=''):
        self.id = next(Teacher.id_obj)
        self.family: str = family
        self.name: str = name
        self.workload: int = workload
        self.abbreviation: str = abbreviation

        self.worktime = deepcopy(WorkTime.worktime)
        self.current_worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self):
        name = f'{str(self.family or "")} {str(self.name or "")}'
        return name

    def get_string(self):
        string = f'{str(self.family or "")} {str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self):
        items = [f'{str(self.family or "")} {str(self.name or "")}',
                 self.abbreviation, self.lessons_count, self.workload]
        return items

    def update_teacher_data(self, family: str = '', name: str = '', workload: int = None, abbreviation: str = ''):
        self.family = family
        self.name = name
        self.workload = workload
        self.abbreviation = abbreviation
        return


class StudentClass:
    id_obj = itertools.count()

    def __init__(self, name: str, abbreviation=''):
        self.id = next(StudentClass.id_obj)
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.worktime = deepcopy(WorkTime.worktime)
        self.current_worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self):
        name = f'{self.name}'
        return name

    def get_string(self):
        string = f'{str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self):
        items = [self.name, self.abbreviation, self.lessons_count]
        return items

    def update_class_data(self, name: str = '', abbreviation: str = ''):
        self.name = name
        self.abbreviation = abbreviation
        return


class Subject:
    id_obj = itertools.count()

    def __init__(self, name: str, abbreviation=''):
        self.id = next(Subject.id_obj)
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.worktime = deepcopy(WorkTime.worktime)
        self.current_worktime = deepcopy(WorkTime.worktime)

        self.lessons_count: int = 0

    def get_name(self) -> str:
        name = f'{self.name}'
        return name

    def get_string(self) -> str:
        string = f'{str(self.name or "")} ({str(self.abbreviation or "")})'
        return string

    def get_attributes(self):
        items = [self.name, self.abbreviation, self.lessons_count]
        return items

    def update_subject_data(self, name: str = '', abbreviation: str = ''):
        self.name = name
        self.abbreviation = abbreviation
        return


class Lesson:
    id_obj = itertools.count()

    def __init__(self, subject: Subject, teacher: Teacher, student_class: StudentClass, amount: int):
        self.id = next(Lesson.id_obj)
        self.subject: Subject = subject
        self.teacher: Teacher = teacher
        self.student_class: StudentClass = student_class
        self.amount: int = amount
        self.current_worktime = deepcopy(WorkTime.worktime)
        self._add_lesson_to_objects()

    def _add_lesson_to_objects(self):
        self.subject.lessons_count += self.amount
        self.teacher.lessons_count += self.amount
        self.student_class.lessons_count += self.amount
        return

    def delete_lesson(self):
        self.subject.lessons_count -= self.amount
        self.teacher.lessons_count -= self.amount
        self.student_class.lessons_count -= self.amount
        return

    def update_lesson_data(self, subject: Subject = None, teacher: Teacher = None,
                           student_class: StudentClass = None, amount: int = -1):
        if subject is not None:
            self.subject.lessons_count -= self.amount
            self.subject = subject
            self.subject.lessons_count += self.amount
        if teacher is not None:
            self.teacher.lessons_count -= self.amount
            self.teacher = teacher
            self.teacher.lessons_count += self.amount
        if student_class is not None:
            self.student_class.lessons_count -= self.amount
            self.student_class = student_class
            self.student_class.lessons_count += self.amount
        if amount != -1:
            self.delete_lesson()
            self.amount = amount
            self._add_lesson_to_objects()
        return

    def is_available(self, day, lesson):
        s = self.subject.worktime[day][lesson]
        t = self.teacher.worktime[day][lesson]
        c = self.student_class.worktime[day][lesson]
        if s * t * c == 0:
            return False
        return True

    def current_available(self, day, lesson):
        t = self.teacher_current_available(day, lesson)
        c = self.student_class_current_available(day, lesson)
        les = self.is_available_today(day)
        return les and t and c

    def teacher_current_available(self, day, lesson):
        if self.teacher.current_worktime[day][lesson] == 0:
            return False
        return True

    def student_class_current_available(self, day, lesson):
        if self.student_class.current_worktime[day][lesson] == 0:
            return False
        return True

    def is_available_today(self, day):
        for lesson in self.current_worktime[day]:
            if lesson == 0:
                return False
        return True

    def set_unavailable(self, day, lesson):
        self.teacher.current_worktime[day][lesson] = 0
        self.student_class.current_worktime[day][lesson] = 0
        self.current_worktime[day][lesson] = 0
        return

    def set_available(self, day, lesson):
        self.teacher.current_worktime[day][lesson] = 1
        self.student_class.current_worktime[day][lesson] = 1
        self.current_worktime[day][lesson] = 1
        return

    def get_string(self):
        string = f'{self.subject.get_string()} {self.teacher.get_string()}' \
                 f' {self.student_class.get_string()} {self.amount}'
        return string

    def get_attributes(self):
        items = [self.subject.name, f'{str(self.teacher.family or "")} {str(self.teacher.name or "")}',
                 self.student_class.name, str(self.amount)]
        return items

    def toJSON(self):
        lesson_tojson = {"id": self.id,
                         "subject": self.subject.id,
                         "teacher": self.teacher.id,
                         "student_class": self.student_class.id,
                         "amount": self.amount,
                         "current_worktime": self.current_worktime
                         }
        return lesson_tojson


class WorkTime:
    worktime: list[list[int]] = []

    @staticmethod
    def set_worktime(amount_days: int, amount_lessons: int):
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
        self.reset_ids()

    def reset_ids(self):
        Subject.id_obj = itertools.count()
        Teacher.id_obj = itertools.count()
        StudentClass.id_obj = itertools.count()
        Lesson.id_obj = itertools.count()
        return

    def drop_current_time(self):
        for teacher in self.teachers:
            teacher.current_worktime = deepcopy(WorkTime.worktime)
        for subject in self.subjects:
            subject.current_worktime = deepcopy(WorkTime.worktime)
        for student_class in self.student_classes:
            student_class.current_worktime = deepcopy(WorkTime.worktime)
        for lesson in self.lessons:
            lesson.current_worktime = deepcopy(WorkTime.worktime)
        return

    def pop_subject(self, position):
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

    def pop_class(self, position):
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

    def pop_teacher(self, position):
        popped = self.teachers.pop(position)

        for i in range(position, len(self.teachers)):
            self.teachers[i].id = i
        Teacher.id_obj = itertools.count(len(self.teachers))

        length = len(self.lessons)
        i = 0
        while i != length:
            if self.lessons[i].teacher == popped:
                self.pop_lesson(i)
                length -= 1
            else:
                i += 1
        return

    def pop_lesson(self, position):
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

    def update_lesson_amount(self, lesson: Lesson, old_amount):
        amount = lesson.amount - old_amount
        if amount == 0:
            return
        elif amount > 0:
            for i in range(amount):
                self.unallocated.append(lesson)
            self.unallocated.sort(key=lambda x: x.id, reverse=False)
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

    def append_pos(self, sender: Lesson, from_day: int = -1) -> (list[bool], list[list[list[Lesson]]]):
        times = [[sender.is_available(day, les_pos) for les_pos in range(self.amount_lessons)
                  ] for day in range(self.amount_days)]
        conflicts = [[[] for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]
        for day in range(self.amount_days):
            for les_pos in range(self.amount_lessons):
                for receiver in self.timetable[day][les_pos]:
                    if receiver == sender and day != from_day:
                        for pos in range(self.amount_lessons):
                            times[day][pos] = False
                            conflicts[day][pos].append({"lesson": receiver, "day": day, "position": les_pos})
                        break

                    if receiver.teacher == sender.teacher:
                        if receiver.student_class != sender.student_class:
                            times[day][les_pos] = False
                            conflicts[day][les_pos].append({"lesson": receiver, "day": day, "position": les_pos})
                            continue
        return times, conflicts

    def toJSON(self):
        school_tojson = {"name": self.name,
                         "amount_days": self.amount_days,
                         "amount_lessons": self.amount_lessons,
                         "teachers": [teacher.__dict__ for teacher in self.teachers],
                         "subjects": [subject.__dict__ for subject in self.subjects],
                         "student_classes": [student_class.__dict__ for student_class in self.student_classes],
                         "lessons": [lesson.toJSON() for lesson in self.lessons],
                         "timetable": [
                             [
                                 [
                                     {"lesson": lesson.id} for lesson in les_pos
                                 ] for les_pos in day
                             ] for day in self.timetable
                         ],
                         "unallocated": [
                             {"lesson": lesson.id} for lesson in self.unallocated
                         ]
                         }
        return school_tojson
