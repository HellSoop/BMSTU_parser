from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, unique=True, nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    channel = relationship('Channel', back_populates='posts')

    def __repr__(self):
        return f'<Post(id={self.id}, url={self.url})>'
