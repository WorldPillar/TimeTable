import random
import sys
from copy import deepcopy

from schooldata.school import School, Lesson


class RecursiveSwapping:
    def __init__(self, school: School):
        self.school = deepcopy(school)
        self.amount_lessons = self.school.amount_lessons
        self.amount_days = self.school.amount_days

        self.timeslots = [[[] for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]

    def sort(self):
        self.school.lessons.sort(key=lambda x: x.amount, reverse=True)

    def shuffle(self):
        random.shuffle(self.school.lessons)

    def start(self):
        self.sort()

        for lesson in self.school.lessons:
            for lesson_amount in range(lesson.amount):
                is_append = False
                for i in range(self.amount_lessons):
                    if is_append:
                        break
                    for j in range(self.amount_days):
                        if self.try_insert_lesson(lesson, j, i):
                            is_append = True
                            break
                if not is_append:
                    if not self.recursive_swapping(lesson, 0):
                        print('Не смогло распределить')

        count = 0
        for day in self.timeslots:
            for les_pos in day:
                count += len(les_pos)
        lessons_count = 0
        for lesson in self.school.lessons:
            lessons_count += lesson.amount

        print(f"Всего уроков: {lessons_count}")
        print(f"Не распределено уроков: {lessons_count - count}")
        self.school.lessons.sort(key=lambda x: x.id, reverse=False)
        self.school.timetable = self.timeslots
        return self.school

    def try_insert_lesson(self, lesson: Lesson, day: int, lesson_pos: int) -> bool:
        if lesson.is_available(day, lesson_pos) and lesson.current_available(day, lesson_pos):
            self.timeslots[day][lesson_pos].append(lesson)
            lesson.set_unavailable(day, lesson_pos)
            return True
        else:
            return False

    def recursive_swapping(self, unallocated_lesson: Lesson, step: int) -> bool:
        if step == 14:
            print(f'Слишком большая рекурсия\nНераспределенный урок: {unallocated_lesson.get_string()}')
            return False

        conflicts = [[0 for _ in range(self.amount_lessons)] for _ in range(self.amount_days)]
        for i in range(self.amount_days):
            for j in range(self.amount_lessons):
                if not unallocated_lesson.is_available(i, j):
                    conflicts[i][j] = -1
                    continue
                for allocated_lesson in self.timeslots[i][j]:
                    if allocated_lesson.teacher == unallocated_lesson.teacher:
                        conflicts[i][j] += 1
                    if allocated_lesson.student_class == unallocated_lesson.student_class:
                        conflicts[i][j] += 1
                if not unallocated_lesson.is_available_today(i):
                    conflicts[i][j] += 100

        (day, lesson_position) = self.find_min(conflicts)
        if day == -1 or lesson_position == -1:
            print('Day and Lesson position is -1')
            return False

        popped_lessons = self.pop(unallocated_lesson, day, lesson_position)
        if conflicts[day][lesson_position] >= 100:
            popped_lessons.append(self.pop_same_lesson(unallocated_lesson, day))

        if not self.try_insert_lesson(unallocated_lesson, day, lesson_position):
            print('not insert but should')

        is_placed = True
        for lesson in popped_lessons:
            try_append = self.try_to_place(lesson, step)
            is_placed = is_placed and try_append

        return is_placed

    def try_to_place(self, popped_lesson: Lesson, step):
        for i in range(self.amount_lessons):
            for j in range(self.amount_days):
                if self.try_insert_lesson(popped_lesson, j, i):
                    return True
        return self.recursive_swapping(popped_lesson, step + 1)

    def pop(self, unallocated_lesson: Lesson, day: int, lesson_position: int) -> list[Lesson]:
        popped_lessons = []
        lessons_amount = len(self.timeslots[day][lesson_position])
        i = 0
        while i != lessons_amount:
            if self.timeslots[day][lesson_position][i].teacher == unallocated_lesson.teacher or \
                    self.timeslots[day][lesson_position][i].student_class == unallocated_lesson.student_class:

                popped = self.timeslots[day][lesson_position].pop(i)
                popped.set_available(day, lesson_position)
                popped_lessons.append(popped)
                lessons_amount -= 1
            else:
                i += 1
        return popped_lessons

    def pop_same_lesson(self, unallocated_lesson: Lesson, day: int) -> Lesson:
        for les_pos in range(len(self.timeslots[day])):
            for lesson in range(len(self.timeslots[day][les_pos])):
                if self.timeslots[day][les_pos][lesson] == unallocated_lesson:
                    popped = self.timeslots[day][les_pos].pop(lesson)
                    popped.set_available(day, les_pos)
                    return popped

    def find_min(self, conflicts) -> (int, int):
        minimum = sys.maxsize
        (day, lesson_position) = (-1, -1)
        for i in range(self.amount_days):
            for j in range(self.amount_lessons):
                if conflicts[i][j] == -1 or conflicts[i][j] == 102:
                    continue
                if conflicts[i][j] < minimum:
                    minimum = conflicts[i][j]
                    (day, lesson_position) = (i, j)
        return day, lesson_position
