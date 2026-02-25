### Main
from book import Book
from library import Library


# Book objects
misek_mali = Book("Misek Mali", "Peter")
trava_raste = Book("Trava raste", "Tomaz")
harry_potter = Book("Harry Potter", "JK")
the_lion = Book("The Lion, the Witch and the Wardrobe", "Kr En")


# Testing... adding books to library
library_celje = Library()
library_celje.load_file_and_save_to_storage()

library_celje.store_book(misek_mali)
library_celje.store_book(trava_raste)
# library_celje.store_book(harry_potter)
# library_celje.store_book(harry_potter)
# library_celje.store_book(harry_potter)
# library_celje.store_book(trava_raste)
# library_celje.store_book(misek_mali)
# library_celje.store_book(the_lion)

library_celje.borrow_book()

library_celje.show_books()
library_celje.save_storage()

