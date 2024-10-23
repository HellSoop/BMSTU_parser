from sqlalchemy import Column, Integer
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    def __repr__(self):
        return f'<User(telegram_id={self.telegram_id})>'
