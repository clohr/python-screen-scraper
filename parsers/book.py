import re
from bs4 import BeautifulSoup
from collections import namedtuple
from utils.config import Config
from locators.book_locators import BookLocators
from utils.logger import logger


def _format_stars(rating: int) -> str:
    plural = "" if rating == 1 else "s"
    text = f"{rating} star{plural}"
    logger.debug(f"Star ratings text: `{text}`.")
    return text


class Book(object):
    """
    Uses a BookLocator to parse book properties within a given parent element
    """

    RATINGS = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def __init__(self, parent: BeautifulSoup):
        # logger.debug(f"New book parser created from: `{parent}`.")
        self.parent = parent

    def __repr__(self):
        return f"<Book \"{self.title}\", {self.price}, {_format_stars(self.rating)}, {self.link}>"

    @property
    def title(self) -> str:
        logger.debug("Finding book title...")
        locator = BookLocators.TITLE
        _title = self.parent.select_one(locator).get("title", "")
        logger.debug(f"Title found: `{_title}`.")
        return _title

    @property
    def link(self) -> str:
        logger.debug("Finding book link...")
        locator = BookLocators.LINK
        url = self.parent.select_one(locator).get("href", "")
        full_url = Config.URI_TO_SCRAPE + url
        logger.debug(f"Link found: `{full_url}`.")
        return full_url

    @property
    def price(self) -> (str, float):
        logger.debug("Finding book price...")
        locator = BookLocators.PRICE
        elem = self.parent.select_one(locator).string
        pattern = r"(.)([0-9]+\.[0-9]{2})"
        match = re.search(pattern, elem)
        Price = namedtuple("Price", ["currency", "number"])
        price_instance = Price(match.group(1), float(match.group(2)))
        logger.debug(f"Price found: `{price_instance.currency}`, `{price_instance.number}`.")
        return price_instance

    @property
    def rating(self) -> int:
        logger.debug("Finding book rating...")
        locator = BookLocators.RATING
        css_class_list = self.parent.select_one(locator).get("class", [])
        ratings_list = [class_name for class_name in css_class_list if class_name != Config.STAR_RATING]
        key = ratings_list.pop()
        logger.debug(f"Key found: `{key}`.")
        _rating = self.RATINGS.get(key, 0)
        logger.debug(f"Rating found: `{_rating}`.")
        return _rating
