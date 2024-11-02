from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import cv2
import requests
import numpy as np
import pyautogui
import pytesseract
from PIL import ImageGrab

def click_rdp_element(driver, method, identifier, click_type='single'):
    """
    Функция имитации клика мышкой по элементу или координатам в окне RDP
    :param driver: подключение к драйверу
    :param method: метод поиска элемента ('coordinates', 'xpath', 'ui_element')
    :param identifier: идентификатор элемента (координаты, XPath или UI-элемент)
    :param click_type: тип клика ('single' или 'double')
    """
    if method == 'coordinates':
        # Разделяем координаты на x и y
        x, y = identifier
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().perform()

    elif method == 'xpath':
        # Поиск элемента по XPath
        element = driver.find_element(By.XPATH, identifier)
        if click_type == 'double':
            ActionChains(driver).double_click(element).perform()
        else:
            element.click()

    elif method == 'ui_element':
        # Поиск элемента по имени или другому свойству
        element = driver.find_element(By.NAME, identifier)
        if click_type == 'double':
            ActionChains(driver).double_click(element).perform()
        else:
            element.click()

    else:
        raise ValueError("Неправильный метод поиска. Используйте 'coordinates', 'xpath' или 'ui_element'")


def check_rdp_element(driver, xpath):
    """
    Функция проверки существования RDP-элемента
    :param driver: подключение к драйверу
    :param xpath: XPath элемента, существование которого нужно проверить
    :return: возвращает True если элемент найден, False - не найден
    """
    try:
        # Попытка найти элемент по XPath
        driver.find_element(By.XPATH, xpath)
        return True  # Элемент найден
    except NoSuchElementException:
        return False  # Элемент не найден


def input_text_in_rdp(driver, identifier, text, method='xpath'):
    """
    Функция ввода текста в RDP-элемент
    :param driver: подключение к драйверу
    :param identifier: XPath элемента или UI-элемент
    :param text: текст
    :param method: метод поиска элемента ('xpath' или 'ui_element')
    """
    if method == 'xpath':
        # Поиск элемента по XPath
        element = driver.find_element(By.XPATH, identifier)
        element.clear()
        element.send_keys(text)

    elif method == 'ui_element':
        # Поиск UI-элемента
        element = driver.find_element(By.NAME, identifier)
        element.clear()
        element.send_keys(text)

    else:
        raise ValueError("Неправильный метод поиска. Используйте 'xpath' или 'ui_element'")


def find_rdp_element(driver, xpath, option):
    """
    Функция поиска одного или всех RDP-элементов по XPath
    :param driver: подключение к драйверу
    :param xpath: XPath для поиска элемента(ов)
    :param option: опция поиска ("first" - первый элемент, "all" - все элементы)
    :return: возвращает элемент или список элементов
    """
    # Поиск первого элемента
    if option == "first":
        element = driver.find_element(By.XPATH, xpath)
        result = element if element else None

    # Поиск всех элементов
    elif option == "all":
        elements = driver.find_elements(By.XPATH, xpath)
        result = elements if elements else []
    else:
        raise ValueError("Неправильная опция. Используйте 'first' или 'all'")

    return result


def get_text_from_rdp(driver, xpath=None, ui_element=None):
    """
    Функция считывания текста из RDP-элемента
    :param driver: подключение к драйверу
    :param xpath: XPath для поиска элемента
    :param ui_element: UI-элемент
    :return: возвращает полученный текст
    """
    # Поиск элемента по XPath
    if xpath:
        element = driver.find_element(By.XPATH, xpath)
        text = element.text if element else None

    # Использование найденного ранее UI-элемента
    elif ui_element:
        text = ui_element.text if ui_element else None
    else:
        raise ValueError("Не выбран метод определения элемента. Укажите XPath или UI_element")

    return text


def wait_for_rdp_element(driver, xpath, option, timeout):
    """
    Функция ожидания появления или сокрытия RDP-элемента
    :param driver: подключение к драйверу
    :param xpath: XPath для поиска элемента
    :param option: опция ожидания ("appear" - появление элемента, "disapper" - сокрытие элемента)
    :param timeout: время ожидания в секундах
    :return:
    """
    # Ожидание появление элемента
    if option == "appear":
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        print("Элемент появился")

    # Ожидание сокрытия элемента
    elif option == "disappear":
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        print("Элемент скрылся")
    else:
        raise ValueError("Неправильная опция. Используйте 'appear' или 'disappear'")


def click_image_element(driver, image_path):
    """
    Функция клика по изображению
    :param driver: подключение к драйверу
    :param image_path: файл искомого изображения png
    :return: сообщение о нахождении или не нахождении искомого изображения
    """
    # Загрузка искомого изображения
    target_image = cv2.imread(image_path)

    # Считывание изображений
    images = driver.find_elements(By.TAG_NAME, 'img')

    for img in images:
        # Скачиваем изображение
        img_url = img.get_attribute("src")
        image = cv2.imdecode(np.asarray(bytearray(requests.get(img_url).content), dtype="uint8"), cv2.IMREAD_COLOR)

        # Сравнение изображения с искомым
        result = cv2.matchTemplate(image, target_image, cv2.TM_CCOEFF_NORMED)

        # Определение порога сравнения
        threshold = 0.8

        if np.any(result >= threshold):
            print("Изображение найдено")
            img.click()
            break
        else:
            print("Изображение не найдено")


def click_text_on_screen(target_text, lang=None):
    """
    Функция клика на текст на экране
    :param target_text: искомый текст
    :param lang: выбор языка искомого текста (по умолчанию eng)
    :return: сообщение о нахождении или не нахождении текста
    """
    # Скриншот экрана
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")

    # Распознание текста
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program files\Tesseract-OCR\tesseract.exe' # Путь к тессеракту
    recognized_text = pytesseract.image_to_data(screenshot, lang=lang, output_type=pytesseract.Output.DICT)

    for i in range(len(recognized_text['text'])):
        if target_text.lower() in recognized_text['text'][i].lower():
            # Получаем координаты текста
            x = recognized_text['left'][i] + recognized_text['width'][i] // 2
            y = recognized_text['top'][i] + recognized_text['height'][i] // 2

            # Кликаем по тексту
            pyautogui.click(x, y)
            return f"Клик по '{target_text}' на координатах: ({x}, {y})"

    return f"Текст '{target_text}' не найден"
