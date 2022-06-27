import os
from sqlmodel import create_engine
from sqlmodel import Session

pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(pwd, "currency_db.sqlite")
connect_args = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args=connect_args)
session = Session(bind=engine)
