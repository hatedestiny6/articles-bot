from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent


def check_ozon(article_num):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на ozon.ru

    Args:
        article_num (str): артикул товара
    """
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")

    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options)
    browser.maximize_window()

    browser.get(f"https://www.ozon.ru/product/{article_num}")
    try:
        price = browser.find_element(
            By.CLASS_NAME, "kx6").text

    except NoSuchElementException:
        price = False

    browser.close()
    return price
