# Library
import os
from book import Book
from pathlib import Path
from user import User
import random


class StorageManager:
    def __init__(self):
        self.book_storage = {}
        self.book_storage_file = Path("saved_books.txt")
        self.user_storage = {}
        self.user_storage_file = Path("users.txt")

    # @staticmethod
    # def testing_something():
    #     print("---")

    # ----------------------- Methods that handle books ------------------------------------------

    def load_books_to_storage(self):
        # Check if file exists so we don't crash
        if not os.path.exists(self.book_storage_file):
            print("No BOOK saved data found. Starting fresh.")
            # with open(self.book_storage_file, "w") as f:  # Creating new file is handled at at save_storage_to_file
            #     f.write("")
            return
        with open(self.book_storage_file, "r") as f:
            print("\n       ------LOADING BOOKS FROM FILE------\n")
            for line in f:
                line = line.strip()
                if line:
                    if ";" in line:
                        title, author, count = line.rsplit(";", 2)
                        book_obj = Book(title, author, count)
                        self.book_storage.update({title: book_obj})
                #         print(book_obj)
                # print("------------------------------")
        print(f"Loaded {len(self.book_storage)} unique titles.\n")

    # Saving book Name, Author and number of books to file
    def save_books(self):
        temp_file = self.book_storage_file.with_suffix(".txt.tmp")
        backup_file = self.book_storage_file.with_suffix(".txt.bak")

        try:
            # 1. Write to a TEMPORARY file first
            # book.storage.items() consists of {book_name : book_obj,...}
            with open(temp_file, "w") as f:
                for book_name, book_info in self.book_storage.items():
                    f.write(f"{book_info.title};{book_info.author};{book_info.count}\n")

            # 2. If writing succeeded, create a backup of the old file
            if os.path.exists(self.book_storage_file):
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                os.rename(self.book_storage_file, backup_file)

            # 3. Rename the temp file to the real filename
            os.rename(temp_file, self.book_storage_file)
            print("✅ Data saved securely.")

        except Exception as e:
            print(f"❌ Critical Save Error: {e}")

    # ----------------------- Methods that handle users ------------------------------------------

    # # Show created users, that are saved inside the user_storage_file
    # def load_users(self):
    #     with open(self.user_storage_file, "r") as f:
    #         for line in f:
    #             print(f"{line=}")

    # Show created users, that are saved inside the user_storage_file
    def load_users_to_storage(self):
        # Check if file exists so we don't crash
        if not os.path.exists(self.user_storage_file):
            print("No USER saved data found. Starting fresh.")
            return
        with open(self.user_storage_file, "r") as f:
            for line in f:
                split_line = line.strip().split(",")
                user = User(name=split_line[0], surname=split_line[1], username=split_line[2], password=split_line[3])
                self.user_storage.update({split_line[2]: user})
        print("\n       ------LOADING USERS FROM FILE------\n")
        for user in self.user_storage:
            print(user, self.user_storage[user])
        print(f"Loaded {len(self.user_storage)} users.\n")

    # Save created use to the user_storage_file
    def save_user(self, user: User):
        # Check for user duplicate
        if user.username in self.user_storage:
            print("This username is already taken!")
            go_on = input("Adding the user with a new username (y to continue): ").lower()
            if go_on == "y":
                while user.username in self.user_storage:
                    user.username = user.username + str(random.randint(0, 1))
            else:
                print("Canceling...")
                return
        self.user_storage.update({user.username: user})
        to_save = f"{user.name},{user.surname},{user.username},{user.password}\n"
        print(f"{to_save=}")
        with open(self.user_storage_file, "a") as f:
            f.write(to_save)


if __name__ == "__main__":
    shramba = StorageManager()
    # shramba.load_books_to_storage()

    peter = User("Komad", "Drugi")
    luka = User("Luka", "Drugi")
    # print(peter.surname, peter.username)
    shramba.load_users_to_storage()
    peterstepanic = shramba.user_storage["peterstepanic"]
    print(shramba.user_storage["peterstepanic"].password)
    print(shramba.user_storage["lukadrugi"].password)

    shramba.save_user(peter)
    shramba.save_user(luka)
