import os
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
                print(line)
                if line:
                    if ";" in line:
                        title, author, count = line.rsplit(";",2 )
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

    # Saving book Name and number of books to file
    def save_storage(self):
        with open(self.file_name, "w") as f:
            # for book in self.storage:
            #     f.write(f"{book};{self.storage[book]["author"]};{self.storage[book]["count"]}\n")
            #     # print(book.title)
            for title, info in self.storage.items():
                author = info["author"]
                count = info["count"]
                f.write(f"{title};{author};{count}\n")
                # print(book.title)