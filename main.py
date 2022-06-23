from fastapi import FastAPI
from db.db import session
from endpoints.users import user_router
from endpoints.currencies import converter_router
from fastapi import  Depends
from endpoints.users import auth_handler
from sqlmodel import select
from models.currency_models import CurrencySymbol
from create_db import create_db_tables
from populate_db import fetch_data


app = FastAPI() 


@app.on_event("startup")
async def startup_event():
    """ Create sqlite database tables on app start up and attempts to fetch Currency data from API to be loaded into database"""
    create_db_tables()
    await fetch_data()


@app.get('/', tags=["Home Page"])
def home():
    response ={"status": "success", 
    "message": "Welcome to I.K Emmanuel's currency converter 😊. Visit: '/docs' to get started with the documentation",}
    return response

app.include_router(user_router)

@app.get('/symbols', tags=["Get Available Currencies"])
def get_available_currencies(user = Depends(auth_handler.get_current_user)):
    currencies = select(CurrencySymbol)
    currencies = session.exec(currencies).all()
    return {'Available_currencies': currencies}


app.include_router(converter_router)