try:
    from sedenecem.sql import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String


class Mute(BASE):
    __tablename__ = "muted"
    chat_id = Column(String(14), primary_key=True)
    sender = Column(String(14), primary_key=True)

    def __init__(self, chat_id, sender):
        self.chat_id = str(chat_id)  # ensure string
        self.sender = str(sender)


Mute.__table__.create(checkfirst=True)


def is_muted(chat_id, sender):
    try:
        ret = (
            SESSION.query(Mute)
            .filter(Mute.chat_id == str(chat_id), Mute.sender == str(sender))
            .all()
        )
        return len(ret) > 0
    except BaseException:
        return None
    finally:
        SESSION.close()


def mute(chat_id, sender):
    adder = Mute(str(chat_id), str(sender))
    SESSION.add(adder)
    SESSION.commit()


def unmute(chat_id, sender):
    rem = (
        SESSION.query(Mute)
        .filter(Mute.chat_id == str(chat_id), Mute.sender == str(sender))
        .all()
    )
    if len(rem):
        for item in rem:
            SESSION.delete(item)
            SESSION.commit()
