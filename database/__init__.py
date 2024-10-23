from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.attachments import Attachment
from .models.channels import Channel
from .models.content_types import ContentType
from .models.posts import Post
from .models.users import User

engine = create_engine('sqlite:///database/bot.db')  # it will only work if you use it from main or another root package
session = sessionmaker(bind=engine)
