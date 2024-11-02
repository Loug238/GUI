from DataTableLib import *
from EmailLib import *
from MessengerLib import *
from RDPLib import *

activities_list = {
    "Получить значение из таблицы": get_cell_value,
    "Заменить значение из таблицы": update_cell_value,
    "Добавить столбец к таблице": add_col,
    "Добавить строчку к таблице": add_row,
    "Удалить все строчки из таблицы": clean_rows,
    "Удалить строку из таблицы": del_row,
    "Удалить столбец из таблицы": del_col,
    "Отсортировать таблицу по столбцу": sort_table,
    "Соединить таблицы": merge_tables,
    "Найти строки по SQL-запросу": find_rows_sql,
    "Проверить существование значения": check_value,
    "Найти строку": find_row,
    "Выгрузить сообщение из почты": receive_emails,
    "Вывести письма в консоль": print_emails,
    "Вывести письма в файл": email_to_eml,
    "Отправить письмо": send_email,
    "Перенести письма в папку на почте": move_emails,
    "Отправить контакт в чат": send_contact,
    "Скачать файл из чата": download_file_bot,
    "Отправить файл в чат": send_file,
    "Отправить сообщение в чат": send_msg,
    "Отправить фото в чат": send_pic,
    "Кликнуть по элементу": click_rdp_element,
    "Проверить существование элемента": check_rdp_element,
    "Ввести текст в элемент": input_text_in_rdp,
    "Поиск элемента": find_rdp_element,
    "Считать текст из элемента": get_text_from_rdp,
    "Ожидать появление/сокрытие элемента": wait_for_rdp_element,
    "Кликнуть по изображению": click_image_element,
    "Кликнуть по тексту на экране": click_text_on_screen
}