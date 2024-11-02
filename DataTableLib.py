import pandas as pd
import pandasql as psql


def get_cell_value(table, row_index, col_index):
    """
    Функция выводит значение ячейки таблицы данных по индексам строки и столбца
    :param table: таблица данных
    :param row_index: индекс строки
    :param col_index: индекс столбца
    :return: значение ячейки
    """
    # Проверка вхождения индексов в диапазоны таблицы данных
    if row_index < 0 or row_index >= table.shape[0]:
        raise IndexError("Индекс строки вне диапазоны таблицы данных")
    if col_index < 0 or col_index >= table.shape[1]:
        raise IndexError("Индекс столбца вне диапазона таблицы данных")

    # Получение значения по индексам
    value = table.iat[row_index, col_index]

    return value


def update_cell_value(table, row_index, col_index, new_value):
    """
    Функция заменяет значение ячейки по индексам в таблице данных
    :param table: таблица данных
    :param row_index: индекс строки
    :param col_index: индекс столбца
    :param new_value: новое значение ячейки
    :return: возвращает обновленную таблицу
    """
    # Проверка вхождения индексов в диапазоны таблицы данных
    if row_index < 0 or row_index >= table.shape[0]:
        raise IndexError("Индекс строки вне диапазоны таблицы данных")
    if col_index < 0 or col_index >= table.shape[1]:
        raise IndexError("Индекс столбца вне диапазона таблицы данных")

    # Получение значения по индексам
    table.iat[row_index, col_index] = new_value

    return table


def add_col(table, col_name, col_index, values=None):
    """
    Функция добавляет столбец к таблице данных по индексу
    :param table: таблица данных
    :param col_name: название нового столбца
    :param col_index: индекс столбца, куда необходимо вставить новый столбец
    :param values: значения нового столбца
    :return: таблица с добавленным столбцом
    """
    # Проверка вхождения индекса в диапазон таблицы данных
    if col_index < 0 or col_index >= table.shape[1]+1:
        raise IndexError("Индекс столбца вне диапазона таблицы данных")

    # Добавляем новый столбец в таблицу
    table.insert(col_index, col_name, values)

    return table


def add_row(table, row_index, values):
    """
    Функция добавляет строку к таблице данных по индексу
    :param table: таблица данных
    :param row_index: индекс строки, куда необходимо вставить новую строку
    :param values: значения новой строки
    :return: таблица с добавленной строкой
    """
    # Проверка вхождения индекса в диапазон таблицы данных
    if row_index < 0 or row_index >= table.shape[0] + 1:
        raise IndexError("Индекс строчки вне диапазона таблицы данных")

    # Проверка соответствия длинны списка и количества столбцов
    if len(values) != table.shape[1]:
        raise Exception("длина списка данных не соответствует количеству столбцов")

    # Добавляем новую строку и сортируем таблицу по индексу
    table.loc[row_index] = values
    table.sort_index(inplace=True)

    return table


def clean_rows(table):
    """
    Функция удаления всех строк из таблицы
    :param table: таблица данных
    :return: возвращает пустую таблицу с заголовками столбцов
    """
    # Очищаем таблицу
    table.drop(table.index, inplace=True)

    return table


def del_row(table, row_index):
    """
    Функция удаления строки по ее индексу
    :param table: таблица данных
    :param row_index: индекс строки, которую необходимо удалить
    :return: возвращает таблицу без указанной строки
    """
    # Проверка вхождения индекса в диапазон таблицы данных
    if row_index < 0 or row_index >= table.shape[0]:
        raise IndexError("Индекс строчки вне диапазона таблицы данных")

    # Удаление строки и сброс индексов
    table.drop(index=row_index, inplace=True)
    table.reset_index(drop=True, inplace=True)

    return table


def del_col(table, col_index):
    """
    Функция удаления столбца по его индексу
    :param table: таблица данных
    :param col_index: индекс столбца таблицы данных, который необходимо удалить
    :return: возвращает таблицу данных без указанного столбца
    """
    # Проверка вхождения индекса в диапазон таблицы данных
    if col_index < 0 or col_index >= table.shape[1]:
        raise IndexError("Индекс столбца вне диапазона таблицы данных")

    # Удаление столбца
    table.drop(table.columns[col_index], axis=1, inplace=True)

    return table


def sort_table(table, col_name=None, col_index=None, ascending=True):
    """
    Функция сортировки таблицы по столбцу
    :param table: таблица данных
    :param col_name: Имя столбца, по которому будет произведена сортировка. Если указан номер столбца, то данное свойство игнорируется
    :param col_index: Номер столбца, по которому будет произведена сортировка. Если указан номер столбца, то свойство Имя столбца игнорируется. Нумерация начинается с 0
    :param ascending: параметр сортировки (True - по возрастанию, False - по убыванию)
    :return: возвращает отсортированную таблицу
    """
    # Проверка наличия имени столбца
    if col_name is not None:
        if col_name not in table.columns:
            raise Exception("Указанный столбец не найден")
        sorted_table = table.sort_values(by=col_name, ascending=ascending)

    # Проверка наличия индекса столбца
    elif col_index is not None:
        if col_index < 0 or col_index >= table.shape[1]:
            raise IndexError("Индекс столбца вне диапазона таблицы данных")
        sorted_table = table.sort_values(by=table.columns[col_index], ascending=ascending)
    else:
        raise Exception("Не указан индекс или имя столбца")

    return sorted_table


def merge_tables(table1, table2, how="inner"):
    """
    Функция соединяет две таблицы в одну с указанным типом соединения
    :param table1: первая таблица
    :param table2: вторая таблица
    :param how: параметр соединения таблиц ("inner" - внутреннее, "outer" - внешнее, "left" - левое, "right" - правое)
    :return: возвращает объединенную таблицу
    """
    # Проверка корректности указания типа соединения
    valid_joins = ["inner", "outer", "left", "right"]
    if how not in valid_joins:
        raise Exception("Неверный тип соединения")

    # Соединение таблиц
    merged_table = pd.merge(table1, table2, how=how)

    return merged_table


def find_rows_sql(df, sql_filter):
    """
    Функция находит строки по SQL-запросу
    :param df: таблица данных
    :param sql_filter: SQL-запрос
    :return: возвращает строки согласно SQl-запросу
    """
    # выполнение SQL-запроса
    rows = psql.sqldf(sql_filter, locals())

    return rows


def check_value(table, value, col_index=None):
    """
    Функция проверяет существование значения
    :param table: таблица данных
    :param value: искомое значение
    :param col_index: индекс столбца, в котором будет осуществляться поиск
    :return: возвращает True, если искомое значение есть в столбце/таблице, возвращает False, если искомого значения нет
    """
    if col_index is not None:
        # Проверка вхождения индекса в диапазон таблицы данных
        if col_index < 0 or col_index >= table.shape[1]:
            raise IndexError("Индекс столбца вне диапазона таблицы данных")

        # Проверка искомого значения в указанном столбце
        return value in table.iloc[:,col_index].values
    else:
        # Проверка искомого значения по всей таблице
        return value in table.values


def find_row(table, value, col_index=None):
    """
    Функция находит по значению первую строчку, где есть это значение
    :param table: таблица данных
    :param value: искомое значение
    :param col_index: индекс столбца, в котором будет осуществляться поиск
    :return: возвращает строчку, где есть искомое значение
    """
    if col_index is not None:
        # Проверка вхождения индекса в диапазон таблицы данных
        if col_index < 0 or col_index >= table.shape[1]:
            raise IndexError("Индекс столбца вне диапазона таблицы данных")

        # Поиск строки с искомым значением в указанном столбце
        founded_row = table[table.iloc[:,col_index] == value]

    else:
        # Поиск строки по всей таблице
        founded_row = table[(table == value).any(axis=1)]

    if not founded_row.empty:
        return founded_row.iloc[0]
    else:
        return "Совпадений не найдено"

