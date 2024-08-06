from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from extensions import db


class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(nullable=False, unique=True)
    create_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f'<TokenBlocklist {self.jti}>'
