# models for books api
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BOOLEAN
from extensions import db


class Books(db.Model):
    """Books ORM"""
    
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(32))
    available: Mapped[BOOLEAN] = mapped_column(BOOLEAN)

    def to_dict(self) -> dict:
        new_book = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "available": self.available,
        }

        return new_book

    def __repr__(self) -> str:
        return f"Books(id={self.id}, name={self.name}, \
    type={self.type}, available={self.available})"
