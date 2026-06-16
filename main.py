# Main
from library import Library
from storage_manager import StorageManager
from user import User


storage_manager = StorageManager()
storage_manager.load_books_to_storage()
print(storage_manager.book_storage["Misek Mali"])
library_celje = Library(storage_manager)
# library_celje.show_books()
# library_celje.add_new_books()



# print(library_celje.book_count("Misek Mali"))

def borrow_books():
    print("          ------BORROWING BOOKS------       ")
    while True:
        book_name_input = input("Book you want to borrow (press 'x' to exit): ").strip()
        if book_name_input == "x":
            print("Exiting form")
            return

        book_status = library_celje.book_count(book_name_input)
        # Book was not found
        if book_status[0] == False:
            print(book_status[1])
            continue
        available_books = book_status[1]
        if available_books < 1:
            print(f"There are {book_status[1]} of {book_name_input} books available.")
            break
        else:
            print(f"Available books: {book_status[1]}.")

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


borrow_books()
return_books()


storage_manager.save_books()
