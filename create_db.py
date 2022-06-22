from sqlmodel import SQLModel
from db.db import engine
from models.currency_models import CurrencySymbol, CurrencyRate
from models.user_models import *

def create_db_tables():
    print('CREATING DATABASE........')
    SQLModel.metadata.create_all(engine)

