# User
import string
import secrets


def generate_password(length=8):
    all_characters = string.ascii_letters + string.digits
    password = ""
    for character in range(length):
        password += secrets.choice(all_characters)
    # password_two = "".join(secrets.choice(all_characters) for _ in range(length))
    return password


class User:
    def __init__(
        self,
        name: str,
        surname: str,
        username: str = None,
        password: str = None,
        is_admin: bool = False,
        borrowed_books: dict = None,
    ):
        if not name.isalpha():
            raise ValueError("❌ Use only letters for name!")
        if not surname.isalpha():
            raise ValueError("❌ Use only letters for surname!")

        self.name = name
        self.surname = surname
        self.username = username if username else (name + surname).lower()
        self.password = password if password else generate_password()
        self.is_admin = is_admin
        self.borrowed_books = borrowed_books if borrowed_books is not None else {}

