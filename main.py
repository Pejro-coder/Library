### Main
from book import Book
from library import Library


# Testing... adding books to library
library_celje = Library()
library_celje.load_file_and_save_to_storage()



library_celje.return_book()
library_celje.update_storage()
library_celje.borrow_book()



library_celje.show_books()
library_celje.save_storage()

