from pickle import dumps, loads

from sedenecem.sql import BASE, SESSION
from sqlalchemy import Column, Integer, LargeBinary


class GDriveCreds(BASE):
    __tablename__ = 'GDrive'

    user_id = Column(Integer, primary_key=True)
    credentials_string = Column(LargeBinary)

    def __init__(self, user_id):
        self.user_id = user_id


GDriveCreds.__table__.create(checkfirst=True)


def set(user_id, credentials):
    saved_creds = SESSION.query(GDriveCreds).get(user_id)
    if not saved_creds:
        saved_creds = GDriveCreds(user_id)
    saved_creds.credentials_string = dumps(credentials)

    SESSION.add(saved_creds)
    SESSION.commit()


def get(user_id):
    saved_creds = SESSION.query(GDriveCreds).get(user_id)
    creds = None
    if saved_creds is not None:
        creds = loads(saved_creds.credentials_string)
    return creds


def remove_(user_id):
    saved_cred = SESSION.query(GDriveCreds).get(user_id)
    if saved_cred:
        SESSION.delete(saved_cred)
        SESSION.commit()
