from fastapi import FastAPI
from endpoints.users import user_router
from endpoints.currencies import converter_router
from endpoints.home import home_router
from create_db import create_db_tables
from populate_db import fetch_data

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Create sqlite database tables on app start up and attempts to
    fetch Currency data from API to be loaded into database"""
    create_db_tables()
    await fetch_data()


app.include_router(user_router)
app.include_router(home_router)
app.include_router(converter_router)
