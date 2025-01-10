from sqlalchemy import create_engine
from database.models.base import Base
from database import session, Channel
from parsers.channels import channels_names


if __name__ == '__main__':
    engine = create_engine('sqlite:///database/bot.db')
    Base.metadata.create_all(engine)

    channels = [Channel(id=cid, name=name) for cid, name in channels_names.items()]
    s = session()
    s.add_all(channels)
    s.commit()
    s.close()

    print('Database has been created')
