import random
from typing import Any

import requests
from bs4 import BeautifulSoup

from libanekdoty.exception import *


class Categories:
    r"""
    Parse categories from anekdoty.ru
    """

    def __init__(self, lxml: bool = False) -> None:
        r"""
        :param lxml: Enable lxml parser. Parsing speed may increase (external dependency)
        """
        self.URL = "https://anekdoty.ru/"
        self.parser_type = "lxml" if lxml else "html.parser"

    def get_all_categories(self) -> list[dict[str, Any]]:
        r"""
            Return all joke categories
        """
        categories = []

        request = requests.get(self.URL)

        if request.status_code == 404:
            raise LibanekdotyException("Server returned 404")

        parser = BeautifulSoup(request.text, self.parser_type)

        category_list_element = parser.find("div", {"class": "category-list"}).find_all("li")
        for category in category_list_element:
            link = category.a
            name = link.text
            url = link["href"]
            quantity = category.find("strong").text
            categories.append({
                "name": name,
                "url": url,
                "quantity": quantity
            })
        return categories

    def get_random_category(self) -> dict:
        """Return random category"""
        categories = self.get_all_categories()
        return random.choice(categories)