# Book

class Book:
    def __init__(self, title, author, count = 1):
        self.title = title
        self.author = author
        self.count = int(count)
        self.is_available = True

    def __str__(self):
        return f"📘 {self.title} by {self.author}. Stored books: {self.count}"

    def save_format(self):
        return f"📘 {self.title} | {self.author} | {self.count}"
