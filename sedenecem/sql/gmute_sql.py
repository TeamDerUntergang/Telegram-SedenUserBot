try:
    from sedenecem.sql import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GMute.__table__.create(checkfirst=True)


def is_gmuted(sender):
    try:
        ret = SESSION.query(GMute).filter(GMute.sender == str(sender)).all()
        return len(ret) > 0
    except BaseException:
        return None
    finally:
        SESSION.close()


def gmute(sender):
    adder = GMute(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender):
    rem = SESSION.query(GMute).get((str(sender)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
