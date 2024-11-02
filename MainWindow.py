import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QListWidget,
                             QLineEdit, QScrollArea, QTextEdit,
                             QComboBox, QLabel)
from PyQt5.QtCore import Qt
# from DataTableLib import *
# from EmailLib import *
# from MessengerLib import *
# from RDPLib import *

class App(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки всплывающего окна
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 900, 600)

        # Основной макет
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Инициализация частей интерфейса
        self.init_left_part()
        self.init_central_part()
        self.init_right_part()

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
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) # вертикальная полоса прокрутки всегда видимая

        # Создание виджета для кнопок
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)  # убирает отступы вокруг макета
        button_layout.setSpacing(0) # убирает промежутки между кнопками

        # Создание кнопок-папок
        self.button_DataTableLib = QPushButton("Таблица")
        self.button_DataTableLib.clicked.connect(self.toggle_DataTableLib)
        button_layout.addWidget(self.button_DataTableLib)

        # Список элементов для кнопки "Таблица"
        self.DataTableLib_list = QListWidget()
        self.DataTableLib_list.addItems([
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
            "Найти строку"
        ])
        # Изначально скрываем список активностей
        self.DataTableLib_list.setVisible(False)

        button_layout.addWidget(self.DataTableLib_list)  # Добавляем список активностей под кнопкой

        button_EmailLib = QPushButton("Почта")
        # button_EmailLib.clicked.connect()
        button_layout.addWidget(button_EmailLib)

        button_MessengerLib = QPushButton("Telegram")
        # button_MessengerLib.clicked.connect()
        button_layout.addWidget(button_MessengerLib)

        button_RDPLib = QPushButton("RDP")
        # button_RDPLib.clicked.connect()
        button_layout.addWidget(button_RDPLib)

        # Добавление виджета кнопок в область прокрутки
        self.scroll_area.setWidget(button_widget)

        # Добавление элементов в левую часть макета
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.title)
        left_layout.addWidget(self.search_box)
        left_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(left_layout)

    def toggle_DataTableLib(self):
        """Переключение видимости опций таблицы"""
        current_visibility = self.DataTableLib_list.isVisible()
        self.DataTableLib_list.setVisible(not current_visibility)

    def init_central_part(self):
        """Инициализация центральной части интерфейса"""
        self.central_scroll_area = QScrollArea()
        self.central_scroll_area.setWidgetResizable(True)

        # Добавление элементов в центральную часть макета
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)

        self.central_scroll_area.setWidget(self.central_widget)
        self.main_layout.addWidget(self.central_scroll_area)

    def init_right_part(self):
        """Инициализация правой части интерфейса"""
        self.text = QTextEdit()

        # Добавление элементов в правую часть макета
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.text)

        self.main_layout.addLayout(right_layout)


class Element(QWidget):
    def __init__(self, element_id, name, function, arguments):
        self.id = element_id
        self.name = name
        self.function = function
        self.arguments = arguments

    def execute(self):
        return self.function(*self.arguments)
list_elements = []
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