import re
from bs4 import BeautifulSoup
from typing import List
from locators.books_page_locators import BooksPageLocators
from parsers.book import Book
from utils.logger import logger


class BooksPage:
    """
    Uses a BooksPageLocator to find all the books on a given web page
    """

    def __init__(self, content: bytes):
        logger.debug("Parsing the page content using BeautifulSoup")
        self.soup = BeautifulSoup(content, "html.parser")

    @property
    def books(self) -> List[Book]:
        logger.debug(f"Finding all books using `{BooksPageLocators.BOOK}`")
        return [Book(elem) for elem in self.soup.select(BooksPageLocators.BOOK)]

    @property
    def pages(self) -> int:
        logger.debug(f"Find total pages using `{BooksPageLocators.TOTAL_PAGES}`")
        total_pages = self.soup.select_one(BooksPageLocators.TOTAL_PAGES).string
        pattern = r"Page [0-9]+ of ([0-9]+)"
        match = re.search(pattern, total_pages)
        page_count = int(match.group(1))
        logger.info(f"Total number of pages: `{page_count}`.")
        return page_count
