import sys
import inspect
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
)

import Activities_list

from PyQt5.QtCore import Qt, pyqtSignal

# from Activities_list import activities_list
from DataTableLib import *
from EmailLib import *
from MessengerLib import *
from RDPLib import *


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройки всплывающего окна
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 900, 600)

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        self.main_layout = QHBoxLayout(central_widget)

        # Инициализация частей интерфейса
        self.init_tools_panel()
        self.init_left_part()
        self.init_central_part()
        self.init_right_part()
        self.init_status_bar()

        # self.test_update_right_part()

        self.list_elements = []  # список элементов в центральной области

    def init_left_part(self):
        """Инициализация левой части интерфейса"""
        # Заголовок
        self.title = QLabel("Активности")

        # Поле поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск активностей")

        # Создание области прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn
        )  # вертикальная полоса прокрутки всегда видимая

        # Создание виджета для кнопок
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)  # убирает отступы вокруг макета
        button_layout.setSpacing(0)  # убирает промежутки между кнопками

        # Создание кнопок-папок
        self.button_DataTableLib = QPushButton("Таблица")
        self.button_DataTableLib.clicked.connect(
            lambda: self.toggle_list(self.DataTableLib_list)
        )
        button_layout.addWidget(self.button_DataTableLib)

        # Список элементов для кнопки "Таблица"
        self.DataTableLib_list = QListWidget()
        self.DataTableLib_list.addItems(
            [
                "Получить значение из таблицы",
                "Заменить значение из таблицы",
                "Добавить столбец к таблице",
                "Добавить строчку к таблице",
                "Удалить все строчки из таблицы",
                "Удалить строку из таблицы",
                "Удалить столбец из таблицы",
                "Отсортировать таблицу по столбцу",
                "Соединить таблицы",
                "Найти строки по SQL-запросу",
                "Проверить существование значения",
                "Найти строку",
            ]
        )

        # Обработка двойного клика
        self.DataTableLib_list.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        self.DataTableLib_list.setVisible(False)

        # Добавляем список активностей под кнопкой
        button_layout.addWidget(self.DataTableLib_list)

        button_EmailLib = QPushButton("Почта")
        button_EmailLib.clicked.connect(lambda: self.toggle_list(self.EmailLib_list))
        button_layout.addWidget(button_EmailLib)

        # Список элементов для кнопки "Почта"
        self.EmailLib_list = QListWidget()
        self.EmailLib_list.addItems(
            [
                "Выгрузить сообщение из почты",
                "Вывести письма в консоль",
                "Вывести письма в файл",
                "Отправить письмо",
                "Перенести письма в папку на почте",
            ]
        )
        # Обработка двойного клика
        self.EmailLib_list.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        self.EmailLib_list.setVisible(False)

        # Добавляем список активностей под кнопкой
        button_layout.addWidget(self.EmailLib_list)

        button_MessengerLib = QPushButton("Telegram")
        button_MessengerLib.clicked.connect(
            lambda: self.toggle_list(self.MessengerLib_list)
        )
        button_layout.addWidget(button_MessengerLib)

        # Список элементов для кнопки "Telegram"
        self.MessengerLib_list = QListWidget()
        self.MessengerLib_list.addItems(
            [
                "Отправить контакт в чат",
                "Скачать файл из чата",
                "Отправить файл в чат",
                "Отправить сообщение в чат",
                "Отправить фото в чат",
            ]
        )
        # Обработка двойного клика
        self.MessengerLib_list.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        self.MessengerLib_list.setVisible(False)

        # Добавляем список активностей под кнопкой
        button_layout.addWidget(self.MessengerLib_list)

        button_RDPLib = QPushButton("RDP")
        button_RDPLib.clicked.connect(lambda: self.toggle_list(self.RDPLib_list))
        button_layout.addWidget(button_RDPLib)

        # Список элементов для кнопки "RDP"
        self.RDPLib_list = QListWidget()
        self.RDPLib_list.addItems(
            [
                "Кликнуть по элементу",
                "Проверить существование элемента",
                "Ввести текст в элемент",
                "Поиск элемента",
                "Считать текст из элемента",
                "Ожидать появление/сокрытие элемента",
                "Кликнуть по изображению",
                "Кликнуть по тексту на экране",
            ]
        )
        # Обработка двойного клика
        self.RDPLib_list.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        self.RDPLib_list.setVisible(False)

        # Добавляем список активностей под кнопкой
        button_layout.addWidget(self.RDPLib_list)

        # Добавление виджета кнопок в область прокрутки
        self.scroll_area.setWidget(button_widget)

        # Добавление элементов в левую часть макета
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.title)
        left_layout.addWidget(self.search_box)
        left_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(left_layout)

    # def toggle_DataTableLib(self):
    #     """Переключение видимости опций таблицы"""
    #     current_visibility = self.DataTableLib_list.isVisible()
    #     self.DataTableLib_list.setVisible(not current_visibility)

    def toggle_list(self, list_widget):
        """Переключение видимости списка"""
        current_visibility = list_widget.isVisible()
        list_widget.setVisible(not current_visibility)

    def init_central_part(self):
        """Инициализация центральной части интерфейса"""
        self.central_scroll_area = QScrollArea()
        self.central_scroll_area.setWidgetResizable(True)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)

        self.central_scroll_area.setWidget(self.central_widget)
        self.main_layout.addWidget(self.central_scroll_area)

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
                widget.deleteLater()  # Удаляем виджет из центральной части

    def init_right_part(self):
        """Инициализация правой части интерфейса"""
        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)

        # Добавление элементов в правую часть макета
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.form_widget)  # Добавляем виджет с формой

        self.main_layout.addLayout(right_layout)

    def init_tools_panel(self):
        """Инициализация панели инструментов"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        button_action = QPushButton("Пример кнопки")
        button_action.clicked.connect(self.example_action)
        toolbar.addWidget(button_action)

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
        else:
            self.status_bar.showMessage("Свойства загружены")
        signature = inspect.signature(func)

        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for name, param in signature.parameters.items():
            label = QLabel(name)
            input_field = QLineEdit()
            self.form_layout.addRow(label, input_field)

    def test_update_right_part(self):
        """Тестовый метод для имитации получения данных"""
        # test_dict = {"Лексема": "", "Выражение": ""}

        def foo(name: str, age: int):
            print(f"name: {name}")

        self.update_right_part(foo)
        # return test_dict


class Element(QWidget):
    clicked = pyqtSignal(object)  # определяем сигнал, который принимает один объект

    def __init__(self, element_id, name, function, arguments):
        super().__init__()
        self.id = element_id
        self.name = name
        self.function = function
        self.arguments = arguments

    def mousePressEvent(self, event):
        """Обработка клика на элемент"""
        # Испускаем сигнал, передавая self.function
        self.clicked.emit(self.function)

    def perform(self):
        return self.function(*self.arguments)


"""
DataTableLib: 
["Получить значение из таблицы", "Заменить значение из таблицы", 
"Добавить столбец к таблице", "Добавить строчку к таблице", "Удалить все строчки из таблицы", 
"Удалить строку из таблицы", Удалить столбец из таблицы, "Отсортировать таблицу по столбцу",
"Соединить таблицы", "Найти строки по SQL-запросу", "Проверить существование значения", "Найти строку"]

EmailLib:
["Выгрузить сообщение из почты", "Вывести письма в консоль", "Вывести письма в файл", 
"Отправить письмо", "Перенести письма в папку на почте"]

MessengerLib:
["Отправить контакт в чат", "Скачать файл из чата", "Отправить файл в чат",
"Отправить сообщение в чат", "Отправить фото в чат"]

RDPLib:
["Кликнуть по элементу", "Проверить существование элемента", "Ввести текст в элемент", 
"Поиск элемента", "Считать текст из элемента", "Ожидать появление/сокрытие элемента", 
"Кликнуть по изображению", "Кликнуть по тексту на экране"]
"""
