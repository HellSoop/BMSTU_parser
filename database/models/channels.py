from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models.base import Base


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship('Post', back_populates='channel', cascade='save-update, merge, delete')

    def __repr__(self):
        return f'<Channel(id={self.id}, name={self.name})>'
