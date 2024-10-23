from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    is_important = Column(Boolean, nullable=False, default=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    attachments = relationship('Attachment', back_populates='post', cascade='save-update, merge, delete')
    channel = relationship('Channel', back_populates='posts')

    def __repr__(self):
        return f'<Post(id={self.id}, text={self.text[:30]}...)>'
