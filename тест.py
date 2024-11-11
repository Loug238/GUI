import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QScrollArea
from PyQt5.QtGui import QColor, QPalette, QBrush, QRegion
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример интерфейса")
        self.setGeometry(100, 100, 800, 600)

        # Основной макет
        main_layout = QHBoxLayout()

        # Левая область
        left_part = QWidget()
        left_layout = QVBoxLayout()

        # Верхняя часть - голубой прямоугольник
        upper_widget = QWidget()
        upper_widget.setStyleSheet(
            "background-color: lightblue; border-top-left-radius: 20px; border-top-right-radius: 20px;")

        # Поле для поиска
        search_box = QLineEdit()
        search_box.setPlaceholderText("Поиск...")
        search_box.setStyleSheet("border-radius: 10px; padding: 10px;")

        # Добавляем поле для поиска в верхнюю часть
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(search_box)
        upper_widget.setLayout(upper_layout)






# -------------------------------------------
        # Нижняя часть - поле скроллинга
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        button_widget = QWidget()
        button_layout = QVBoxLayout()

        # Добавляем несколько текстовых полей для демонстрации скроллинга
        for i in range(20):
            text_edit = QTextEdit()
            text_edit.setPlainText(f"Текстовое поле {i + 1}")
            button_layout.addWidget(text_edit)

        button_widget.setLayout(button_layout)
        scroll_area.setWidget(button_widget)







        # ---------------------------------------------------
        # Собираем левую область
        left_layout.addWidget(upper_widget)
        left_layout.addWidget(scroll_area)
        left_part.setLayout(left_layout)

        # Правая область (пока пустая)
        right_area = QWidget()
        right_area.setStyleSheet("background-color: white;")

        # Добавляем области в основной макет
        main_layout.addWidget(left_part)
        main_layout.addWidget(right_area)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())