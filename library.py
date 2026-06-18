# Library
import os
from storage_manager import StorageManager
from book import Book


class Library:
    def __init__(self, storage_manager:StorageManager):
        self.db = storage_manager.book_storage


    def book_info(self, book_name):
        if book_name in self.db:
            return self.db[book_name]
        return None


    # Used when adding a totally new book
    def add_new_book(self, book_title: str, book_amount:int , book_author: str = None):
            book_obj = Book(book_title, book_author, book_amount)
            self.db.update({book_title: book_obj})


    # Used when updating a book amount in storage
    def update_book_amount(self, book_title: str, book_amount:int):
        if book_title in self.db:
            self.db[book_title].count += book_amount


    # Method that prints the book information, together with the number of stored books for each book in storage
    def show_books(self):
        print("\n--- CURRENT LIBRARY INVENTORY ---")
        for book in self.db:
            print(self.db[book])


    # Check if the book already exists in storage
    def book_in_storage(self, book_name: str):
        if book_name in self.db:
            return True
        else:
            return False


    # Returns the number of a specific book in library
    def get_available_copies(self, book_name: str):
        if book_name not in self.db:
            return f"❌ {book_name} was not found in library. Check spelling."
        book_count = self.db[book_name].count
        return book_count


    # Used when the customer is borrowing a book
    def borrow_book(self, book_name: str, book_amount: int):
        if book_name not in self.db:
            return False, f"❌ '{book_name}' was not found in library. Check spelling."
        book_data = self.db[book_name]

        if book_amount > book_data.count:
            return False, f"❌ only {book_data.count} are available in storage."

        book_data.count -= book_amount

        book_s = "books" if book_amount > 1 else "book"
        return True, f"✅ successfully borrowed {book_amount} '{book_name}' {book_s}."


    # Used when a customer wants to return the book
    def return_book(self, book_name: str, book_amount: int):
        if book_name not in self.db:
            return False, f"❌ {book_name} was not found in library. Check spelling."
        else:
            self.db[book_name].count += book_amount
            return True, f"✅ {book_name} was successfully returned."


    # This method is used for the "employee" to use when new books are added to the library
    def add_new_books_old(self):
        print("---ADDING BOOKS TO STORAGE---")
        while True:
            while True:
                book_title = input("Book title: ").strip()
                if book_title in self.db:
                    print(self.db[book_title])
                try:
                    nb_books = int(input(f"Number of new '{book_title}' books you want to add: "))
                    if nb_books <= 0:
                        print("⚠️ Please enter a positive number.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Please enter a whole number (1, 3, 4...)!")

            if book_title in self.db:
                self.db[book_title].count += nb_books
            else:
                book_author = input("Book_author: ")
                book_obj = Book(book_title, book_author, nb_books)
                self.db.update({book_title: book_obj})
                print("New book added to library!")

            # Dynamic printing
            word = "book" if nb_books == 1 else "books"
            print(f"{nb_books} '{book_title}' {word} added to library.\n"
                  f"Number of books: {self.db[book_title].count}")
            print("------------------------------")

            if input("Do you want to add more books? (y/n) ") != "y":
                break

