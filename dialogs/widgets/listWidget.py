from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QAbstractItemView

import utils
from schooldata.school import Lesson, StudentClass, Subject, Teacher, School
from dialogs.widgets.tablewidget import MyTableWidget


class ListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, lesson: Lesson):
        super().__init__(lesson.subject.name)
        self.lesson = lesson
        self.conflicts = []
        self.setText(lesson.subject.abbreviation)
        self.setToolTip(self.set_tooltip_info())
        self.set_controls()

    def set_controls(self):
        self.setSizeHint(QSize(45, 28))
        self.setBackground(QtGui.QColor(255, 255, 255))
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_tooltip_info(self):
        tooltip = f'{str(self.lesson.subject.abbreviation or "")} - {self.lesson.subject.name}\n' \
                  f'{self.lesson.student_class.name}\n' \
                  f'{str(self.lesson.teacher.abbreviation or "")} - ' \
                  f'{str(self.lesson.teacher.family or "")} {str(self.lesson.teacher.name or "")}'
        return tooltip

    def update(self):
        self.setText(self.lesson.subject.abbreviation)
        return


class MyListWidget(QtWidgets.QListWidget):
    def __init__(self, parent, timetable: MyTableWidget):
        super(MyListWidget, self).__init__(parent)
        self.mainapp = parent
        self.set_drag_and_drop()

        self.setToolTip('Список нераспределенных уроков')

        self.timetable = timetable
        self.last_selected_row = None

    def set_drag_and_drop(self):
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setDragDropOverwriteMode(False)
        self.setFlow(QtWidgets.QListWidget.Flow.LeftToRight)
        self.setWrapping(True)
        self.setFixedHeight(90)
        self.setSpacing(5)
        self.setStyleSheet("""QListWidget{background: rgb(225, 225, 225);}""")
        return

    def add_unallocated_lessons(self, lessons: list[Lesson]):
        for lesson in lessons:
            item = ListWidgetItem(lesson)
            self.addItem(item)

    def add_unallocated_lesson(self, lesson: Lesson):
        item = ListWidgetItem(lesson)
        self.mainapp.school.unallocated.append(lesson)
        self.addItem(item)
        return

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        selected_item = self.selectedItems()[0]
        self.last_selected_row = selected_item.lesson.student_class.id
        self.set_color(True)

        self.timetable.swapping_available, self.timetable.conflicts =\
            self.mainapp.school.append_pos(selected_item.lesson)
        self.timetable.mark_conflicts(self.mainapp.school.amount_lessons)

        super(MyListWidget, self).startDrag(supportedActions)
        return
    
    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        sender = event.source()
        if sender == self:
            self.set_color(False)
            return

        school = self.mainapp.school
        from_index = self.timetable.selectedIndexes()[0]
        from_item = self.timetable.takeItem(from_index.row(), from_index.column())
        from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)

        self._throw_lesson(school, from_item.lesson, from_day, from_les_pos)
        self.add_unallocated_lesson(from_item.lesson)
        return

    @staticmethod
    def _throw_lesson(school: School, throw_lesson: Lesson, day: int, les_pos: int):
        for lesson in range(len(school.timetable[day][les_pos])):
            if school.timetable[day][les_pos][lesson] == throw_lesson:
                school.timetable[day][les_pos].pop(lesson)
                throw_lesson.set_available(day, les_pos)
                return
        return

    def takeItem(self, row: int) -> QtWidgets.QListWidgetItem:
        pop_item = self.item(row)
        pop_lesson = pop_item.lesson
        for lesson in range(len(self.mainapp.school.unallocated)):
            if self.mainapp.school.unallocated[lesson] == pop_lesson:
                self.mainapp.school.unallocated.pop(lesson)
        return super(MyListWidget, self).takeItem(row)

    def set_color(self, on: bool):
        item = self.timetable.verticalHeaderItem(self.last_selected_row)
        if on:
            item.setBackground(QtGui.QColor(0, 204, 0))
        else:
            item.setBackground(QtGui.QColor(255, 255, 255))
        self.timetable.setVerticalHeaderItem(self.last_selected_row, item)
