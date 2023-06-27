def parse_ozon(article_num):
    pass
#     """Вытаскивает информацию из карточки товара с
#         артикулом article_num на ozon.ru

#     Args:
#         article_num (str): артикул товара
#     """

#     browser = webdriver.Chrome(
#         service=ChromeService(ChromeDriverManager().install()))
#     browser.maximize_window()
#     browser.get(f"https://www.ozon.ru/product/{article_num}")

#     try:
#         brand = browser.find_element(
#             By.CLASS_NAME, "r4j").text

#     except NoSuchElementException:
#         brand = "Неизвестно"

#     try:
#         name = browser.find_element(
#             By.CLASS_NAME, "z9k").text

#     except NoSuchElementException:
#         name = "Неизвестно"

#     try:
#         discount = browser.find_element(
#             By.CLASS_NAME, "r2k").text[1:]

#     except NoSuchElementException:
#         discount = False

#     try:
#         ozon_card = browser.find_element(
#             By.CLASS_NAME, "a1-a5").text

#     except NoSuchElementException:
#         ozon_card = False

#     browser.close()
#     return [brand, name, discount, ozon_card]
