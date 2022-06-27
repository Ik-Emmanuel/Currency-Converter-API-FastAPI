from fastapi import APIRouter, Depends
from auth.auth import AuthHandler
from db.db import session
from sqlmodel import select
from models.currency_models import CurrencySymbol

home_router = APIRouter()
auth_handler = AuthHandler()


@home_router.get("/", tags=["Home Page"])
def home():
    response = {
        "status": "success",
        "message": "Welcome to I.K Emmanuel's currency converter 😊. \
            Visit: '/docs' to get started with the documentation",
    }
    return response


@home_router.get("/symbols", tags=["Get Available Currencies"])
def get_available_currencies(user=Depends(auth_handler.get_current_user)):
    currencies = select(CurrencySymbol)
    currencies = session.exec(currencies).all()
    return {"Available_currencies": currencies}
