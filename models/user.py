from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid4()))
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'
