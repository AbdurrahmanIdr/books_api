from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid4()))
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[Text] = mapped_column(nullable=False)  
    
    def __repr__(self) -> str:
        return f"<User {self.username, self.email, self.password}>"
    