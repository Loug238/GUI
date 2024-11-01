import imaplib
import email
import datetime
import os.path
import email.mime.application
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def receive_emails(imap_server, email_account, app_password, seen="ALL", count=None, start_date=None, end_date=None, read=0, rev=False, delete_after_fetch=False, folder="INBOX"):
    """
    Функция выгрузки сообщений из почты
    :param imap_server: сервер почты
    :param email_account: аккаунт почты
    :param app_password: пароль аккаунта почты
    :param seen: критерий поиска писем ("ALL" - все, "UNSEEN" - непрочитанные, "SEEN" - прочитанные)
    :param count: ограничение по количеству вывода сообщений
    :param start_date: критерий поиска писем по дате (начальная дата) [DD.Mon.YYYY]
    :param end_date: критерий поиска писем по дате (конечная дата) [DD.Mon.YYYY]
    :param read: параметр чтения писем (0 - не читать письмо после выгрузки, 1 - читать письмо после выгрузки)
    :param rev: параметр сортировки выгружаемых писем (False - от нового к старому, True - наоборот)
    :param delete_after_fetch: параметр удаления писем из почты после выгрузки (False - отсутствие удаления, True - удаление)
    :param folder: папка с письмами ("INBOX" - Входящие, "Sent" - Отправленные, "Drafts" - Черновики, "Spam" - Спам, "Trash" - Корзина, собственные папки на английском)
    :return: список писем class 'bytes'
    """
    try:
        # Подключение к серверу и вход в аккаунт
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_account, app_password)

        # Выбор папки "INBOX"
        imap.select(folder)

        # Определение критерия поиска
        criteria = []
        if start_date:
            criteria.append(f"SINCE {start_date}")
        if end_date:
            criteria.append(f"BEFORE {end_date}")
        if seen == "UNSEEN":
            criteria.append("UNSEEN")
        if seen == "SEEN":
            criteria.append("SEEN")

        query = " ".join(criteria) if criteria else "ALL"

        # Поиск писем по критериям
        status, data = imap.search(None, query)

        # Преобразование списка ID сообщений
        email_ids = data[0].split()

        # Ограничение количества выгружаемых писем
        if count and len(email_ids) > count:
            email_ids = email_ids[:count]

        emails = []

        for email_id in email_ids:
            # Получение сообщения по ID
            if read == 0:
                status, msg_data = imap.fetch(email_id, "(BODY.PEEK[])")
            else:
                status, msg_data = imap.fetch(email_id, "(RFC822)")

            # Получение содержимого сообщения
            raw_msg = msg_data[0][1]
            emails.append(raw_msg)

            # Отметка сообщений, которые нужно удалить
            if delete_after_fetch:
                imap.store(email_id, "+FLAGS", "\\Deleted")

        # Удаление писем
        if delete_after_fetch:
            imap.expunge()

        # Сортировка писем
        emails.sort(reverse=rev) # False - от нового к старому, True - наоборот

    finally:
        # Завершение сессии
        imap.logout()

        # возврат писем
        return emails


def print_emails(emails):
    """
    Функция вывода писем в консоль
    :param emails: выгруженные письма
    :return: выводит в консоль сервер, аккаунт, тему письма, дату получения, ID письма, Email отправителя, текст письма
    """
    msgs = []
    for raw_email in emails:
        data = email.message_from_bytes(raw_email)
        msgs.append(data)
    # Вывод информации о сервере и аккаунте
    for msg in msgs:

        # Декодирование заголовка
        subject, encoding = decode_header(msg["Subject"])[0]

        # Проверка типа заголовков
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Получение даты получения, ID письма, Email отправителя
        letter_date = datetime.datetime(*(email.utils.parsedate_tz(msg["Date"]))[0:6])
        letter_id = msg["Message-ID"]
        letter_from = msg["Return-path"]
        print("________________________________________________")
        print("Тема:", subject)
        print("Дата получения:", letter_date)
        print("ID письма:", letter_id)
        print("Email отправителя:", letter_from)

        # Получение текста сообщений
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Текст сообщения:", body)
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            print("Текст сообщения:", body)


def email_to_eml(email, path, file_name):
    """
    Функция вывода писем в создаваемый файл
    :param email: письмо
    :param path: путь к папке, в которой необходимо создать файл письма
    :param file_name: название файла для сохранения письма
    :return: создается файл с письмом
    """
    file_name = os.path.join(path, file_name + ".eml")
    f = open(file_name, "wb")
    f.write(email)
    f.close()


def send_email(smtp_server:str, email_account:str, app_password:str, port:int, receiver_email:str, receivers_email_copy=None, hidden_receivers=None, email_subject="", email_body="", attachment=None, msg_to_forward=None):
    """
    Функция отправки сообщения
    :param smtp_server: сервер почты
    :param email_account: аккаунт почты
    :param app_password: пароль аккаунта почты
    :param port: порт
    :param receiver_email: получатель сообщения
    :param receivers_email_copy: список получателей копии письма ["example1@ex.com", "ex2@ex.com", ...]
    :param hidden_receivers: список скрытых получателей письма ["example1@ex.com", "ex2@ex.com", ...]
    :param email_subject: тема письма
    :param email_body: тело письма
    :param attachment: вложение к письму
    :param msg_to_forward: письмо для пересылки
    :return: возвращает состояние отправки письма и ошибку, в случае ее возникновения
    """
    try:
        # Подключение к серверу и вход в аккаунт
        smtp = smtplib.SMTP_SSL(smtp_server, port)
        smtp.login(email_account, app_password)

        # Создание письма
        msg = MIMEMultipart()
        msg["From"] = email_account
        msg["To"] = receiver_email

        if receivers_email_copy:
            msg["Cc"] = ", ".join(receivers_email_copy) # добавляет получателей копии при наличии
        msg["Subject"] = email_subject

        # Пересылаемое письмо
        if msg_to_forward:
            for msgtf in msg_to_forward:
                data = email.message_from_bytes(msgtf)

                # Получение данных о пересылаемом сообщении
                dsubject, encoding = decode_header(data["Subject"])[0]
                if isinstance(dsubject, bytes):
                    dsubject = dsubject.decode(encoding if encoding else "utf-8")
                dfrom = data["Return-path"]
                dto = data["To"]
                ddate = data["Date"]

                fbody = (f"\n\n--- Пересланное сообщение ---\n"
                         f"Тема: {dsubject}\n"
                         f"От кого: {dfrom}\n"
                         f"Кому: {dto}\n"
                         f"Дата отправки: {ddate}\n\n")

                if data.is_multipart():
                    for part in data.walk():
                        if part.get_content_type() == "text/plain":
                            fbody += part.get_payload(decode=True).decode()
                            break
                else:
                    fbody += data.get_payload(decode=True).decode()
                fbody += "\n--- Конец пересланного сообщения ---\n"
                email_body += fbody

        msg.attach(MIMEText(email_body, "plain"))

        # Добавление файла в письмо
        if attachment:
            f = open(attachment, "rb")
            att = email.mime.application.MIMEApplication(f.read())
            f.close()
            att.add_header("Content-Disposition", "attachment", filename=attachment)
            msg.attach(att)

        all_receiver_email = [receiver_email]
        if receivers_email_copy:
            all_receiver_email.extend(receivers_email_copy)
        if hidden_receivers:
            all_receiver_email.extend(hidden_receivers)

        # Отправка сообщения
        smtp.send_message(msg, to_addrs=all_receiver_email)
        print("Письмо отправлено")

    except Exception as exc:
        print(f"Не удалось отправить письмо: {exc}" )

    finally:
        smtp.quit()


def move_emails(imap_server, email_account, app_password, emails, selected_folder, delete_after_move=False):
    """
    Функция перемещения писем в папку на почте
    :param imap_server: сервер почты
    :param email_account: аккаунт почты
    :param app_password: пароль аккаунта почты
    :param emails: письма
    :param selected_folder: папка на почте, в которую необходимо перенести письма
    :param delete_after_move: параметр удаления писем из первоначальной папки после переноса (False - отсутствие удаления, True - удаление)
    :return:
    """
    try:
        # Подключение к серверу и вход в аккаунт
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_account, app_password)

        # выбор исходной папки
        imap.select('test')

        for raw_email in emails:
            # Получаем идентификатор письма
            msg = email.message_from_bytes(raw_email)
            email_id = msg["Message-ID"]
            print(email_id)

            # Поиск письма в исходной папке
            # status, data = imap.search(None, '(HEADER Message-ID "%s")' % email_id)
            status, data = imap.search(None, f'HEADER Message-ID "{email_id}')
            print(status)
            print(data)
            if status == "OK":
                email_ids = data[0].split()
                if email_ids:
                    # Перемещаем письмо в выбранную папку
                    imap.copy(email_ids[0], selected_folder)

                    # Удаляем письмо после переноса
                    if delete_after_move:
                        imap.store(email_ids[0], "+FLAGS", "\\Deleted")
                        imap.expunge()

    except Exception as exc:
        print(f"Не удалось перенести письмо: {exc}" )

    finally:
        # Завершение сессии
        imap.logout()
