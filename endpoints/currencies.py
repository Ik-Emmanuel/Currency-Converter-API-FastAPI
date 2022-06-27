from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select
from starlette.responses import JSONResponse
from endpoints.users import auth_handler
from models.currency_models import CurrencyConvert, CurrencyRate
from db.db import session
import datetime
import pytz

utc = pytz.UTC

converter_router = APIRouter(
    tags=["Currency Converter"],
    prefix="/convert",
)


def get_rate(symbol: str, date: str = None):
    """This Function checks for rates from database with date or with date provided"""
    if date:
        try:
            rate = (
                select(CurrencyRate)
                .where(CurrencyRate.symbol == symbol)
                .where(CurrencyRate.exchange_date <= date)
                .order_by(CurrencyRate.exchange_date.desc())
            )
            rate = session.exec(rate).first()
            return (rate.exchange_rate, rate.exchange_date)
        except Exception:
            return (
                f"No exchange rate data for: {symbol} for date period before {date}",
                None,
            )
    else:
        try:
            rate = (
                select(CurrencyRate)
                .where(CurrencyRate.symbol == symbol)
                .order_by(CurrencyRate.exchange_date.desc())
            )
            rate = session.exec(rate).first()
            return (rate.exchange_rate, rate.exchange_date)
        except Exception:
            return (
                f"Error fetching rate for currency: {symbol}. Please confirm currency symbol",
                None,
            )


async def convert_currency(
    from_currency: str, to_currency: str, amount: float, date: str = None
):
    """This function converts currencies given a from_currency and to_currency"""
    final_result = {}
    Errors = []
    if date:
        try:
            from_rate = get_rate(from_currency, date)
            if not from_rate[1]:
                Errors.append(from_rate[0])
            to_rate = get_rate(to_currency, date)
            if not to_rate[1]:
                Errors.append(to_rate[0])
            result = amount * (to_rate[0] / from_rate[0])
            date = from_rate[1]
            final_result["status"] = "Success"
            final_result["converted_currency"] = "{:.2f}".format(result)
            final_result["price_date"] = date
            return final_result
        except Exception:
            final_result["status"] = "Error"
            final_result["message"] = Errors
            return final_result
    else:
        try:
            from_rate = get_rate(from_currency)
            if not from_rate[1]:
                Errors.append(from_rate[0])
            to_rate = get_rate(to_currency)
            if not to_rate[1]:
                Errors.append(to_rate[0])
            result = amount * (to_rate[0] / from_rate[0])
            date = from_rate[1]
            final_result["status"] = "Success"
            final_result["converted_currency"] = "{:.2f}".format(result)
            final_result["price_date"] = date
            return final_result
        except Exception:
            final_result["status"] = "Error"
            final_result["message"] = Errors
            return final_result


@converter_router.post("/", status_code=200, description="Convert Currencies")
async def currency_converter(
    converter: CurrencyConvert, user=Depends(auth_handler.get_current_user)
):
    """
    Converts currencies given two currency symbols and an amount
    This gets converted currency amount if given 2 currency symbols,
    an amount and a date period of format(%YY-%MM-%DD e.g 2022-06-22T00:00:00Z)

    """
    from_currency = converter.currency_from
    to_currency = converter.currency_to
    amount = converter.amount
    date = converter.date
    if amount < 0:
        raise HTTPException(status_code=403, detail="Invalid currency amount")

    if date:
        now = utc.localize(datetime.datetime.now())
        if date > now:
            raise HTTPException(
                status_code=403, detail="Selected date must be in the past"
            )

        result = await convert_currency(from_currency, to_currency, amount, date)
        if result["status"] != "Error":
            return {
                "data": {
                    "currency_from": from_currency,
                    "currency_to": to_currency,
                    "amount": amount,
                    "result": result,
                }
            }
        else:
            result = {"stats": "Error", "message": result["message"]}
            return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        result = await convert_currency(from_currency, to_currency, amount)
        if result["status"] != "Error":
            return {
                "data": {
                    "currency_from": from_currency,
                    "currency_to": to_currency,
                    "amount": amount,
                    "result": result,
                }
            }
        else:
            result = {"stats": "Error", "message": result["message"]}
            return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
