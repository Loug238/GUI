import sys
import inspect
from cProfile import label

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QScrollArea,
    QTextEdit,
    QComboBox,
    QLabel,
    QToolBar,
    QMainWindow,
    QStatusBar,
    QFormLayout,
    QMenu,
    QGridLayout,
    QListWidgetItem
)

import Activities_list
import styles
from PyQt5.QtCore import Qt, pyqtSignal, QSize

# from Activities_list import activities_list
from DataTableLib import *
from EmailLib import *
from MessengerLib import *
from RDPLib import *


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(styles.rarus_style_sheet) # Задается стиль

        # Настройки всплывающего окна
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 1200, 800)

        # Создание центрального виджета
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #2e329e;")
        self.setCentralWidget(central_widget)

        # Основной макет
        self.main_layout = QHBoxLayout(central_widget)

        # Инициализация частей интерфейса
        self.init_tools_panel()
        self.init_left_part()
        self.init_central_part()
        self.init_right_part()
        self.init_status_bar()

        self.list_elements = []  # Список элементов в центральной области

    def init_left_part(self):
        """Инициализация левой части интерфейса"""
        # Создание левой области
        left_part = QWidget()
        left_part.setMaximumWidth(350)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Создание верхнего виджета для поля поиска
        upper_widget = QWidget()
        upper_widget.setMinimumHeight(60)
        upper_widget.setMaximumHeight(60)
        upper_widget.setStyleSheet("background-color: #aec9ff; border-top-left-radius: 30px; border-top-right-radius: 30px;")

        # Поле поиска
        self.search_box = QLineEdit()
        self.search_box.setMinimumHeight(30)
        self.search_box.setMaximumHeight(30)
        self.search_box.setPlaceholderText("Поиск активностей")
        self.search_box.setStyleSheet("background-color: white; border-radius: 11px;")
        self.search_box.textChanged.connect(
            self.filter_activities)  # Подключение сигнала изменения текста к фильтрации

        # Добавление поля поиска в верхнюю часть
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(self.search_box)
        upper_widget.setLayout(upper_layout)

        # Создание области прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: white; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )  # Вертикальная полоса прокрутки всегда видимая (временно)

        # Создание виджета для кнопок
        button_widget = QWidget()
        button_layout = QVBoxLayout()

        button_layout.setContentsMargins(11, 11, 11, 11)  # Убирает отступы вокруг макета

        # Создание кнопок-папок
        self.create_activity_button(button_layout, "Таблица", [
            "Получить значение из таблицы", "Заменить значение из таблицы",
            "Добавить столбец к таблице", "Добавить строчку к таблице",
            "Удалить все строчки из таблицы", "Удалить строку из таблицы",
            "Удалить столбец из таблицы", "Отсортировать таблицу по столбцу",
            "Соединить таблицы", "Найти строки по SQL-запросу",
            "Проверить существование значения", "Найти строку"
        ])

        self.create_activity_button(button_layout, "Почта", [
            "Выгрузить сообщение из почты", "Вывести письма в консоль",
            "Вывести письма в файл", "Отправить письмо",
            "Перенести письма в папку на почте"
        ])

        self.create_activity_button(button_layout, "Telegram", [
            "Отправить контакт в чат", "Скачать файл из чата",
            "Отправить файл в чат", "Отправить сообщение в чат",
            "Отправить фото в чат"
        ])

        self.create_activity_button(button_layout, "RDP", [
            "Кликнуть по элементу", "Проверить существование элемента",
            "Ввести текст в элемент", "Поиск элемента",
            "Считать текст из элемента", "Ожидать появление/сокрытие элемента",
            "Кликнуть по изображению", "Кликнуть по тексту на экране"
        ])

        # Добавление виджета кнопок в область прокрутки
        button_widget.setLayout(button_layout)
        self.scroll_area.setWidget(button_widget)

        # Сборка левой области
        left_layout.addWidget(upper_widget)
        left_layout.addWidget(self.scroll_area)
        left_part.setLayout(left_layout)

        self.main_layout.addWidget(left_part)

        # Добавление разделителя
        self.addSeparator()
        button_layout.addStretch()

    def create_activity_button(self, layout, title, activities):
        """Создание кнопки и списка активностей"""
        button = QPushButton(title)

        list_widget = QListWidget()

        for activity in activities:
            item = QListWidgetItem(activity)
            item.setText(activity)
            list_widget.addItem(item)

            # Добавляем разделитель между элементами списка
            separator_item = QListWidgetItem()
            separator_item.setFlags(Qt.NoItemFlags)  # Отключение возможности взаимодействия с разделителем
            separator_item.setSizeHint(QSize(0, 1))  # Высота разделителя
            list_widget.addItem(separator_item)

            list_widget.setItemWidget(separator_item, QWidget())  # Добавление пустого виджета для разделителя

        # Обработка двойного клика
        list_widget.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        list_widget.setVisible(False)

        button.clicked.connect(lambda: self.toggle_list(list_widget))

        layout.addWidget(button)
        layout.addWidget(list_widget)

    def filter_activities(self):
        """Фильтр активностей по введенному тексту"""
        search_term = self.search_box.text().lower()  # Получение текста из поля поиска и приведение к нижнему регистру

        # Поиск кнопок
        for button in self.findChildren(QPushButton):
            list_widget = button.nextInFocusChain()
            if isinstance(list_widget, QListWidget):
                match_found = False  # Переменная для отслеживания наличия совпадений

                for i in range(list_widget.count()):
                    item = list_widget.item(i)
                    if search_term in item.text().lower():  # Проверка наличия совпадения
                        match_found = True
                        item.setHidden(False)  # Отображение элемента, если он соответствует запросу
                    else:
                        item.setHidden(True)  # Сокрытие элемента, если он не соответствует запросу

                if match_found:
                    list_widget.show()  # Отображение списка, если есть совпадения
                else:
                    list_widget.hide()  # Сокрытие списка, если нет совпадений

        # Если строка поиска пустая, все списки активностей скрываются
        if not search_term:
            for button in self.findChildren(QPushButton):
                list_widget = button.nextInFocusChain()
                if isinstance(list_widget, QListWidget):
                    list_widget.hide()

    def toggle_list(self, list_widget):
        """Переключение видимости списка"""
        current_visibility = list_widget.isVisible()
        list_widget.setVisible(not current_visibility)

    def init_central_part(self):
        """Инициализация центральной части интерфейса"""
        # Создание центральной области
        central_part = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Создание верхнего виджета для заголовка области
        upper_widget = QWidget()
        upper_widget.setMinimumHeight(60)
        upper_widget.setMaximumHeight(60)
        upper_widget.setStyleSheet(
            "background-color: #aec9ff; border-top-left-radius: 30px; border-top-right-radius: 30px;")

        # Заголовок области
        label_string = QLabel("Выбранные активности")
        label_string.setMinimumHeight(30)
        label_string.setMaximumHeight(30)
        label_string.setAlignment(Qt.AlignCenter)
        label_string.setStyleSheet("background-color: white; border-radius: 11px;")

        # Добавление заголовка в верхнюю часть
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(label_string)
        upper_widget.setLayout(upper_layout)

        # Создание области отображения выбранных активностей
        self.central_scroll_area = QScrollArea()
        self.central_scroll_area.setWidgetResizable(True)
        self.central_scroll_area.setStyleSheet(
            "background-color: white; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)  # Убирает отступы вокруг макета
        self.central_layout.setSpacing(0)  # Убирает промежутки между элементами

        self.central_scroll_area.setWidget(self.central_widget)

        # Сборка центральной области
        central_layout.addWidget(upper_widget)
        central_layout.addWidget(self.central_scroll_area)
        central_part.setLayout(central_layout)

        self.main_layout.addWidget(central_part)

    def add_element_to_central(self, item):
        """Добавление элемента в центральную часть"""
        # Создание нового элемента
        element_name = item.text()
        element_function = Activities_list.activities_list.get(element_name, None)
        element_arguments = []

        if not element_function:
            self.status_bar.showMessage(f"Функция для '{element_name}' не найдена.")
            return
        else:
            self.status_bar.showMessage(
                f"Функция для '{element_name}' найдена: {element_function}."
            )

        # Создаём элемент и подключаем его сигнал
        new_element = Element(
            len(self.list_elements), element_name, element_function, element_arguments
        )
        new_element.clicked.connect(self.update_right_part)
        self.list_elements.append(new_element)

        # Используем QPushButton вместо QLabel
        element_widget = QPushButton(element_name)
        element_widget.clicked.connect(
            lambda: new_element.clicked.emit(element_function)
        )

        # Контекстное меню для кнопки
        element_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        element_widget.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, new_element, element_widget)
        )

        self.central_layout.addWidget(element_widget)

    def show_context_menu(self, pos, element, widget):
        """Появление контекстного меню для блоков в центральной области"""
        context_menu = QMenu(self)

        delete_action = context_menu.addAction("Удалить")

        action = context_menu.exec_(widget.mapToGlobal(pos))

        if action == delete_action:
            # Удаляем элемент из списка и виджета
            if element in self.list_elements:
                self.list_elements.remove(element)
                widget.deleteLater()  # Удаление виджета из центральной части

    def init_right_part(self):
        """Инициализация правой части интерфейса"""
        # Создание правой области
        right_part = QWidget()
        right_part.setMaximumWidth(350)
        right_part.setMinimumWidth(350)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Создание верхнего виджета для заголовка области
        upper_widget = QWidget()
        upper_widget.setMinimumHeight(60)
        upper_widget.setMaximumHeight(60)
        upper_widget.setStyleSheet(
            "background-color: #aec9ff; border-top-left-radius: 30px; border-top-right-radius: 30px;")

        # Заголовок области
        label_string = QLabel("Информация об активности")
        label_string.setMinimumHeight(30)
        label_string.setMaximumHeight(30)
        label_string.setAlignment(Qt.AlignCenter)
        label_string.setStyleSheet("background-color: white; border-radius: 11px;")

        # Добавление заголовка в верхнюю часть
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(label_string)
        upper_widget.setLayout(upper_layout)

        # Создание области информации об активности
        self.form_widget = QWidget()
        self.form_widget.setStyleSheet("background-color: white; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")
        self.form_layout = QFormLayout(self.form_widget)

        # Добавление метки с описанием
        self.info_label = QLabel(
            "Здесь будет отображаться информация о выбранной активности."
        )
        self.info_label.setWordWrap(True)
        self.form_layout.addRow(self.info_label)

        # Установка минимального размера для правой части
        self.form_widget.setMinimumWidth(250)
        self.form_widget.setMaximumWidth(400)

        # Сборка правой области
        right_layout.addWidget(upper_widget)
        right_layout.addWidget(self.form_widget)
        right_part.setLayout(right_layout)

        # Добавление разделителя
        self.addSeparator()
        self.main_layout.addLayout(right_layout)

        self.main_layout.addWidget(right_part)

    def addSeparator(self):
        """Добавление разделителя между рабочими зонами."""
        separator = QWidget()
        separator.setFixedWidth(6)
        separator.setStyleSheet(
            "background-color: #fca115; border-radius: 3px;"
        )
        self.main_layout.addWidget(separator)

    def init_tools_panel(self):
        """Инициализация панели инструментов"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setStyleSheet("background-color: #aec9ff;")
        self.addToolBar(toolbar)

        button_action = QPushButton("Пример кнопки")
        button_action.setFixedSize(160, 40)
        button_action.setStyleSheet("margin: 5px; background-color: white; border-radius: 7px;")
        button_action.clicked.connect(self.example_action)
        toolbar.addWidget(button_action)

        # Добавление разделителя
        separator1 = QWidget()
        separator1.setFixedWidth(3)
        separator1.setStyleSheet(
            "background-color: #fca115; border-radius: 1px;")
        toolbar.addWidget(separator1)

        # Кнопка отображения переменных
        button_variables = QPushButton("Отображение переменных")
        button_variables.setFixedSize(250, 40)
        button_variables.setStyleSheet("margin: 5px; background-color: white; border-radius: 7px;")
        # button_variables.cliked.connect()
        toolbar.addWidget(button_variables)

        # Добавление разделителя
        separator2 = QWidget()
        separator2.setFixedWidth(3)
        separator2.setStyleSheet(
            "background-color: #fca115; border-radius: 1px;")
        toolbar.addWidget(separator2)

        # Кнопка отображения информации об активностях
        button_right_part = QPushButton("Отображение правой части")
        button_right_part.setFixedSize(250, 40)
        button_right_part.setStyleSheet("margin: 5px; background-color: white; border-radius: 7px;")
        # button_right_part.clicked.connect()
        toolbar.addWidget(button_right_part)

    def init_status_bar(self):
        """Инициализация статус-бара"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def example_action(self):
        """Пример действия для кнопки на панели инструментов"""
        self.status_bar.showMessage("Кнопка на панели инструментов нажата!")

    def update_right_part(self, func):
        if not func:
            self.status_bar.showMessage("Функция не задана для данного элемента")
            return

        signature = inspect.signature(func)

        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for name, param in signature.parameters.items():
            label = QLabel(name)
            input_field = QLineEdit()
            self.form_layout.addRow(label, input_field)


class Element(QWidget):
    clicked = pyqtSignal(object)  # Определение сигнала, который принимает один объект

    def __init__(self, element_id, name, function, arguments):
        super().__init__()
        self.id = element_id
        self.name = name
        self.function = function
        self.arguments = arguments

    def mousePressEvent(self, event):
        """Обработка клика на элемент"""
        # Испускание сигнала, передаваемого self.function
        self.clicked.emit(self.function)

    def perform(self):
        return self.function(*self.arguments)

# Класс для блоков в центральной области
# class DraggableButton(QPushButton):
#     def __init__(self, text):
#         super().__init__(text)
#         self.setAcceptDrops(True)
#         self.dragging = False
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.dragging = True
#             self.startPos = event.pos()
#
#     def mouseMoveEvent(self, event):
#         if self.dragging:
#             if (event.pos() - self.startPos).manhattanLength() > QApplication.startDragDistance():
#                 self.move(event.globalPos() - self.rect().center())
#
#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.dragging = False

