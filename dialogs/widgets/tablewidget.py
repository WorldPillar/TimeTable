import logging

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QAbstractItemView

import utils
from schooldata.data import SchoolData
from schooldata.school import School, Lesson, StudentClass


class BookedMenuLabelAction(QtWidgets.QWidgetAction):
    """
    Класс Действие-надпись у меню для занятой ячейки таблицы.
    """

    def __init__(self, parent, lesson: Lesson):
        super(BookedMenuLabelAction, self).__init__(parent)
        widget = QtWidgets.QWidget()

        v_layout = QtWidgets.QVBoxLayout()
        string = f'{lesson.subject.abbreviation} ({lesson.student_class.abbreviation})'
        label = QtWidgets.QLabel(string)
        v_layout.addWidget(label)

        widget.setLayout(v_layout)
        self.setDefaultWidget(widget)


class EmptyMenuLabelAction(QtWidgets.QWidgetAction):
    """
    Класс Действие-надпись у меню для пустой ячейки таблицы.
    """

    def __init__(self, parent, student_class: StudentClass):
        super(EmptyMenuLabelAction, self).__init__(parent)
        widget = QtWidgets.QWidget()

        v_layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(student_class.get_full_name())
        v_layout.addWidget(label)

        widget.setLayout(v_layout)
        self.setDefaultWidget(widget)


class ConflictAction(QtWidgets.QWidgetAction):
    """
    Класс Действие-надпись у меню, список конфликтных уроков.
    """

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
    """
    Класс ячейки заголовка таблицы.
    """

    def __init__(self, student_class: StudentClass):
        super().__init__()
        self.setText(student_class.name)
        self.student_class = student_class
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def update(self) -> None:
        self.setText(self.student_class.name)
        return


class TimeTableItem(QtWidgets.QTableWidgetItem):
    """
    Класс ячейки таблицы.
    """

    def __init__(self, lesson: Lesson):
        super().__init__(lesson.subject.name)
        self.lesson = lesson
        self.setText(lesson.subject.abbreviation)
        self.set_tooltip_info()
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_tooltip_info(self) -> None:
        teachers_name = ''
        for teacher in self.lesson.teachers:
            teachers_name = teachers_name + f'{str(teacher.abbreviation or "")} - '\
                                            f'{str(teacher.family or "")} {str(teacher.name or "")}\n'
        tooltip = f'{str(self.lesson.subject.abbreviation or "")} - {self.lesson.subject.name}\n' \
                  f'{self.lesson.student_class.name}\n' + teachers_name
        self.setToolTip(tooltip)
        return

    def update(self) -> None:
        self.setText(self.lesson.subject.abbreviation)
        return


class MyTableWidget(QtWidgets.QTableWidget):
    """
    Таблица расписания занятий.
    """

    def __init__(self, parent, mainapp):
        super(MyTableWidget, self).__init__(parent)
        self.mainapp = mainapp
        self.unallocated_list = None
        self.swapping_available = []
        self.conflicts = []
        self.last_selected_row = None
        self.is_drop = False

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setAcceptDrops(True)

    def create_table(self, days_amount: int = 5, lessons_amount: int = 8) -> None:
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
        return

    def setItem(self, row: int, column: int, item: QtWidgets.QTableWidgetItem) -> None:
        row = row
        column = column
        self.setSpan(row, column, 1, item.lesson.duration)
        super(MyTableWidget, self).setItem(row, column, item)
        return

    def takeItem(self, row: int, column: int) -> QtWidgets.QTableWidgetItem:
        self.setSpan(row, column, 1, 1)
        return super(MyTableWidget, self).takeItem(row, column)

    def fill_table(self, school: School) -> None:
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
                if lesson.get_start_end_lesson(day, les_pos) is not None:
                    if lesson.get_start_end_lesson(day, les_pos)['start'] != les_pos:
                        continue
                self.setItem(lesson.student_class.id, j, TimeTableItem(lesson))
        return

    def set_color(self, on: bool) -> None:
        item = self.verticalHeaderItem(self.last_selected_row)
        if on:
            item.setBackground(QtGui.QColor(0, 204, 0))
        else:
            item.setBackground(QtGui.QColor(255, 255, 255))
        self.setVerticalHeaderItem(self.last_selected_row, item)
        return

    def mark_conflicts(self, amount_lessons) -> None:
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            day, les_pos = utils.column_to_days_lessons(i, amount_lessons)

            if self.swapping_available[day][les_pos]:
                item.setBackground(QtGui.QColor(0, 204, 0))
            else:
                item.setBackground(QtGui.QColor(204, 0, 0))
            self.setHorizontalHeaderItem(i, item)
        return

    def reset_conflicts(self) -> None:
        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            item.setBackground(QtGui.QColor(255, 255, 255))
            self.setHorizontalHeaderItem(i, item)
        return

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        self.mark_conflicts(self.mainapp.school.amount_lessons)
        if len(self.selectedIndexes()) != 0:
            index = self.selectedIndexes()[0]
            if index is not None:
                item = self.itemFromIndex(index)
                if item is not None:
                    item.setText('')
                    self.setSpan(index.row(), index.column(), 1, 1)

        super(MyTableWidget, self).dragEnterEvent(e)
        return

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        self.is_drop = False

        from_index = self.selectedIndexes()[0]
        from_item = self.itemFromIndex(from_index)
        if from_item is None:
            return

        school = self.mainapp.school
        from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)

        self.last_selected_row = from_item.lesson.student_class.id
        self.set_color(True)

        self.swapping_available, self.conflicts = school.get_lesson_conflicts(from_item.lesson, from_day)
        self.mark_conflicts(school.amount_lessons)

        super(MyTableWidget, self).startDrag(supportedActions)
        self.set_color(False)

        self.reset_conflicts()
        from_item.update()
        if self.is_drop:
            self.setSpan(from_index.row(), from_index.column(), 1, 1)
        else:
            self.setSpan(from_index.row(), from_index.column(), 1, from_item.lesson.duration)
        return

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        sender = event.source()
        try:
            self.is_drop, newItem = self.dropData(event, sender)
            self.reset_conflicts()
            if self.is_drop:
                super(MyTableWidget, self).dropEvent(event)
                newItem.set_tooltip_info()
            else:
                event.ignore()
            return
        except BaseException:
            logging.error('TABLE_DROPEVENT_ERROR')
        return
    def dropData(self, event: QtGui.QDropEvent, sender) -> (bool, TimeTableItem):
        school = self.mainapp.school
        from_index = sender.selectedIndexes()[0]
        from_item = sender.itemFromIndex(from_index)

        point = QPoint(int(event.position().x()), int(event.position().y()))
        to_index = self.indexAt(point)
        to_day, to_les_pos = utils.column_to_days_lessons(to_index.column(), school.amount_lessons)

        is_ignore = (to_les_pos + from_item.lesson.duration) > school.amount_lessons
        is_ignore = is_ignore or (from_item.lesson.student_class.id != to_index.row() or from_item is None)
        if sender == self:
            is_ignore = is_ignore or (from_index == to_index)

        if is_ignore:
            event.ignore()
            return False, None

        is_swapping_available = self.swapping_available[to_day][to_les_pos]
        if not is_swapping_available:
            position = (to_day, to_les_pos)
            action = self.dropContextMenu(self.mapToGlobal(point), position)

            if action == 1:
                self._throw_conflicts(school, to_day, to_les_pos)
                is_swapping_available = True
            elif action == 2:
                is_swapping_available = True

        newItem = None
        if is_swapping_available:
            for d in range(from_item.lesson.duration):
                to_item = self.item(to_index.row(), to_index.column() + d)
                if to_item is not None:
                    if to_item != from_item:
                        to_item = self.takeItem(to_index.row(), to_index.column() + d)
                        to_lesson = to_item.lesson
                        self._throw_lesson(school, to_lesson, to_day, to_les_pos + d)

            if sender != self:
                from_item = self.unallocated_list.takeItem(from_index.row())
                from_lesson = from_item.lesson
                newItem = TimeTableItem(from_lesson)
                self.setItem(to_index.row(), to_index.column(), newItem)
                self._append_lesson(school, from_lesson, to_day, to_les_pos)
            else:
                from_day, from_les_pos = utils.column_to_days_lessons(from_index.column(), school.amount_lessons)
                from_item = self.takeItem(from_index.row(), from_index.column())
                self.setItem(to_index.row(), to_index.column(), from_item)
                self._replace(school, from_item.lesson, from_day, from_les_pos, to_day, to_les_pos)
                newItem = from_item

        if sender != self:
            self.unallocated_list.set_color(False)
        return is_swapping_available, newItem

    @staticmethod
    def _append_lesson(school: School, append_lesson: Lesson, day: int, les_pos: int):
        """
        Метод помещения урока в timetable.
        """
        for d in range(append_lesson.duration):
            school.timetable[day][les_pos + d].append(append_lesson)
        append_lesson.set_unavailable(day, les_pos)
        return

    def _throw_lesson(self, school: School, throw_lesson: Lesson, day: int, les_pos: int):
        """
        Метод удаления урока из timetable и помещения его в список нераспределенных уроков.
        """
        self.unallocated_list.add_unallocated_lesson(throw_lesson)
        school.remove_duration(throw_lesson, day, les_pos)
        throw_lesson.set_available(day, les_pos)
        return

    def _throw_conflicts(self, school: School, day: int, les_pos: int):
        """
        Метод удаления конфликтов из таблицы.
        """
        self.conflicts[day][les_pos].sort(key=lambda x: x['position'], reverse=True)
        del_conf = list({v['lesson']: v for v in self.conflicts[day][les_pos]}.values())
        for conflict in del_conf:
            conflict_day = conflict['day']
            conflict_position = conflict['position']
            conflict_lesson = conflict['lesson']
            position = conflict_lesson.get_start_end_lesson(conflict_day, conflict_position)

            self._throw_lesson(school, conflict_lesson, conflict_day, conflict_position)

            column = conflict_day * school.amount_lessons + position['start']
            self.takeItem(conflict_lesson.student_class.id, column)
        return

    def _replace(self, school: School, from_lesson: Lesson, from_day, from_les_pos, to_day, to_les_pos):
        """
        Метод удаляет lesson из одной позиции timetable и ставит его в другую позицию.
        :param school: объект класса School с timetable.
        :param from_lesson: lesson, который необходимо переставить.
        :param from_day: День, из которого необходимо переставить lesson.
        :param from_les_pos: Позиция в дне, из которой необходимо переставить lesson.
        :param to_day: День, в который необходимо переставить lesson.
        :param to_les_pos: Позиция в дне, в которую необходимо переставить lesson.
        """
        school.remove_duration(from_lesson, from_day, from_les_pos)
        from_lesson.set_available(from_day, from_les_pos)
        self._append_lesson(school, from_lesson, to_day, to_les_pos)
        return

    def dropContextMenu(self, globPoint: QPoint, position: (int, int)) -> int:
        """
        Метод выводит меню при успешном действии drop.
        """
        menu = QtWidgets.QMenu()
        menu.setWindowTitle('Несоответствия')

        conflict_action = ConflictAction(menu, self.conflicts, position[0], position[1])

        menu.addAction(conflict_action)
        cancel_action = menu.addAction('Отменить')
        throw_action = None
        if len(self.conflicts[position[0]][position[1]]) != 0:
            throw_action = menu.addAction('Выбросить несоответствия и поместить')
        place_action = menu.addAction('Игнорировать и поместить')
        action = menu.exec(globPoint)
        if action == cancel_action:
            return 0
        elif action == throw_action:
            return 1
        elif action == place_action:
            return 2
        else:
            return -1

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        """
        Метод выводит пользователю меню в зависимости от параметров ячейки.
        """
        menu = QtWidgets.QMenu()

        point = QPoint(int(a0.pos().x()), int(a0.pos().y()))
        to_index = self.indexAt(point)
        cell = self.itemAt(a0.pos())

        # Вызывается метод emptyCellMenu, если ячейка пустая, либо bookedCellMenu, если ячейка заполнена
        if cell is not None:
            if not self.bookedCellMenu(menu, to_index, a0, cell):
                return
        else:
            if not self.emptyCellMenu(menu, to_index, a0):
                return
        super(MyTableWidget, self).contextMenuEvent(a0)
        return

    def bookedCellMenu(self, menu: QtWidgets.QMenu, to_index: QtCore.QModelIndex,
                       a0: QtGui.QContextMenuEvent, cell: QtWidgets.QTableWidgetItem) -> bool:

        labelAction = BookedMenuLabelAction(menu, cell.lesson)
        menu.addAction(labelAction)
        throwAction = QtGui.QAction('Выбросить')
        menu.addAction(throwAction)

        action = menu.exec(a0.globalPos())
        if action is None or action == labelAction:
            return False

        day, les_pos = utils.column_to_days_lessons(to_index.column(), self.mainapp.school.amount_lessons)
        item = self.takeItem(to_index.row(), to_index.column())
        self._throw_lesson(self.mainapp.school, item.lesson, day, les_pos)
        return True

    def emptyCellMenu(self, menu: QtWidgets.QMenu, to_index: QtCore.QModelIndex,
                      a0: QtGui.QContextMenuEvent) -> bool:
        day, les_pos = utils.column_to_days_lessons(to_index.column(), self.mainapp.school.amount_lessons)
        av_items = self.unallocated_list.get_available_items(to_index.row(), day, les_pos)
        if len(av_items) == 0:
            return False

        labelAction = EmptyMenuLabelAction(menu, self.mainapp.school.student_classes[to_index.row()])
        menu.addAction(labelAction)
        actions = []
        for item in av_items:
            message = f'{item.lesson.subject.abbreviation} ({item.lesson.student_class.abbreviation})'
            action = QtGui.QAction(f'{message}')
            action.setData(item)
            actions.append(action)
        menu.addActions(actions)

        action = menu.exec(a0.globalPos())
        if action is None or action == labelAction:
            return False

        item = action.data()
        item = self.unallocated_list.takeItem(self.unallocated_list.row(item))
        from_lesson = item.lesson
        self.setItem(to_index.row(), to_index.column(), TimeTableItem(from_lesson))
        self._append_lesson(self.mainapp.school, from_lesson, day, les_pos)
        return True
