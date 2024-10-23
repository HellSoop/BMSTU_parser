from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class ContentType(Base):
    __tablename__ = 'content_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    attachments = relationship('Attachment', back_populates='content_type',
                               cascade='save-update, merge, delete')

    def __repr__(self):
        return f'<ContentType(id={self.id}, name={self.name})>'
