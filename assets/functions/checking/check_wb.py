import requests
import json


def check_wb(article_num):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru

    Args:
        article_num (str): артикул товара
    """
    url = "https://card.wb.ru/cards/detail?appType=1&curr=rub" \
        f"&dest=-331412&fregions=68,69,30,86,1,66,22,48,114&spp=30&nm={article_num}"
    data = requests.get(url, timeout=3)

    if data.json()["data"]["products"]:
        with open("source.json", 'w', encoding='utf-8') as source:
            json.dump(data.json()["data"]["products"][0], source)
    else:
        return False

    return str(data.json()["data"]["products"][0]["salePriceU"])[:-2]
