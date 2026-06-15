# Main
from library import Library
from storage_manager import StorageManager
from user import User


storage_manager = StorageManager()
storage_manager.load_books_to_storage()

library_celje = Library(storage_manager)
# library_celje.show_books()
# library_celje.add_new_books()
# library_celje.borrow_book()

storage_manager.save_books()


# Test comment,
# Test comment two


def return_books():
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


return_books()