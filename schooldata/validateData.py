from schooldata.school import School, Teacher, StudentClass


class Validator:
    @staticmethod
    def _worktime_counter(worktime: list[list[int]]) -> int:
        count = 0
        for day in worktime:
            for les_pos in day:
                count += les_pos
        return count

    @staticmethod
    def _create_comment(obj, worktime: int) -> str:
        type_obj = type(obj)
        if type_obj == StudentClass:
            name = 'класса'
        elif type_obj == Teacher:
            name = 'учителя'
        else:
            return ''

        comment = f'У {name} {obj.get_name()} больше уроков, ' \
                  f'чем свободных уроков в его рабочей неделе: {obj.lessons_count} > {worktime}'
        return comment

    @staticmethod
    def validate(school: School) -> list[str]:
        conflicts = []
        for teacher in school.teachers:
            workload = teacher.workload
            if workload is not None:
                if teacher.lessons_count > workload:
                    string = f'У учителя {teacher.get_name()} больше уроков, ' \
                             f'чем его рабочая ставка: {teacher.lessons_count} > {workload}'
                    conflicts.append(string)
            worktime = Validator._worktime_counter(teacher.worktime)
            if teacher.lessons_count > worktime:
                comment = Validator._create_comment(teacher, worktime)
                conflicts.append(comment)
        for student_class in school.student_classes:
            worktime = Validator._worktime_counter(student_class.worktime)
            if student_class.lessons_count > worktime:
                comment = Validator._create_comment(student_class, worktime)
                conflicts.append(comment)
        return conflicts
