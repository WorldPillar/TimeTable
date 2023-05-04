from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QAbstractItemView

import utils
from schooldata.data import SchoolData
from schooldata.school import School, Lesson, StudentClass


class ConflictMenuEvent(QtGui.QContextMenuEvent):
    def __init__(self, point: QPoint, position: (int, int), is_table_sender: bool):
        super(ConflictMenuEvent, self).__init__(QtGui.QContextMenuEvent.Reason(1), point)
        self.position = position
        self.is_table_sender = is_table_sender


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
        self.unallocated_list = None
        self.swapping_available = []
        self.conflicts = []
        self.last_selected_row = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setAcceptDrops(True)

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
            lessons_in_slot = school.timetable[day][les_pos]
            for lesson in lessons_in_slot:
                self.setItem(lesson.student_class.id, j, TimeTableItem(lesson))

    def set_color(self, on: bool):
        item = self.verticalHeaderItem(self.last_selected_row)
        if on:
            item.setBackground(QtGui.QColor(0, 204, 0))
        else:
            item.setBackground(QtGui.QColor(255, 255, 255))
        self.setVerticalHeaderItem(self.last_selected_row, item)

    def mark_conflicts(self, amount_lessons):
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            day, les_pos = utils.column_to_days_lessons(i, amount_lessons)

            if self.swapping_available[day][les_pos]:
                item.setBackground(QtGui.QColor(0, 204, 0))
            else:
                item.setBackground(QtGui.QColor(204, 0, 0))
            self.setHorizontalHeaderItem(i, item)
        # self.set_color(True)
        return

    def reset_conflicts(self):
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            item.setBackground(QtGui.QColor(255, 255, 255))
            self.setHorizontalHeaderItem(i, item)
        # self.set_color(False)

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        self.reset_conflicts()
        super(MyTableWidget, self).dragLeaveEvent(e)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        self.mark_conflicts(self.mainapp.school.amount_lessons)
        super(MyTableWidget, self).dragEnterEvent(e)

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        from_index = self.selectedIndexes()[0]
        from_item = self.itemFromIndex(from_index)
        if from_item is None:
            return

        school = self.mainapp.school
        from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)

        self.last_selected_row = from_item.lesson.student_class.id

        self.swapping_available, self.conflicts = school.append_pos(from_item.lesson, from_day)
        self.mark_conflicts(school.amount_lessons)

        super(MyTableWidget, self).startDrag(supportedActions)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        sender = event.source()
        self.dropData(event, sender)
        return

    def dropData(self, event: QtGui.QDropEvent, sender):
        school = self.mainapp.school
        from_index = sender.selectedIndexes()[0]
        from_item = sender.itemFromIndex(from_index)

        point = QPoint(int(event.position().x()), int(event.position().y()))
        to_index = self.indexAt(point)
        to_item = self.item(to_index.row(), to_index.column())

        if sender != self:
            if from_item.lesson.student_class.id != to_index.row() or from_item is None:
                event.ignore()
                self.reset_conflicts()
                return
        else:
            if from_index.row() != to_index.row() or from_item is None or from_index == to_index:
                event.ignore()
                self.reset_conflicts()
                return

        to_day, to_les_pos = utils.column_to_days_lessons(to_index.column(), school.amount_lessons)

        is_swapping_available = self.swapping_available[to_day][to_les_pos]
        if not is_swapping_available:
            position = (to_day, to_les_pos)

            is_self_sender = sender == self
            action = self.contextMenuEvent(ConflictMenuEvent(self.mapToGlobal(point), position, is_self_sender))

            if action == 1:
                self._throw_conflicts(school, to_day, to_les_pos)
                is_swapping_available = True
            elif action == 2:
                is_swapping_available = True

        if is_swapping_available:
            if to_item is not None:
                to_item = self.takeItem(to_index.row(), to_index.column())
                to_lesson = to_item.lesson

            if sender != self:
                from_item = self.unallocated_list.takeItem(from_index.row())
                from_lesson = from_item.lesson
                self.setItem(to_index.row(), to_index.column(), TimeTableItem(from_lesson))
                self._append_lesson(school, from_lesson, to_day, to_les_pos)
            else:
                from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)
                from_item = self.takeItem(from_index.row(), from_index.column())
                self.setItem(to_index.row(), to_index.column(), from_item)
                self._replace(school, from_item.lesson, from_day, from_les_pos, to_day, to_les_pos)

            if to_item is not None:
                self._throw_lesson(school, to_lesson, to_day, to_les_pos)

        if sender != self:
            self.unallocated_list.set_color(False)
        self.reset_conflicts()

    @staticmethod
    def _append_lesson(school: School, append_lesson: Lesson, day: int, les_pos: int):
        school.timetable[day][les_pos].append(append_lesson)
        append_lesson.set_unavailable(day, les_pos)
        return

    def _throw_lesson(self, school: School, throw_lesson: Lesson, day: int, les_pos: int):
        self.unallocated_list.add_unallocated_lesson(throw_lesson)

        for lesson in range(len(school.timetable[day][les_pos])):
            if school.timetable[day][les_pos][lesson] == throw_lesson:
                school.timetable[day][les_pos].pop(lesson)
                throw_lesson.set_available(day, les_pos)
                return
        return

    def _throw_conflicts(self, school: School, day: int, les_pos: int):
        for conflict in self.conflicts[day][les_pos]:
            conflict_day = conflict['day']
            conflict_position = conflict['position']
            conflict_lesson = conflict['lesson']
            for lesson in range(len(school.timetable[conflict_day][conflict_position])):
                if school.timetable[conflict_day][conflict_position][lesson] == conflict_lesson:
                    school.timetable[conflict_day][conflict_position].pop(lesson)

                    column = conflict_day * school.amount_lessons + conflict_position
                    self.takeItem(conflict_lesson.student_class.id, column)

                    conflict_lesson.set_available(day, les_pos)
                    self.unallocated_list.add_unallocated_lesson(conflict['lesson'])
                    break
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

    def contextMenuEvent(self, a0: ConflictMenuEvent) -> int:
        if a0.is_table_sender:
            from_index = self.selectedIndexes()[0]
            from_item = self.itemFromIndex(from_index)
            if from_item is None:
                return
        else:
            from_index = self.unallocated_list.selectedIndexes()[0]
            from_item = self.unallocated_list.itemFromIndex(from_index)
            if from_item is None:
                return

        menu = QtWidgets.QMenu()
        menu.setWindowTitle('Несоответствия')

        conflict_action = ConflictAction(menu, self.conflicts, a0.position[0], a0.position[1])

        menu.addAction(conflict_action)
        cancel_action = menu.addAction('Отменить')
        throw_action = menu.addAction('Выбросить несоответствия и поместить')
        place_action = menu.addAction('Игнорировать и поместить')
        action = menu.exec(a0.pos())
        if action == cancel_action:
            return 0
        elif action == throw_action:
            return 1
        elif action == place_action:
            return 2
