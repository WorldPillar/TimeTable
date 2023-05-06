import json

from schooldata.school import Teacher, Subject, StudentClass, Lesson, School


class JSONProcessor:

    @staticmethod
    def json_read(root: str):
        try:
            f = open(root, 'r', encoding='utf8')
        except FileExistsError:
            print('Cant open file')
        else:
            with f:
                try:
                    import_data = json.load(f)
                    school = JSONProcessor._json_parse(import_data)
                    return school
                except SyntaxError:
                    print('Cant parse file')

    @staticmethod
    def _json_parse(import_data: dict) -> School:
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
            current_worktime = subject['current_worktime']
            new_subject = Subject(name, abbreviation)
            new_subject.worktime = worktime
            new_subject.current_worktime = current_worktime
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
            teacher = school.teachers[lesson['teacher']]
            student_class = school.student_classes[lesson['student_class']]
            amount = lesson['amount']
            current_worktime = lesson['current_worktime']
            new_lesson = Lesson(subject, teacher, student_class, amount)
            new_lesson.current_worktime = current_worktime
            school.lessons.append(new_lesson)

        timetable = import_data['timetable']
        school.timetable = [[[school.lessons[lesson['lesson']] for lesson in les_pos] for les_pos in day
                             ] for day in timetable]

        unallocated = import_data['unallocated']
        school.unallocated = [school.lessons[lesson['lesson']] for lesson in unallocated]
        return school

    @staticmethod
    def json_save(root: str, school: School):
        try:
            with open(root, 'w', encoding='utf8') as f:
                json.dump(school.toJSON(), f, ensure_ascii=False, indent=4)
        except IOError:
            print('Cant save file')
