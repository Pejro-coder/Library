# ### Library
# import os
#
#
# from book import Book
#
#
# class Library:
#     def __init__(self):
#         self.storage = {}
#         self.file_name = "saved_books.txt"
#
#     # @staticmethod
#     # def testing_something():
#     #     print("---")
#
#     def load_file_and_save_to_storage(self):
#         # Check if file exists so we don't crash
#         if not os.path.exists(self.file_name):
#             print("No saved data found. Starting fresh.")
#             return
#         with open(self.file_name, "r") as f:
#             print("Loading:\n")
#             for line in f:
#                 line = line.strip()
#                 if line:
#                     if ";" in line:
#                         title, author, count = line.rsplit(";", 2)
#                         book_obj = Book(title, author, count)
#                         self.storage.update({title: book_obj})
#                         # self.storage.update({title: {"author": author,
#                         #                              "count": int(count)
#                         #                              }})
#                         print(title, book_obj)
#                 print("------------------------------")
#         print(f"Loaded {len(self.storage)} unique titles.\n")
#
#     # Saving book Name, Author and number of books to file
#     def save_storage(self):
#         temp_file = self.file_name + ".tmp"
#         backup_file = self.file_name + ".bak"
#
#         try:
#             # 1. Write to a TEMPORARY file first
#             with open(temp_file, "w") as f:
#                 for book_name, book_info in self.storage.items():
#                     f.write(f"{book_info.title};{book_info.author};{book_info.count}\n")
#
#             # 2. If writing succeeded, create a backup of the old file
#             if os.path.exists(self.file_name):
#                 if os.path.exists(backup_file):
#                     os.remove(backup_file)
#                 os.rename(self.file_name, backup_file)
#
#             # 3. Rename the temp file to the real filename
#             os.rename(temp_file, self.file_name)
#             print("✅ Data saved securely.")
#
#         except Exception as e:
#             print(f"❌ Critical Save Error: {e}")
#
#     # Method that prints the book information, together with the number of stored books
#     def show_books(self):
#         print("\n--- CURRENT LIBRARY INVENTORY ---")
#         for book in self.storage:
#             print(self.storage[book])
#
#     # This method is used for the "employee" to use when new books are added to the library
#     def update_storage(self):
#         print("---ADDING BOOKS TO STORAGE---")
#         while True:
#             book_title = input("Book title: ").strip()
#             nb_books = int(input(f"Number of new '{book_title}' books you want to add: "))
#
#             if nb_books <= 0:
#                 print("⚠️ Please enter a positive number.")
#                 continue
#
#             if book_title in self.storage:
#                 # book_obj = Book(book_title, self.storage[book_title]["author"])
#                 self.storage[book_title].count += nb_books
#             else:
#                 book_author = input("Book_author: ")
#                 book_obj = Book(book_title, book_author, nb_books)
#                 self.storage.update({book_title: book_obj})
#                 # self.storage.update({book_obj.title: {"author": book_obj.author,
#                 #                                       "count": nb_books}})
#                 print("New book added to library!")
#
#             # Dynamic printing
#             word = "book" if nb_books == 1 else "books"
#             print(f"{nb_books} '{book_title}' {word} added to library.\n"
#                   f"Number of books: {self.storage[book_title].count}")
#             print("------------------------------")
#
#             if input("Do you want to add more books? (y/n) ") != "y":
#                 break
#
#     # Used when a customer wants to return the book
#     def return_book(self):
#         print("---RETURNING BOOKS---")
#         while True:
#             book_name_input = input("Book you want to return: ").strip()
#
#             if book_name_input == "x":
#                 print("Exiting form.")
#                 return
#
#             elif book_name_input not in self.storage:
#                 print(f"❌ '{book_name_input}' was not found in library. Check spelling.")
#                 continue
#
#             while True:
#                 book_amount_input = int(input("How many books are you returning: ").strip())
#                 if book_amount_input <= 0:
#                     print("⚠️ Please enter a positive number.")
#                     continue
#
#                 print(f"Returning {book_amount_input} {book_name_input} books?")
#                 confirmation = input("Please confirm (y/n): ").lower()
#                 if confirmation == "y":
#                     self.storage[book_name_input].count += book_amount_input
#                     print(f"✅ {book_amount_input} {book_name_input} books were successfully returned. ")
#                     break
#                 elif confirmation == "n":
#                     print("0 book borrowed. Exiting.")
#                     break
#
#             if input("Do you want to return more books? (y/n): ").strip() != "y":
#                 break
#
#     # Used when the customer is borrowing a book
#     def borrow_book(self):
#         print("---BORROWING BOOKS---")
#         while True:
#             book_name_input = input("Book you want to borrow: ").strip()
#
#             if book_name_input == "x":
#                 print("Exiting form")
#                 return
#
#             elif book_name_input not in self.storage:
#                 print(f"❌ '{book_name_input}' was not found in library. Check spelling.")
#                 continue
#
#             book_data = self.storage[book_name_input]
#             print(f"Available books: {book_data.count}.")
#
#             while True:
#                 try:
#                     book_amount_input = input(f"Number of books to borrow: ").strip()
#                     amount = int(book_amount_input) if book_amount_input else 1
#
#                     if amount <= 0:
#                         print("⚠️ Please enter a positive number.")
#                         continue
#
#                     if amount > book_data.count:
#                         print(f"⚠️ Please enter a lower number. {book_data.count} books available.")
#                         continue
#
#                     print(f"Borrowing {amount} {book_name_input} books?")
#                     confirmation = input("Please confirm (y/n): ").lower()
#                     if confirmation == "y":
#                         book_data.count -= amount
#                         print(f"✅ {amount} {book_name_input} books were successfully borrowed. ")
#                         break
#                     elif confirmation == "n":
#                         print("0 book borrowed. Exiting.")
#                         break
#
#                 except ValueError:
#                     print("❌ Please type a whole number.")
#
#             if input("Borrow more books? y/n: ").lower() != "y":
#                 return
#
#
#
#
