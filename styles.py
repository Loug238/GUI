# Рарус
rarus_style_sheet = """
* {
    font-family: 'Verdana';
    font-size: 14px;
    font-weight: 900;
    color: #2e329e;
}
"""



# Темная тема
dark_style_sheet = """
* {
    font-family: 'Verdana';
    font-weight: 900;
}
QWidget {
    background-color: #2E2E2E;  /* Основной фон */
    color: #FFFFFF;              /* Цвет текста */
}

QPushButton {
    background-color: #3E3E3E;  /* Фон кнопок */
    color: #FFFFFF;              /* Цвет текста на кнопках */
    border: 1px solid #4E4E4E;  /* Рамка кнопок */
    padding: 5px;                /* Отступы внутри кнопок */
    border-radius: 7px;         /* Скругленные углы кнопок*/
}

QPushButton:hover {
    background-color: #5E5E5E;   /* Фон кнопок при наведении */
}

QLineEdit {
    background-color: #3E3E3E;   /* Фон поля ввода */
    color: #FFFFFF;               /* Цвет текста в поле ввода */
    border: 1px solid #4E4E4E;   /* Рамка поля ввода */
    border-radius: 7px;          /* Скругленные углы строки поиска*/
}

QListWidget {
    background-color: #3E3E3E;   /* Фон списка */
    color: #FFFFFF;               /* Цвет текста в списке */
}

QScrollBar:vertical {
    background: #2E2E2E;          /* Фон вертикального скроллбара */
    width: 10px;                  /* Ширина скроллбара */
}

QScrollBar::handle:vertical {
    background: #4E4E4E;          /* Фон ползунка скроллбара */
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;             /* Убираем фон для стрелок скроллбара */
}

QStatusBar {
    background-color: #3E3E3E;   /* Фон статус-бара */
    color: #FFFFFF;               /* Цвет текста в статус-баре */
}

QLabel {
    color: #FFFFFF;               /* Цвет текста меток */
}
"""

# Светлая тема
light_style_sheet = """
* {
    font-family: 'Verdana';
    font-weight: 900;
}
QWidget {
    background-color: #FFFFFF;  /* Основной фон */
    color: #000000;              /* Цвет текста */
}

QPushButton {
    background-color: #E0E0E0;  /* Фон кнопок */
    color: #000000;              /* Цвет текста на кнопках */
    border: 1px solid #B0B0B0;  /* Рамка кнопок */
    padding: 5px;                /* Отступы внутри кнопок */
    border-radius: 7px;         /* Скругленные углы кнопок*/
}

QPushButton:hover {
    background-color: #D0D0D0;   /* Фон кнопок при наведении */
}

QLineEdit {
    background-color: #FFFFFF;   /* Фон поля ввода */
    color: #000000;               /* Цвет текста в поле ввода */
    border: 1px solid #B0B0B0;   /* Рамка поля ввода */
    border-radius: 7px;          /* Скругленные углы строки поиска*/
}

QListWidget {
    background-color: #FFFFFF;   /* Фон списка */
    color: #000000;               /* Цвет текста в списке */
}

QListWidget::item {
    border-bottom: 1px solid #E0E0E0;  /* Разделитель между элементами списка */
}

QScrollBar:vertical {
    background: #F5F5F5;          /* Фон вертикального скроллбара */
    width: 10px;                  /* Ширина скроллбара */
}

QScrollBar::handle:vertical {
    background: #B0B0B0;          /* Фон ползунка скроллбара */
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;             /* Убираем фон для стрелок скроллбара */
}

QStatusBar {
    background-color: #F5F5F5;   /* Фон статус-бара */
    color: #000000;               /* Цвет текста в статус-баре */
}

QLabel {
    color: #000000;               /* Цвет текста меток */
}
"""

