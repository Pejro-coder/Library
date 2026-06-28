# Library
import os
import random
from storage_manager import StorageManager
from book import Book
from user import User


class Library:
    def __init__(self, storage_manager: StorageManager):
        self.db = storage_manager.book_storage
        self.users = storage_manager.user_storage

    def book_info(self, book_name):
        if book_name in self.db:
            return self.db[book_name]
        return None

    def add_new_user(
        self,
        name: str,
        surname: str,
        is_admin: bool = False,
        password: str = None,
    ):
        user = User(name, surname, is_admin=is_admin, password=password)
        while user.username in self.users:
            user.username = user.username + str(random.randint(0, 9999))
        self.users[user.username] = user
        return user

    # Used when adding a totally new book
    def add_new_book(self, book_title: str, book_amount: int, book_author: str):
        book_obj = Book(book_title, book_author, book_amount)
        self.db.update({book_title: book_obj})

    # Used when updating a book amount in storage
    def update_book_amount(self, book_title: str, book_amount: int):
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
            return 0
        return self.db[book_name].count

    # Used when the customer is borrowing a book
    def borrow_book(self, user: User, book_name: str, book_amount: int):
        if book_name not in self.db:
            return False, f"❌ '{book_name}' was not found in library. Check spelling."
        book_data = self.db[book_name]

        if book_amount > book_data.count:
            return False, f"❌ only {book_data.count} are available in storage."

        book_data.count -= book_amount
        user.borrowed_books[book_name] = user.borrowed_books.get(book_name, 0) + book_amount

        book_s = "books" if book_amount > 1 else "book"
        return True, f"✅ successfully borrowed {book_amount} '{book_name}' {book_s}."

    # Used when a customer wants to return the book
    def return_book(self, user: User, book_name: str, book_amount: int):
        if book_name not in self.db:
            return False, f"❌ {book_name} was not found in library. Check spelling."

        borrowed_count = user.borrowed_books.get(book_name, 0)
        if borrowed_count < book_amount:
            return False, (
                f"❌ you only have {borrowed_count} copy/copies of '{book_name}' to return."
            )

        remaining = borrowed_count - book_amount
        if remaining == 0:
            del user.borrowed_books[book_name]
        else:
            user.borrowed_books[book_name] = remaining

        self.db[book_name].count += book_amount
        return True, f"✅ {book_name} was successfully returned."

    def update_user(
        self,
        username: str,
        name: str,
        surname: str,
        password: str,
        is_admin: bool = False,
    ):
        if username not in self.users:
            raise ValueError("❌ User not found.")
        if not name.isalpha():
            raise ValueError("❌ Use only letters for name!")
        if not surname.isalpha():
            raise ValueError("❌ Use only letters for surname!")
        if not password.strip():
            raise ValueError("❌ Password is required.")

        user = self.users[username]
        user.name = name
        user.surname = surname
        user.password = password
        user.is_admin = is_admin
        return user
