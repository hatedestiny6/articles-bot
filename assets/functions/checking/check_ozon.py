def check_ozon(article_num):
    pass
#     """Вытаскивает цену из карточки товара с
#         артикулом article_num на ozon.ru

#     Args:
#         article_num (str): артикул товара
#     """

#     browser = webdriver.Chrome(
#         service=ChromeService(ChromeDriverManager().install()))
#     browser.set_window_size(800, 800)

#     browser.get(f"https://www.ozon.ru/product/{article_num}")
#     try:
#         price = browser.find_element(
#             By.CLASS_NAME, "kx6").text

#         with open("source.html", "w", encoding='utf-8') as f:
#             f.write(browser.page_source)

#     except NoSuchElementException:
#         price = False

#     browser.close()
#     return price
