import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QListWidget,
                             QLineEdit, QScrollArea, QTextEdit,
                             QComboBox)


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки всплывающего окна
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 1200, 800)

        # Основной макет
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Инициализация частей интерфейса
        self.init_left_part()
        self.init_central_part()
        self.init_right_part()

    def init_left_part(self):
        """Инициализация левой части интерфейса"""
        # Поле поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск")

        # Создание области прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Создание кнопки
        button = QPushButton("тестовая кнопка")
        # button.clicked.connect()

        # Добавление кнопки в область прокрутки
        self.scroll_area.setWidget(button)

        # Добавление элементов в левую часть макета
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.search_box)
        left_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(left_layout)

    def init_central_part(self):
        """Инициализация центральной части интерфейса"""
        self.text = QTextEdit()
        # Добавление элементов в правую часть макета
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.text)

        self.main_layout.addLayout(central_layout)

    def init_right_part(self):
        """Инициализация правой части интерфейса"""
        self.text = QTextEdit()
        # Добавление элементов в правую часть макета
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.text)

        self.main_layout.addLayout(right_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())


