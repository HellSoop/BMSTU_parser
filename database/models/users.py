from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    channels = relationship('Channel', secondary='users_channels_association', back_populates='subscribers')

    def __repr__(self):
        return f'<User(telegram_id={self.telegram_id})>'
