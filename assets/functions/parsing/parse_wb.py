import json


def parse_wb():
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru
    """
    with open("source.json", 'r', encoding='utf-8') as source:
        data = json.load(source)

    brand = data["brand"]
    name = data["name"]
    priceU = str(data["priceU"])[:-2]
    salePriceU = str(data["salePriceU"])[:-2]

    # extended = data["extended"]
    try:
        sale = data["sale"]
    except KeyError:
        sale = False

    # try:
    #     priceU = str(data["priceU"])[:-2]
    # except KeyError:
    #     priceU = False

    # try:
    #     clientSale = extended["clientSale"]
    # except KeyError:
    #     clientSale = False

    # try:
    #     clientPriceU = str(extended["clientPriceU"])[:-2]
    # except KeyError:
    #     clientPriceU = False

    # quantity = data["sizes"][0]["stocks"][0]["qty"]

    return [brand, name, sale, priceU, salePriceU]
