from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base


class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    content_type_id = Column(Integer, ForeignKey('content_types.id'), nullable=False)
    content = Column(Text, nullable=False)

    post = relationship('Post', back_populates='attachments')
    content_type = relationship('ContentType', back_populates='attachments')

    def __repr__(self):
        return f'<Attachment(id={self.id}, content={self.content[:40]})>'
