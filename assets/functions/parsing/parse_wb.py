from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time


def parse_wb(browser):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru

    Args:
        browser (selenium.webdriver): chromedriver
    """
    browser.implicitly_wait(1)

    price = browser.find_element(
        By.CLASS_NAME, "price-block__final-price").text

    try:
        brand_name = browser.find_element(
            By.CLASS_NAME, "product-page__header")

        brand = brand_name.find_element(
            By.TAG_NAME, 'a').text

        name = brand_name.find_element(
            By.TAG_NAME, 'h1').text

    except NoSuchElementException:
        brand = "Неизвестно"
        name = "Неизвестно"

    try:
        old_price_elem = browser.find_element(
            By.CLASS_NAME, "price-block__old-price")
        old_price = old_price_elem.text

        time.sleep(1)

        ActionChains(browser)\
            .scroll_to_element(browser.find_element(
                By.CLASS_NAME, "details-section__header"))\
            .perform()

        time.sleep(1)

        ActionChains(browser)\
            .click(old_price_elem)\
            .perform()

        time.sleep(1)

        data = browser.find_elements(
            By.CLASS_NAME, "discount-tooltipster-content")

        if not data:
            discount = False

        else:
            discs = {item.find_element(By.TAG_NAME, "span").text[:-1]:
                     item.find_elements(By.TAG_NAME, "span")[-1].text[:-1]
                     for item in data[0].find_elements(
                By.TAG_NAME, "p")[1:]}
            # all_discs = data[0].find_elements(
            #     By.TAG_NAME, "p")[1:]

            # if len(all_discs) == 2:

            # else:
            #     # ищем последний <p> и оттуда извлекаем
            #     # первый span
            #     discount = all_discs[-1].find_elements(
            #         By.TAG_NAME, "span")[0].text[:-1]

        price = int(''.join(price.split()[:-1]))
        old_price = int(''.join(old_price.split()[:-1]))

    except NoSuchElementException:
        old_price = False
        discount = False

    return [brand, name, discs, old_price]
