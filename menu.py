from app import books

USER_CHOICES = """
    Enter one of the following:
    
    - "b" to look at 5-star books
    - "c" to look at the cheapest books
    - "n" to get the next available book on the page
    - "q" to exit
    
    Enter your choice: 
"""


def print_best_books():
    print("\n---BEST RATED BOOKS---\r")
    sorted_best_books = sorted(books, key=lambda x: (x.rating * -1, x.price))[:10]
    for book in sorted_best_books:
        print(book)


def print_cheapest_books():
    print("\n---CHEAPEST BOOKS---\r")
    sorted_cheapest_books = sorted(books, key=lambda x: x.price)[:10]
    for book in sorted_cheapest_books:
        print(book)


books_generator = (book for book in books)


def get_next_book():
    print(next(books_generator))


VALID_CHOICES = {
    "b": print_best_books,
    "c": print_cheapest_books,
    "n": get_next_book
}


def menu():
    user_input = input(USER_CHOICES)
    while user_input != "q":
        if VALID_CHOICES[user_input]:
            VALID_CHOICES[user_input]()
        else:
            print("Please enter a valid choice.")
        user_input = input(USER_CHOICES)


menu()
