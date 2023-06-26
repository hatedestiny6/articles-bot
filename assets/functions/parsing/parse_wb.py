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
    price = str(data["salePriceU"])[:-2]

    extended = data["extended"]
    try:
        sale = extended["basicSale"]
    except KeyError:
        sale = False

    try:
        basicPriceU = str(extended["basicPriceU"])[:-2]
    except KeyError:
        basicPriceU = False

    try:
        clientSale = extended["clientSale"]
    except KeyError:
        clientSale = False

    try:
        clientPriceU = str(extended["clientPriceU"])[:-2]
    except KeyError:
        clientPriceU = False

    quantity = data["sizes"][0]["stocks"][0]["qty"]

    return [brand, name, sale, basicPriceU,
            clientSale, clientPriceU, quantity, priceU, price]
