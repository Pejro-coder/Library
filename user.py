# User
import string
import secrets


class User:
    def __init__(self):
        self.name = None
        self.surname = None
        self.username = None
        self.password = None


    def create_user(self):

        # Need to add check, if created user already exists...
        name = input("What's your name: ")
        if not name.isalpha():
            raise ValueError("❌ Use only letters for name!")
        self.name = name

        surname = input("What's your surname: ")
        if not surname.isalpha():
            raise ValueError("❌ Use only letters for surname!")
        self.surname = surname
        self.username = name + surname


    def generate_password(self, length=8):
        all_characters = string.ascii_letters + string.digits
        password = ""
        for character in range(length):
            password += secrets.choice(all_characters)
        # password_two = "".join(secrets.choice(all_characters) for _ in range(length))
        self.password = password




    # User login method
