from sqlalchemy import text
from .base import db
from .Book import Book


class BookRequest(db.Model):
    """Represents a request for a book by someone"""

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship(
        Book, backref=db.backref("requests", uselist=True, cascade="delete,all")
    )
    created = db.Column(db.DateTime, server_default=text("now()"))

    def __init__(self, email, book):
        self.email = email
        self.book = book

    def __repr__(self):
        return f"<BookRequest {self.email} - {self.book}>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "title": self.book.title,
            "timestamp": self.created,
        }
