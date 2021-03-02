import requests
from pages.books_page import BooksPage
from utils.config import Config
from utils.logger import logger

logger.info("Loading the books list...")

web_page = requests.get(Config.URI_TO_SCRAPE).content
books_page = BooksPage(web_page)

books = books_page.books

for page_num in range(1, books_page.pages):
    next_page_url = f"{Config.URI_TO_SCRAPE}catalogue/page-{page_num + 1}.html"
    next_page = requests.get(next_page_url).content
    parsed_page = BooksPage(next_page)
    books.extend(parsed_page.books)
