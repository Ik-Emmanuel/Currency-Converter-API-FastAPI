from db.db import engine
from models.currency_models import CurrencyRate, CurrencySymbol
from sqlmodel import Session, select, or_


def select_all_currency():
    with Session(engine) as session:
        statement = select(CurrencySymbol)
        result = session.exec(statement)
        return result


def select_rate(symbol):
    with Session(engine) as session:
        statement = select(CurrencyRate)
        statement = statement.where(CurrencyRate.symbol==symbol)
        result = session.exec(statement)
        return result.first()


def select_rate_date(symbol, date):
    with Session(engine) as session:
        statement = select(CurrencyRate)
        statement = statement.where(CurrencyRate.symbol==symbol).where(CurrencyRate.exchange_date == date)
        result = session.exec(statement)
        return result.first()
