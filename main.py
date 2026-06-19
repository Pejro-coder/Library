# Main
from library import Library
from storage_manager import StorageManager
from user import User


storage_manager = StorageManager()
storage_manager.load_books_to_storage()
library_celje = Library(storage_manager)


def add_new_books():
    print("---ADDING BOOKS TO STORAGE---")
    while True:
        while True:
            book_title = input("Book title: ").strip()
            if library_celje.book_in_storage(book_title):
                print(library_celje.book_info(book_title))
            else:
                print("Book was not found, adding as a new book!")
            try:
                nb_books = int(input(f"Number of new '{book_title}' books you want to add: "))
                if nb_books <= 0:
                    print("⚠️ Please enter a positive number.")
                    continue
                else:
                    break
            except ValueError:
                print("Please enter a whole number (1, 3, 4...)!")

        if library_celje.book_in_storage(book_title): # Updating existing book
            library_celje.update_book_amount(book_title, nb_books)
        else: # Adding new book
            book_author = input("Book_author: ")
            library_celje.add_new_book(book_title, nb_books, book_author)

        # Dynamic printing
        word = "book" if nb_books == 1 else "books"
        print(f"{nb_books} '{book_title}' {word} added to library.\n"
              f"Number of books: {library_celje.get_available_copies(book_title)}")
        print("------------------------------")

        if input("Do you want to add more books? (y/n) ") != "y":
            break


# function that calls the 'library_celje.borrow_book' method if the criteria is meet
def borrow_books():
    print("          ------BORROWING BOOKS------       ")
    while True:
        book_name_input = input("Book you want to borrow (press 'x' to exit): ").strip()
        if book_name_input == "x":
            print("Exiting form")
            return

        # Book was not found
        if not library_celje.book_in_storage(book_name_input):
            print(f"❌ {book_name_input} was not found in library. Check spelling.")
            continue

        available_books = library_celje.get_available_copies(book_name_input)
        if available_books < 1:
            print(f"There are {available_books} of {book_name_input} books available.")
            break
        else:
            print(f"Available books: {available_books}.")

        while True:
            try:
                book_amount_input = int(input(f"Number of books to borrow: ").strip())
                amount = int(book_amount_input) if book_amount_input else 1

                if amount <= 0:
                    print("⚠️ Please enter a positive number.")
                    continue

                if amount > available_books:
                    print(f"⚠️ Please enter a lower number. {available_books} books available.")
                    continue

                print(f"Borrowing {amount} {book_name_input} books?")
                confirmation = input("Please confirm (y/n): ").lower()
                if confirmation == "y":
                    # Borrowing the book from the actual storage
                    print(library_celje.borrow_book(book_name_input, book_amount_input))
                    break
                elif confirmation == "n":
                    print("0 book borrowed. Exiting.")
                    break

            except ValueError:
                print("❌ Please type a whole number.")

        if input("Borrow more books? y/n: ").lower() != "y":
            return


# function that calls the 'library_celje.return_book' method if the criteria is meet
def return_books():
    print("          ------RETURNING BOOKS------       ")
    while True:
        book_name_input = input("Book you want to return (press 'x' to exit): ").strip()
        if book_name_input == "x":
            print("Exiting form.")
            return

        while True:
            try:
                book_amount_input = int(input("How many books are you returning: ").strip())
                if book_amount_input <= 0:
                    print("⚠️ Please enter a positive number.")
                    continue
            except ValueError:
                print("Please enter a number!")
                continue


            print(f"Returning {book_amount_input} '{book_name_input}' books?")
            confirmation = input("Please confirm (y/n): ").lower()
            if confirmation == "y":
                print(library_celje.return_book(book_name_input, book_amount_input))
                break
            elif confirmation == "n":
                print("0 books returned. Exiting.")
                break


add_new_books()
borrow_books()
return_books()
storage_manager.save_books()

# hello cursor!