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
    QGridLayout
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
        self.load_styles()
        # Настройки всплывающего окна
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 1200, 800)

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

        self.list_elements = []  # список элементов в центральной области

    def init_left_part(self):
        """Инициализация левой части интерфейса"""
        # Заголовок
        self.title = QLabel("Активности")

        # Поле поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск активностей")
        self.search_box.textChanged.connect(
            self.filter_activities)  # подключение сигнала изменения текста к фильтрации

        # Создание области прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn
        )  # вертикальная полоса прокрутки всегда видимая

        # Создание виджета для кнопок
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)

        # нужно сделать, чтобы все элементы были в одном подокне,
        # сейчас они размещаются отдельно, чтобы не нужно было
        # устанавливать размеры для каждого элемента отдельно
        self.title.setMinimumWidth(250)
        self.title.setMaximumWidth(400)
        self.search_box.setMinimumWidth(250)
        self.search_box.setMaximumWidth(400)
        self.scroll_area.setMinimumWidth(250)
        self.scroll_area.setMaximumWidth(400)
        button_widget.setMinimumHeight(250)
        button_widget.setMaximumWidth(400)

        button_layout.setContentsMargins(0, 0, 0, 0)  # убирает отступы вокруг макета
        button_layout.setSpacing(0)  # убирает промежутки между кнопками

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
        self.scroll_area.setWidget(button_widget)

        # Добавление элементов в левую часть макета
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.title)
        left_layout.addWidget(self.search_box)
        left_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(left_layout)
        self.addSeparator()
        button_layout.addStretch()

    def create_activity_button(self, layout, title, activities):
        """Создание кнопки и списка активностей"""
        button = QPushButton(title)

        list_widget = QListWidget()
        list_widget.addItems(activities)

        # Обработка двойного клика
        list_widget.itemDoubleClicked.connect(self.add_element_to_central)

        # Изначально скрываем список активностей
        list_widget.setVisible(False)

        button.clicked.connect(lambda: self.toggle_list(list_widget))

        layout.addWidget(button)
        layout.addWidget(list_widget)

    def filter_activities(self):
        """Фильтр активностей по введенному тексту"""
        search_term = self.search_box.text().lower()  # Получаем текст из поля поиска и приводим к нижнему регистру

        # Поиск кнопок
        for button in self.findChildren(QPushButton):
            list_widget = button.nextInFocusChain()
            if isinstance(list_widget, QListWidget):
                match_found = False  # Переменная для отслеживания наличия совпадений

                for i in range(list_widget.count()):
                    item = list_widget.item(i)
                    if search_term in item.text().lower():  # Проверяем наличие совпадения
                        match_found = True
                        item.setHidden(False)  # Показываем элемент, если он соответствует запросу
                    else:
                        item.setHidden(True)  # Скрываем элемент, если он не соответствует запросу

                if match_found:
                    list_widget.show()  # Показываем список, если есть совпадения
                else:
                    list_widget.hide()  # Скрываем список, если нет совпадений

        # Если строка поиска пустая, скрываем все списки активностей
        if not search_term:
            for button in self.findChildren(QPushButton):
                list_widget = button.nextInFocusChain()
                if isinstance(list_widget, QListWidget):
                    list_widget.hide()

    def load_styles(self):
        """Загрузка стилей из файла."""
        with open("static\\CSS\\style.css", "r") as style_file:
            self.setStyleSheet(style_file.read())

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
        self.central_layout.setContentsMargins(0, 0, 0, 0)  # # убирает отступы вокруг макета
        self.central_layout.setSpacing(0)  # убирает промежутки между элементами

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

        # Добавляем метку с описанием
        self.info_label = QLabel(
            "Здесь будет отображаться информация о выбранной активности."
        )
        self.info_label.setWordWrap(True)
        self.form_layout.addRow(self.info_label)

        # Устанавливаем минимальный размер для правой части
        self.form_widget.setMinimumWidth(250)
        self.form_widget.setMaximumWidth(400)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.form_widget)

        # Добавляем разделитель
        self.addSeparator()
        self.main_layout.addLayout(right_layout)

    def addSeparator(self):
        """Добавление разделителя между рабочими зонами."""
        separator = QWidget()
        separator.setFixedWidth(2)
        separator.setStyleSheet(
            "background-color: #cccccc;"
        )  # серый цвет для разделителя
        self.main_layout.addWidget(separator)

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

