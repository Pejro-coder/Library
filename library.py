### Library
import os
from email.policy import default

from book import Book

class Library:
    def __init__(self):
        self.storage = {}
        self.file_name = "saved_books.txt"

    @staticmethod
    def testing_something():
        print("---")


    def load_file_and_save_to_storage(self):
        # Check if file exists so we don't crash
        if not os.path.exists(self.file_name):
            print("No saved data found. Starting fresh.")
            return
        with open(self.file_name, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    if ";" in line:
                        title, author, count = line.rsplit(";",2 )
                        print("Loading:")
                        print(title, author, count)
                        self.storage.update({title: {"author": author,
                                                     "count": int(count)
                                                     }})
                print("------------------------------")
        print(f"Loaded {len(self.storage)} unique titles.")


    def store_book(self, book_obj: Book):
        # Checking if the book is already in storage
        if book_obj.title in self.storage:
            self.storage[book_obj.title]["count"] += 1

            # print(f"-> Updated the number of stored '{book_obj.title}'\n")
        else:
            self.storage.update({book_obj.title: {"author": book_obj.author,
                                                  "count": 1}})
            # print(f"-> Stored '{book_obj.title}'\n")


    # Method that prints the book information, together with the number of stored books
    def show_books(self):
        print("\n--- CURRENT LIBRARY INVENTORY ---")
        self.testing_something()
        for book in self.storage:
            print(f"{book}, {self.storage[book]}")
        print(f"\n{self.storage=}")


    def borrow_book(self):
        while True:
            book_name_input = input("Book you want to borrow: ").strip()

            if book_name_input not in self.storage:
                print(f"❌ {book_name_input} was not found in library.")
                return

            book_data = self.storage[book_name_input]
            print(f"Available books: {book_data["count"]}.")

            while True:
                try:
                    book_amount_input = input(f"Number of books to borrow: ").strip()
                    amount = int(book_amount_input) if book_amount_input else 1

                    if amount <= 0:
                        print("⚠️ Please enter a positive number:.")
                        continue

                    if amount > book_data["count"]:
                        print(f"⚠️ Please enter a lower number. {book_data["count"]} books available.")
                        continue


                    print(f"Borrowing {amount} {book_name_input} books?")
                    confirmation = input("Please confirm (y/n): ").lower()
                    if confirmation == "y":
                        book_data["count"] -= amount
                        print(f"✅ {amount} {book_name_input} books were successfully borrowed. ")
                        break
                    elif confirmation == "n":
                        print("0 book borrowed. Exiting.")
                        break

                except ValueError:
                    print("❌ Please type a whole number.")

            add_more_book = input("Add more books? y/n: ").lower()
            if add_more_book == "y":
                continue

            elif add_more_book == "n":
                return


    # Saving book Name and number of books to file
    def save_storage(self):
        temp_file = self.file_name + ".tmp"
        backup_file = self.file_name + ".bak"

        try:
            # 1. Write to a TEMPORARY file first
            with open(temp_file, "w") as f:
                for title, info in self.storage.items():
                    f.write(f"{title};{info['author']};{info['count']}\n")

            # 2. If writing succeeded, create a backup of the old file
            if os.path.exists(self.file_name):
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                os.rename(self.file_name, backup_file)

            # 3. Rename the temp file to the real filename
            os.rename(temp_file, self.file_name)
            print("✅ Data saved securely.")

        except Exception as e:
            print(f"❌ Critical Save Error: {e}")