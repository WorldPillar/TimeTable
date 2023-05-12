import sys
from copy import deepcopy

from schooldata.school import School, Lesson


class ExtendedRecursiveSwapping:
    def __init__(self, school: School):
        self.school = deepcopy(school)
        self.amount_lessons = self.school.amount_lessons
        self.amount_days = self.school.amount_days
        self.school.timetable = [[[] for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]
        self.school.unallocated = []

    def sort(self):
        self.school.lessons.sort(key=lambda x: x.amount * x.duration, reverse=True)

    def start(self) -> School:
        self.sort()

        for lesson in range(len(self.school.lessons)):
            for lesson_amount in range(self.school.lessons[lesson].amount):
                is_append = False
                for i in range(self.amount_lessons - self.school.lessons[lesson].duration + 1):
                    if is_append:
                        break
                    for j in range(self.amount_days):
                        if self.try_insert_lesson(self.school, self.school.lessons[lesson], j, i):
                            is_append = True
                            break
                if not is_append:
                    copy_school, copy_lesson = self.copy_school_and_lesson(self.school, self.school.lessons[lesson])

                    is_swapped, school = self.recursive_swapping(copy_school, copy_lesson, 0)
                    if is_swapped:
                        self.school = school
                    else:
                        self.school.unallocated.append(self.school.lessons[lesson])
                        print('Не смогло распределить')
        count = 0
        for day in self.school.timetable:
            for les_pos in day:
                count += len(les_pos)
        lessons_count = 0
        for lesson in self.school.lessons:
            lessons_count += lesson.amount * lesson.duration
        print(f"Всего уроков: {lessons_count}")
        print(f"Не распределено уроков: {lessons_count - count}")
        self.school.lessons.sort(key=lambda x: x.id, reverse=False)
        return self.school

    @staticmethod
    def try_insert_lesson(school: School, lesson: Lesson, day: int, lesson_pos: int) -> bool:
        if lesson.is_available(day, lesson_pos) and lesson.current_available(day, lesson_pos):
            for i in range(lesson.duration):
                school.timetable[day][lesson_pos + i].append(lesson)
            lesson.set_unavailable(day, lesson_pos)
            return True
        else:
            return False

    @staticmethod
    def copy_school_and_lesson(school: School, lesson: Lesson) -> (School, Lesson):
        """
        Метод копирует школу и находит в ней урок, совпадающий с переданным.
        :param school: Объект класса School для копирования.
        :param lesson: Объект класса Lesson для поиска в скопированном объекте school.
        :return: Копия school и копия lesson
        """
        copy_school = deepcopy(school)
        copy_lesson = None
        for les in copy_school.lessons:
            if les.id == lesson.id:
                copy_lesson = les
        return copy_school, copy_lesson

    def recursive_swapping(self, school: School, unallocated_lesson: Lesson, step: int):
        if step == 14:
            # print(f'Слишком большая рекурсия\nНераспределенный урок: {unallocated_lesson.get_string()}')
            return False, None

        conflicts = self.find_conflicts(school, unallocated_lesson)

        is_swappable = True
        while is_swappable:

            (day, lesson_position) = self.find_min(conflicts, unallocated_lesson)
            if day == -1 or lesson_position == -1:
                print('Day and Lesson position is -1')
                print(f'Нераспределенный урок: {unallocated_lesson.get_string()}')
                break

            if step == 0:
                copy_school, copy_lesson = self.copy_school_and_lesson(school, unallocated_lesson)
                is_placed = self.replacing_lessons(copy_school, copy_lesson, day, lesson_position, conflicts, step)
                if is_placed:
                    return True, copy_school
            else:
                is_placed = self.replacing_lessons(school, unallocated_lesson, day, lesson_position, conflicts, step)
                if is_placed:
                    return True, school
                else:
                    is_swappable = False

            conflicts[day][lesson_position] = -1
        return False, None

    def try_to_place(self, school: School, popped_lesson: Lesson, step) -> (bool, School):
        """
        Метод, пытающийся поместить выкинутый урок обратно в школу. В удачном случае возвращает True, иначе рекурсивно
        вызывает метод recursive_swapping
        :param school: объект класса School, в который помещаются выкинутые уроки.
        :param popped_lesson: Выкинутый урок.
        :param step: Шаг рекурсии.
        :return: Результат рекурсии в виде bool и объект School.
        """
        for i in range(self.amount_lessons - popped_lesson.duration + 1):
            for j in range(self.amount_days):
                if self.try_insert_lesson(school, popped_lesson, j, i):
                    return True, school
        return self.recursive_swapping(school, popped_lesson, step + 1)

    def replacing_lessons(self, school: School, lesson: Lesson, day: int, les_pos: int, conflicts, step) -> bool:
        """
        Метод выкидывающий конфликтные уроки и поочерёдно пытающийся поместить их обратно в школу.
        :param school: Объект класса School
        :param lesson: Нераспределенный урок.
        :param day: Выбранный день, из которого будут выброшены конфликтные уроки.
        :param les_pos: Выбранная позиция урока, из которой будут выброшены конфликтные уроки.
        :param conflicts: Матрица конфликтов.
        :param step: Шаг рекурсии.
        :return: Результат в виде bool.
        """
        if lesson.id == 256:
            pass
        popped_lessons = self.throw_conflicts(school, lesson, day, les_pos)
        if conflicts[day][les_pos] >= 100:
            popped_lessons.append(self.throw_same_lesson(school, lesson, day))

        if not self.try_insert_lesson(school, lesson, day, les_pos):
            print(f'not insert but should {lesson.get_string()}')

        for lesson in popped_lessons:
            try_append, copy_school = self.try_to_place(school, lesson, step)
            if not try_append:
                return False
        return True

    def throw_conflicts(self, school: School, unallocated_lesson: Lesson, day: int, lesson_position: int) -> list[Lesson]:
        """
        Метод выбрасывает конфликтные уроки, мешающие поместить переданный в метод урок на определенную позицию дня.
        :return: Список выброшенных конфликтных уроков.
        """
        popped_lessons = []
        for d in range(unallocated_lesson.duration):
            lesson_position = lesson_position + d
            lessons_amount = len(school.timetable[day][lesson_position])
            i = 0
            while i != lessons_amount:
                same_teacher = school.timetable[day][lesson_position][i].teacher == unallocated_lesson.teacher
                same_class = school.timetable[day][lesson_position][i].student_class == unallocated_lesson.student_class
                if same_teacher or same_class:
                    popped = school.timetable[day][lesson_position][i]
                    school.remove_duration(popped, day, lesson_position)

                    popped.set_available(day, lesson_position)
                    popped_lessons.append(popped)
                    lessons_amount -= 1
                else:
                    i += 1
        return popped_lessons

    def throw_same_lesson(self, school: School, unallocated_lesson: Lesson, day: int) -> Lesson:
        """
        Метод, выбрасывающий конфликтный урок, совпадающий с нераспределенным в определенный день.
        :return: Выброшенный конфликтный урок.
        """
        for les_pos in range(len(school.timetable[day])):
            for lesson in range(len(school.timetable[day][les_pos])):
                if school.timetable[day][les_pos][lesson] == unallocated_lesson:
                    popped = school.timetable[day][les_pos][lesson]
                    school.remove_duration(popped, day, les_pos)

                    popped.set_available(day, les_pos)
                    return popped

    def find_conflicts(self, school: School, unallocated_lesson: Lesson) -> list[list[int]]:
        """
        Метод находит число конфликтов, мешающих поместить нераспределенный урок на данную позицию
        :param school:
        :param unallocated_lesson:
        :return: Список конфликтов
        """
        conflicts = [[0 for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]
        for i in range(self.amount_days):
            for j in range(self.amount_lessons - unallocated_lesson.duration + 1):
                for k in range(unallocated_lesson.duration):
                    if not unallocated_lesson.is_available(i, j):
                        conflicts[i][j] = -1
                        continue
                    for allocated_lesson in school.timetable[i][j]:
                        if allocated_lesson.teacher == unallocated_lesson.teacher:
                            conflicts[i][j] += 1
                        if allocated_lesson.student_class == unallocated_lesson.student_class:
                            conflicts[i][j] += 1
                    if not unallocated_lesson.is_available_today(i):
                        conflicts[i][j] += 100
        return conflicts

    def find_min(self, conflicts, unallocated_lesson: Lesson) -> (int, int):
        """
        Метод находит день и позицию урока с минимальным числом конфликтов.
        :return: (день, позиция урока)
        """
        minimum = sys.maxsize
        (day, lesson_position) = (-1, -1)
        for i in range(self.amount_days):
            for j in range(self.amount_lessons - unallocated_lesson.duration + 1):
                if conflicts[i][j] == -1 or conflicts[i][j] == 102:
                    continue
                if conflicts[i][j] < minimum:
                    minimum = conflicts[i][j]
                    (day, lesson_position) = (i, j)
        return day, lesson_position
