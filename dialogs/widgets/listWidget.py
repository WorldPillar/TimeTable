import logging

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QAbstractItemView, QListWidgetItem

import utils
from schooldata.school import Lesson, School
from dialogs.widgets.tablewidget import MyTableWidget


class ListWidgetItem(QtWidgets.QListWidgetItem):
    """
    Класс ячейки списка MyListWidget
    """

    def __init__(self, lesson: Lesson, amount: int = 1):
        super().__init__(lesson.subject.name)
        self.lesson = lesson
        self.amount = amount
        self.setText(lesson.subject.abbreviation)
        self.set_tooltip_info()
        self.set_controls()

    def set_controls(self) -> None:
        """
        Метод устанавливает внешний вид элемента.
        """
        self.setSizeHint(QSize(45, 28))
        self.setBackground(QtGui.QColor(255, 255, 255))
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return

    def set_tooltip_info(self) -> None:
        """
        Метод устанавливает tooltip элемента.
        """
        teachers_name = ''
        for teacher in self.lesson.teachers:
            teachers_name = teachers_name + f'{str(teacher.abbreviation or "")} - '\
                                            f'{str(teacher.family or "")} {str(teacher.name or "")}\n'
        tooltip = f'{str(self.lesson.subject.abbreviation or "")} - {self.lesson.subject.name}\n' \
                  f'{self.lesson.student_class.name}\n'\
                  + teachers_name + f'Длительность - {self.lesson.duration}\n'\
                  + f'Количество - {self.amount}\n'
        self.setToolTip(tooltip)
        return

    def update(self) -> None:
        """
        Метод обновляет текст элемента.
        """
        self.setText(self.lesson.subject.abbreviation)
        return

    def add_count(self) -> int:
        """
        Метод увеличивает количество уроков в элементе на 1.
        :return: Новое количество уроков.
        """
        self.amount += 1
        self.set_tooltip_info()
        return self.amount

    def remove_count(self) -> int:
        """
        Метод уменьшает количество уроков в элементе на 1.
        :return: Новое количество уроков.
        """
        self.amount -= 1
        self.set_tooltip_info()
        return self.amount


class MyListWidget(QtWidgets.QListWidget):
    """
    Класс списка нераспределенных уроков.
    """

    def __init__(self, parent, timetable: MyTableWidget):
        super(MyListWidget, self).__init__(parent)
        self.mainapp = parent
        self.set_drag_and_drop()

        self.setToolTip('Список нераспределенных уроков')

        self.timetable = timetable
        self.last_selected_row = None
        self.is_drop = False

    def set_drag_and_drop(self):
        """
        Метод устанавливает внешний вид списка и правила drag and drop.
        """
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

    def add_unallocated_lessons(self, lessons: list[Lesson]) -> None:
        """
        Метод переопределяет список нераспределенных уроков.
        """
        self.clear()
        if len(lessons) == 0:
            return
        prev_lesson = lessons[0]
        count = 0
        for lesson in lessons:
            # Увеличиваем количество совпадающих уроков, находящихся в списке нераспределенных
            if prev_lesson == lesson:
                count += 1
            else:
                item = ListWidgetItem(prev_lesson, count)
                self.addItem(item)
                count = 1
            prev_lesson = lesson

        item = ListWidgetItem(lesson, count)
        self.addItem(item)
        return

    def add_unallocated_lesson(self, lesson: Lesson) -> None:
        """
        Добавляет урок в список нераспределенных.
        """
        for pos in range(self.count()):
            # Если урок уже присутствует в списке, то увеличивается количество и выходит из метода.
            if lesson == self.item(pos).lesson:
                self.mainapp.school.unallocated.append(lesson)
                self.item(pos).add_count()
                return

        item = ListWidgetItem(lesson)
        self.mainapp.school.unallocated.append(lesson)
        self.addItem(item)
        return

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        """
        Метод переопределяет событие startDrag
        """
        self.is_drop = False
        school = self.mainapp.school
        self.timetable.clearSelection()

        selected_item = self.selectedItems()[0]
        self.last_selected_row = selected_item.lesson.student_class.id
        self.set_color(True)

        self.timetable.swapping_available, self.timetable.conflicts =\
            school.get_lesson_conflicts(selected_item.lesson)
        self.timetable.mark_conflicts(school.amount_lessons)

        super(MyListWidget, self).startDrag(supportedActions)
        self.set_color(False)
        return

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """
        Метод переопределяет событие dropEvent
        """
        self.is_drop = True
        sender = event.source()
        if sender == self:
            return

        try:
            self.timetable.is_drop = True
            school = self.mainapp.school
            from_index = self.timetable.selectedIndexes()[0]
            from_item = self.timetable.takeItem(from_index.row(), from_index.column())
            from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)

            self._throw_lesson(school, from_item.lesson, from_day, from_les_pos)
            self.add_unallocated_lesson(from_item.lesson)
            return
        except BaseException:
            logging.error('DROPEVENT_ERROR')
        return

    @staticmethod
    def _throw_lesson(school: School, throw_lesson: Lesson, day: int, les_pos: int) -> None:
        """
        Метод выбрасывает урок из расписания занятий.
        :param school: Школа, из расписания которой выбрасывается урок.
        :param throw_lesson: Выбрасываемый урок.
        :param day: День, в котором находится выбрасываемый урок.
        :param les_pos: Позиция дня, в которой находится выбрасываемый урок.
        """
        school.remove_duration(throw_lesson, day, les_pos)
        throw_lesson.set_available(day, les_pos)
        return

    def takeItem(self, row: int) -> QtWidgets.QListWidgetItem:
        """
        Метод переопределяет событие takeItem
        """
        school = self.mainapp.school

        pop_item = self.item(row)
        pop_lesson = pop_item.lesson
        for lesson in range(len(school.unallocated)):
            if school.unallocated[lesson] == pop_lesson:
                school.unallocated.pop(lesson)
                break
        if pop_item.remove_count() == 0:
            return super(MyListWidget, self).takeItem(row)
        else:
            return pop_item

    def get_available_items(self, class_id: int, to_day: int, to_les_pos: int) -> list[QListWidgetItem]:
        """
        Метод возвращает список свободных уроков.
        :param class_id: id класса, для которого выбираются уроки.
        :param to_day: День, для которого выбираются уроки.
        :param to_les_pos: Позиция дня, для которой выбираются уроки.
        :return: Список ListWidgetItem со свободными уроками.
        """
        available_items = []

        for pos in range(self.count()):
            if self.item(pos).lesson.student_class.id != class_id:
                continue
            if self.item(pos).lesson.is_available(to_day, to_les_pos):
                available_items.append(self.item(pos))
        return available_items

    def set_color(self, on: bool) -> None:
        """
        Метод меняет цвет заголовков MyTableWidget
        :param on: Менять цвет или сбросить.
        """
        item = self.timetable.verticalHeaderItem(self.last_selected_row)
        if on:
            item.setBackground(QtGui.QColor(0, 204, 0))
        else:
            item.setBackground(QtGui.QColor(255, 255, 255))
        self.timetable.setVerticalHeaderItem(self.last_selected_row, item)
        return
