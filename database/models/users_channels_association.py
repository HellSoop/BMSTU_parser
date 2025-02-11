from sqlalchemy import Column, Integer, ForeignKey
from database.models.base import Base


class UserChannelAssociation(Base):
    __tablename__ = 'users_channels_association'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), primary_key=True)
