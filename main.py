# Main
from library import Library
from storage_manager import StorageManager
from user import User

storage_manager = StorageManager()
storage_manager.load_books_to_storage()

# storage_manager.load_users()

# peter = User("Peter", "Stepanic")
# peter.generate_password()
# storage_manager.save_user(peter)
# tomaz = User("Tomaz", "Stepanic")
# tomaz.generate_password()
# storage_manager.save_user(tomaz)
# tom = User("Tom", "Stepanic")
# tom.generate_password()
# storage_manager.save_user(tom)
# julija = User("Julija", "Stepanic")
# julija.generate_password()
# storage_manager.save_user(julija)

library_celje = Library(storage_manager)
# library_celje.show_books()

library_celje.add_new_books()
library_celje.return_book()
library_celje.borrow_book()

storage_manager.save_books()


# Test comment,
# Test comment two