from typing import Any

import requests
from bs4 import BeautifulSoup

from libanekdoty.exception import *


class Jokes:
    """Parsing jokes from anekdoty.ru categories"""

    def __init__(self, category_url: str, lxml: bool = False) -> None:
        r"""
        :param category_url: Jokes category URL
        :param lxml: Enable lxml parser. Parsing speed may increase (external dependency)
        """
        self.URL = category_url
        self.parser_type = "lxml" if lxml else "html.parser"

    def get_all_jokes(self) -> list[dict[str, Any]]:
        """Get all jokes from category"""
        jokes = []
        request = requests.get(self.URL)
        if request.status_code == 404:
            raise LibanekdotyException("Server returned 404")
        parser = BeautifulSoup(request.text, self.parser_type)
        joke_list = parser.find("ul", {"class": "item-list"}).find_all("li", recursive=False)
        for joke in joke_list:
            joke_text = joke.find("div", {"class": "holder-body"}).p.text
            top = joke.find("div", {"class": "like-counter"}).text
            jokes.append({"text": joke_text, "top": top})
        return jokes
