from database import session, User


# TODO: optimize registration check
def is_registered(telegram_id: int) -> bool:
    s = session()
    u = s.query(User).where(User.telegram_id == telegram_id).scalar()
    s.close()
    return u is not None


def register_user(telegram_id: int) -> None:
    s = session()
    s.add(User(telegram_id=telegram_id))
    s.commit()
    s.close()


def unregister_user(telegram_id: int) -> None:
    s = session()
    u = s.query(User).where(User.telegram_id == telegram_id).scalar()

    if u is not None:
        s.delete(u)
        s.commit()

    s.close()
