from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent


def parse_wb(article_num):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru

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

    browser.get(
        f"https://www.wildberries.ru/catalog/{article_num}/detail.aspx")

    # ждем, пока страница прогрузится
    # price = WebDriverWait(browser, timeout=10).until(browser.find_elements(
    #     By.CLASS_NAME, "price-block__final-price")[-1].text)

    browser.implicitly_wait(3)

    price = browser.find_elements(
        By.CLASS_NAME, "price-block__final-price")[-1].text

    try:
        brand = ' '.join(browser.find_element(
            By.PARTIAL_LINK_TEXT,
            "Все товары").text.split()[2:])

    except NoSuchElementException:
        brand = "Неизвестно"

    try:
        name = browser.find_element(
            By.CLASS_NAME, "product-page__header").find_element(
            By.TAG_NAME, 'h1').text

    except NoSuchElementException:
        name = "Неизвестно"

    try:
        old_price = browser.find_elements(
            By.CLASS_NAME, "price-block__old-price")[-1].text
        price = int(''.join(price.split()[:-1]))
        old_price = int(''.join(old_price.split()[:-1]))
        discount = int((old_price - price) / old_price * 100)

    except IndexError:
        old_price = False
        discount = False

    browser.close()
    return [brand, name, discount]
