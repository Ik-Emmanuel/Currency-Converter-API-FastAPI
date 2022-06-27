import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class CurrencyRate(SQLModel, table=True):
    """Create a table to store currency exchange rates"""

    id: Optional[int] = Field(primary_key=True)
    symbol: str = Field(index=True)
    exchange_rate: float
    exchange_date: datetime.datetime
    created_at: datetime.datetime = datetime.datetime.now()


class CurrencySymbol(SQLModel, table=True):
    """Create a table to store available currency symbols"""

    id: Optional[int] = Field(primary_key=True)
    symbol: str
    name: str


class CurrencyConvert(SQLModel):
    currency_from: str
    currency_to: str
    amount: float
    date: Optional[datetime.datetime]
