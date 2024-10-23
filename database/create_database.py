from sqlalchemy import create_engine
from database.models.base import Base


if __name__ == '__main__':
    engine = create_engine('sqlite:///bot.db')
    Base.metadata.create_all(engine)
    print('Database has been created')
