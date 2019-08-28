from .base import db


class Book(db.Model):
    """Represents a book that can be requested for email delivery"""

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String)

    def __init__(self, title: str):
        self.title = title

    def __repr__(self):
        return f"<Book {self.title}>"
