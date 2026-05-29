### Main
from library import Library
from storage_manager import StorageManager


storage_manager = StorageManager()
storage_manager.load_file_and_save_to_storage()

library_celje = Library(storage_manager)
library_celje.show_books()
library_celje.add_new_books()
library_celje.return_book()
library_celje.borrow_book()

storage_manager.save_storage()

