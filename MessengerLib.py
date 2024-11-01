import telebot
import os


def send_contact(phone_num, name, chat_id, connection, surname=None, msg_id=None):
    """
    Функция отправляет контакт в чат
    :param phone_num: номер телефона контакта
    :param name: имя контакта
    :param surname: фамилия контакта
    :param chat_id: идентификатор чата, в который отправляются данные
    :param msg_id: идентификатор сообщения, на который требуется сделать ссылку на ответ (Reply message)
    :return:
    """
    contact = telebot.types.Contact(phone_number=phone_num, first_name=name, last_name=surname)
    connection.send_contact(chat_id, contact.phone_number, contact.first_name, contact.last_name, reply_to_message_id=msg_id)


def download_file_bot(connection, file_id, path):
    """
    Функция скачивания файла бота
    :param connection: активное соединение с Telegram API
    :param file_id: идентификатор скачиваемого файла
    :param path: путь к каталогу сохранения файла
    :return: возвращает путь к скачанному файлу
    """
    # Получение информации о файле
    file_info = connection.get_file(file_id)

    # Формирование пути для скачивания файла
    file_path = file_info.file_path
    full_path = os.path.join(path, file_info.file_path.split("/")[-1])

    # Скачиваем файл
    downloaded_file = connection.download_file(file_path)

    # Сохраняем файл
    with open(full_path, "wb") as new_file:
        new_file.write(downloaded_file)

    # Возвращение пути к файлу
    return full_path


def send_file(file_path, chat_id, connection, text=None, msg_id=None):
    """
    Функция отправки файла в чат
    :param file_path: путь к отправляемому файлу
    :param text: текстовое сообщение, отправляемое вместе с файлом
    :param connection: активное соединение с Telegram
    :param chat_id: идентификатор чата, в который отправляются данные
    :param msg_id: идентификатор сообщения, на который требуется сделать ссылку в ответе (Reply message)
    :return:
    """
    with open(file_path, "rb") as file:
        connection.send_document(chat_id=chat_id, document=file, caption=text, reply_to_message_id=msg_id)


def send_msg(text, connection, chat_id, msg_id=None):
    """
    Функция отправки сообщения в чат
    :param text: текстовое сообщение для отправки в чат
    :param connection: активное соединение с Telegram
    :param chat_id: идентификатор чата, в который отправляются данные
    :param msg_id: идентификатор сообщения, на который требуется сделать ссылку в ответе(Reply message)
    :return:
    """
    connection.send_message(chat_id=chat_id, text=text, reply_to_message_id=msg_id)


def send_pic(pic_path, connection, chat_id, text=None, msg_id=None):
    """
    Функция отправки фото в чат
    :param pic_path: путь к отправляемой фотографии
    :param text: текстовое сообщение, отправляемое вместе с фото
    :param connection: активное соединение с Telegram
    :param chat_id: идентификатор чата, в который отправляются данные
    :param msg_id: идентификатор сообщения, на который требуется сделать ссылку в ответе(Reply message)
    :return:
    """
    with open(pic_path, "rb") as pic:
        connection.send_photo(chat_id=chat_id, photo=pic, caption=text, reply_to_message_id=msg_id)



