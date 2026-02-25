### Book

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"📘 {self.title} by {self.author}"

    def save_format(self):
        return f"📘 {self.title} | {self.author} | {self.is_available}"

    # def create_book(self):
    #     input("Book title: ")
    #     input("Book author: ")
