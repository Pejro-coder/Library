### Library
import os
# from email.policy import default WTF JE TO?

from book import Book


class StorageManager:
    def __init__(self):
        self.storage = {}
        self.file_name = "saved_books.txt"

    # @staticmethod
    # def testing_something():
    #     print("---")

    def load_file_and_save_to_storage(self):
        # Check if file exists so we don't crash
        if not os.path.exists(self.file_name):
            print("No saved data found. Starting fresh.")
            return
        with open(self.file_name, "r") as f:
            print("\n       ------LOADING FROM FILE------\n")
            for line in f:
                line = line.strip()
                if line:
                    if ";" in line:
                        title, author, count = line.rsplit(";", 2)
                        book_obj = Book(title, author, count)
                        self.storage.update({title: book_obj})
                        # self.storage.update({title: {"author": author,
                        #                              "count": int(count)
                        #                              }})
                        print(book_obj)
                print("------------------------------")
        print(f"Loaded {len(self.storage)} unique titles.\n")


    # Saving book Name, Author and number of books to file
    def save_storage(self):
        temp_file = self.file_name + ".tmp"
        backup_file = self.file_name + ".bak"

        try:
            # 1. Write to a TEMPORARY file first
            with open(temp_file, "w") as f:
                for book_name, book_info in self.storage.items():
                    f.write(f"{book_info.title};{book_info.author};{book_info.count}\n")

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

