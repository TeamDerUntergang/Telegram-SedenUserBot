try:
    from sedenecem.sql import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String


class KRead(BASE):
    __tablename__ = "kread"
    groupid = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.groupid = str(sender)


KRead.__table__.create(checkfirst=True)


def is_kread():
    try:
        return SESSION.query(KRead).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def kread(chat):
    if SESSION.query(KRead).get((str(chat))):
        return False
    adder = KRead(str(chat))
    SESSION.add(adder)
    SESSION.commit()
    return True


def unkread(chat):
    rem = SESSION.query(KRead).get((str(chat)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
        return True
    return False
