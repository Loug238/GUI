import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QScrollArea,
    QTextEdit,
    QLabel,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
    QToolBar,
    QStatusBar,
)

from PyQt5.QtCore import Qt


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # Настройки окна
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
        self.init_status_bar()  # Инициализация статус-бара

        # ДЛЯ ТЕСТОВ УДАЛИТЬ
        self.test_update_right_part()

    def init_left_part(self):
        """Инициализация левой части интерфейса"""
        self.title = QLabel("Активности")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск активностей")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        self.button_DataTableLib = QPushButton("Таблица")
        self.button_DataTableLib.clicked.connect(self.toggle_DataTableLib)
        button_layout.addWidget(self.button_DataTableLib)

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
        self.DataTableLib_list.setVisible(False)
        button_layout.addWidget(self.DataTableLib_list)

        button_EmailLib = QPushButton("Почта")
        button_layout.addWidget(button_EmailLib)

        button_MessengerLib = QPushButton("Telegram")
        button_layout.addWidget(button_MessengerLib)

        button_RDPLib = QPushButton("RDP")
        button_layout.addWidget(button_RDPLib)

        self.scroll_area.setWidget(button_widget)

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
        self.text = QTextEdit()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.text)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.main_layout.addWidget(central_widget)

    def init_right_part(self):
        """Инициализация правой части интерфейса"""
        self.right_scroll_area = QScrollArea()
        self.right_scroll_area.setWidgetResizable(True)

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.form_layout = QFormLayout()
        self.right_layout.addLayout(self.form_layout)

        self.right_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.right_scroll_area.setWidget(self.right_widget)
        self.main_layout.addWidget(self.right_scroll_area)

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

    def update_right_part(self, item: dict):
        """Обновляет правую часть интерфейса при выборе элемента"""
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if len(item):
            for key in item:
                label = QLabel(key)
                input_field = QLineEdit()
                self.form_layout.addRow(label, input_field)

    # ДЛЯ ТЕСТА УДАЛИТЬ
    def test_update_right_part(self):
        """Тестовый метод для имитации получения данных"""
        test_dict = {"Лексема": "", "Выражение": ""}
        self.update_right_part(test_dict)
        return test_dict


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
