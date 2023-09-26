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
        self._URL = category_url
        self.parser_type = "lxml" if lxml else "html.parser"

    def get_jokes_from_selected_page(self, page_num: int) -> list[dict[str, Any]]:
        r"""
        Returns jokes from the selected page
        :param page_num: Page number
        """
        url = self._URL
        jokes = []

        if page_num > 1:
            url = f"{url}{page_num}/"

        request = requests.get(url)

        if request.status_code == 404:
            raise LibanekdotyException("Server returned 404")

        parser = BeautifulSoup(request.text, self.parser_type)

        joke_list_element = parser.find("ul", {"class": "item-list"}).find_all("li", recursive=False)
        for joke in joke_list_element:
            joke_text = joke.find("div", {"class": "holder-body"}).p.text
            top = joke.find("div", {"class": "like-counter"}).text
            jokes.append({"text": joke_text, "top": top})
        return jokes

    def get_all_jokes(self) -> list[dict[str, Any]]:
        r"""Get all jokes from category"""
        jokes = []
        current_url = self._URL

        while True:
            request = requests.get(current_url)

            if request.status_code == 404:
                raise LibanekdotyException("Server returned 404")

            parser = BeautifulSoup(request.text, self.parser_type)

            joke_list_element = parser.find("ul", {"class": "item-list"}).find_all("li", recursive=False)
            for joke in joke_list_element:
                joke_text = joke.find("div", {"class": "holder-body"}).p.text
                top = joke.find("div", {"class": "like-counter"}).text
                jokes.append({"text": joke_text, "top": top})

            next_page_element = parser.find("li", {"class": "next"})
            next_page_link = next_page_element.find("a")

            if next_page_link is None:  # checks that the link to the next page is not None
                break

            current_url = next_page_link["href"]
        return jokes

    def get_number_of_pages(self) -> str:
        """Get the number of pages with jokes """

        request = requests.get(self._URL)

        if request.status_code == 404:
            raise LibanekdotyException("Server returned 404")

        parser = BeautifulSoup(request.text, self.parser_type)

        page_list = parser.find_all("li", {"class": "pagination-holder-item"})
        return page_list[-1].text
