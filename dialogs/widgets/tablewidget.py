from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPoint

import utils
from schooldata.data import SchoolData
from schooldata.school import School, Lesson, StudentClass


class ConflictMenuEvent(QtGui.QContextMenuEvent):
    def __init__(self, point: QPoint, position: (int, int, int, int)):
        super(ConflictMenuEvent, self).__init__(QtGui.QContextMenuEvent.Reason(1), point)
        self.position = position


class ConflictAction(QtWidgets.QWidgetAction):
    def __init__(self, parent, conflicts, to_day, to_les_pos):
        super(ConflictAction, self).__init__(parent)
        widget = QtWidgets.QWidget()
        v_layout = self.create_labels(conflicts, to_day, to_les_pos)
        widget.setLayout(v_layout)
        self.setDefaultWidget(widget)

    @staticmethod
    def create_labels(conflicts, to_day, to_les_pos) -> QtWidgets.QVBoxLayout:
        v_layout = QtWidgets.QVBoxLayout()

        for conflict in conflicts[to_day][to_les_pos]:
            tool_string = ''
            tool_string += f'{conflict["lesson"].subject.abbreviation} ({conflict["lesson"].student_class.name})' \
                           f' - {SchoolData.get_day_abb(conflict["day"])} {conflict["position"] + 1}'
            label = QtWidgets.QLabel(tool_string)
            v_layout.addWidget(label)

        if len(conflicts[to_day][to_les_pos]) == 0:
            tool_string = 'Не соответствует рабочей неделе'
            label = QtWidgets.QLabel(tool_string)
            v_layout.addWidget(label)

        return v_layout


class HeaderItem(QtWidgets.QTableWidgetItem):
    def __init__(self, student_class: StudentClass):
        super().__init__()
        self.setText(student_class.name)
        self.student_class = student_class

    def update(self) -> None:
        self.setText(self.student_class.name)
        return


class TimeTableItem(QtWidgets.QTableWidgetItem):
    def __init__(self, lesson: Lesson):
        super().__init__(lesson.subject.name)
        self.lesson = lesson
        self.setText(lesson.subject.abbreviation)
        self.setToolTip(self.set_tooltip_info())

    def set_tooltip_info(self):
        tooltip = f'{str(self.lesson.subject.abbreviation or "")} - {self.lesson.subject.name}\n' \
                  f'{self.lesson.student_class.name}\n' \
                  f'{str(self.lesson.teacher.abbreviation or "")} - ' \
                  f'{str(self.lesson.teacher.family or "")} {str(self.lesson.teacher.name or "")}'
        return tooltip

    def update(self):
        self.setText(self.lesson.subject.abbreviation)
        return


class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.mainapp = None
        self.swapping_available = []
        self.conflicts = []
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)

    def create_table(self, days_amount: int = 5, lessons_amount: int = 8):
        self.setRowCount(0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnCount(days_amount * lessons_amount)
        self.verticalHeader().setMinimumSize(31, 0)

        lessons_name = [f'{(i % lessons_amount) + 1}' for i in range(days_amount * lessons_amount)]
        self.setHorizontalHeaderLabels(lessons_name)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.horizontalHeader().setFont(font)

    def fill_table(self, school: School):
        self.setRowCount(0)
        self.setRowCount(len(school.student_classes))

        vertical_headers = [st_class.name for st_class in school.student_classes]
        self.setVerticalHeaderLabels(vertical_headers)

        for i in range(self.rowCount()):
            self.setVerticalHeaderItem(i, HeaderItem(school.student_classes[i]))
            self.setRowHeight(i, 28)
        for j in range(self.columnCount()):
            day, les_pos = utils.column_to_days_lessons(j, school.amount_lessons)
            for lesson in school.timetable[day][les_pos]:
                self.setItem(lesson.student_class.id, j, TimeTableItem(lesson))

    def mark_conflicts(self, amount_lessons):
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            day, les_pos = utils.column_to_days_lessons(i, amount_lessons)

            if self.swapping_available[day][les_pos]:
                item.setBackground(QtGui.QColor(0, 204, 0))
            else:
                item.setBackground(QtGui.QColor(204, 0, 0))
            self.setHorizontalHeaderItem(i, item)
        return

    def reset_conflicts(self):
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            item.setBackground(QtGui.QColor(255, 255, 255))
            self.setHorizontalHeaderItem(i, item)

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        from_index = self.selectedIndexes()[0]
        from_item = self.itemFromIndex(from_index)
        if from_item is None:
            return

        school = self.mainapp.school
        from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)

        self.swapping_available, self.conflicts = school.swapping_pos(from_item.lesson, from_day, from_les_pos)
        self.mark_conflicts(school.amount_lessons)

        super(MyTableWidget, self).startDrag(supportedActions)

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        self.reset_conflicts()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        school = self.mainapp.school
        from_index = self.selectedIndexes()[0]
        from_item = self.itemFromIndex(from_index)

        point = QPoint(int(event.position().x()), int(event.position().y()))
        to_index = self.indexAt(point)
        to_item = self.item(to_index.row(), to_index.column())

        if from_index.row() != to_index.row() or from_item is None:
            event.ignore()
            self.reset_conflicts()
            return

        from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)
        to_day, to_les_pos = utils.column_to_days_lessons(to_index.column(), school.amount_lessons)

        is_swapping_available = self.swapping_available[to_day][to_les_pos]
        if not is_swapping_available:
            position = (from_day, from_les_pos, to_day, to_les_pos)
            is_swapping_available = self.contextMenuEvent(ConflictMenuEvent(self.mapToGlobal(point), position))

        if is_swapping_available:
            super(MyTableWidget, self).dropEvent(event)
            self.setItem(to_index.row(), to_index.column(), from_item)
            self._replace(school, from_item.lesson, from_day, from_les_pos, to_day, to_les_pos)

            if to_item is not None:
                self.setItem(from_index.row(), from_index.column(), TimeTableItem(to_item.lesson))
                self._replace(school, to_item.lesson, to_day, to_les_pos, from_day, from_les_pos)
            event.accept()

        self.reset_conflicts()
        return

    @staticmethod
    def _replace(school: School, from_lesson: Lesson, from_day, from_les_pos, to_day, to_les_pos):
        for lesson in range(len(school.timetable[from_day][from_les_pos])):
            if school.timetable[from_day][from_les_pos][lesson] == from_lesson:
                school.timetable[from_day][from_les_pos].pop(lesson)
                from_lesson.set_available(from_day, from_les_pos)
                break
        school.timetable[to_day][to_les_pos].append(from_lesson)
        from_lesson.set_unavailable(to_day, to_les_pos)
        return

    def contextMenuEvent(self, a0: ConflictMenuEvent) -> bool:
        from_index = self.selectedIndexes()[0]
        from_item = self.itemFromIndex(from_index)
        if from_item is None:
            return

        menu = QtWidgets.QMenu()
        menu.setWindowTitle('Несоответствия')

        conflict_action = ConflictAction(menu, self.conflicts, a0.position[2], a0.position[3])

        menu.addAction(conflict_action)
        cancel_action = menu.addAction('Отменить')
        place_action = menu.addAction('Игнорировать и поместить')
        action = menu.exec(a0.pos())
        if action == cancel_action:
            return False
        elif action == place_action:
            return True
