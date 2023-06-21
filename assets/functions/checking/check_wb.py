from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def check_wb(article_num, browser):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru

    Args:
        article_num (str): артикул товара
    """
    browser.get(
        f"https://www.wildberries.ru/catalog/{article_num}/detail.aspx")

    try:
        # ждем, пока страница прогрузится
        price = WebDriverWait(browser, timeout=3).until(
            lambda brows: brows.find_element(By.CLASS_NAME, "price-block__final-price").text)
        # может произойти такое, что страница полностью
        # загрузилась, но когда артикул неверный
        # на странице написано о том, что
        # что то пошло не так. а ведь
        # WebDriverWait ждет появления элемента (цены)
        # на странице. поэтому после окончания таймаута
        # мы еще раз проверяем, что на странице нет того
        # самого элемента (цены)
        # price = browser.find_element(
        #     By.CLASS_NAME, "price-block__final-price").text

        price = ''.join(price.split()[:-1])

    except NoSuchElementException:
        price = False

    except TimeoutException:
        try:
            browser.find_element(
                By.CLASS_NAME, "error500__title")
            price = False

        except NoSuchElementException:
            price = "TIMEOUT"

    return price
