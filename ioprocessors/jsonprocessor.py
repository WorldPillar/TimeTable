import json

from schooldata.school import Teacher, Subject, StudentClass, Lesson, School


class JSONProcessor:

    @staticmethod
    def json_read(root: str) -> School:
        """
        Метод считывает файл и преобразует его в объект класса School.
        :param root: Путь к файл.
        """
        try:
            f = open(root, 'r', encoding='utf8')
        except FileExistsError:
            print('Cant open file')
        else:
            with f:
                import_data = json.load(f)
                school = JSONProcessor._json_parse(import_data)
                return school

    @staticmethod
    def _json_parse(import_data: dict) -> School:
        """
        Метод считывает загруженный файл в виде dict и возвращает созданный объект School.
        """
        name = import_data['name']
        amount_days = import_data['amount_days']
        amount_lessons = import_data['amount_lessons']
        school = School(name, amount_days, amount_lessons)

        for teacher in import_data['teachers']:
            family = teacher['family']
            name = teacher['name']
            workload = teacher['workload']
            abbreviation = teacher['abbreviation']
            worktime = teacher['worktime']
            current_worktime = teacher['current_worktime']
            new_teacher = Teacher(family, name, workload, abbreviation)
            new_teacher.worktime = worktime
            new_teacher.current_worktime = current_worktime
            school.teachers.append(new_teacher)

        for subject in import_data['subjects']:
            name = subject['name']
            abbreviation = subject['abbreviation']
            worktime = subject['worktime']
            new_subject = Subject(name, abbreviation)
            new_subject.worktime = worktime
            school.subjects.append(new_subject)

        for student_class in import_data['student_classes']:
            name = student_class['name']
            abbreviation = student_class['abbreviation']
            worktime = student_class['worktime']
            current_worktime = student_class['current_worktime']
            new_class = StudentClass(name, abbreviation)
            new_class.worktime = worktime
            new_class.current_worktime = current_worktime
            school.student_classes.append(new_class)

        for lesson in import_data['lessons']:
            subject = school.subjects[lesson['subject']]
            teachers = [school.teachers[teacher_id['teacher']] for teacher_id in lesson['teachers']]
            student_class = school.student_classes[lesson['student_class']]
            amount = lesson['amount']
            duration = lesson['duration']
            start_end_positions = lesson['start_end_positions']
            new_lesson = Lesson(subject, teachers[0], student_class, amount, duration)
            new_lesson.update_lesson_data(teachers=teachers)
            new_lesson.start_end_positions = start_end_positions
            school.lessons.append(new_lesson)

        for lesson in school.lessons:
            append = 0
            for positions in lesson.start_end_positions:
                for position in range(positions['start'], positions['end'] + 1):
                    school.timetable[positions['day']][position].append(lesson)
                append += 1
            for i in range(lesson.amount - append):
                school.unallocated.append(lesson)
        return school

    @staticmethod
    def json_save(root: str, school: School) -> None:
        """
        Метод сохраняет файл.
        :param root: Путь к файлу.
        :param school: Объект класса School для сохранения.
        """
        with open(root, 'w', encoding='utf8') as f:
            json.dump(school.toJSON(), f, ensure_ascii=False, indent=4)
        return
