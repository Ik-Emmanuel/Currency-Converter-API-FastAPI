from sqlmodel import SQLModel
from db.db import engine
from models.currency_models import CurrencySymbol, CurrencyRate
from models.user_models import *
import os

pwd = os.path.dirname(os.path.abspath(__file__))
path_to_file = os.path.join(pwd, "currency_db.sqlite")
db_exists = os.path.exists(path_to_file)

def create_db_tables():
    if not db_exists:
        print("Creating database...")
        SQLModel.metadata.create_all(engine)
    else:
        print("Database already exists")
