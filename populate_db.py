from sqlmodel import Session, select
from db.db import engine
from models.currency_models import CurrencyRate, CurrencySymbol
import datetime
import asyncio
import requests
from collections import defaultdict
import os 
from dotenv import load_dotenv


env_file = os.path.join(".env")
load_dotenv(env_file)


####################################### API CALL TO  FETCH NEW DATA ######################################


JSON = int or str or float or bool or None or dict[str, "JSON"] or list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


def http_get_sync(url: str, headers: dict) -> JSONObject:
    """This function is used to make api request given a url and header configuration"""
    response = requests.get(url, headers=headers)
    return response.json()


async def http_get(url: str, headers: dict) -> JSONObject:
    """This function allows for asynchronous API calls"""
    return await asyncio.to_thread(http_get_sync, url, headers)


async def get_symbols(url:str, header:str) -> dict:
    """This function makes an api call to fetch currency available currency symbols""" 
    currency_symbols = await http_get(url, header)
    results = defaultdict(None)
    results["status"] = currency_symbols["success"]
    try:
        results["symbols"] = currency_symbols["symbols"]
    except Exception as e:
        results["symbols"] = None
    return results


async def get_exchange_rates(url:str, header:str) -> dict: 
    """This function makes an api call to fetch current exchange rates using USD as base currency from an API endpoint""" 
    exchange_rates = await http_get(url, header)
    results = defaultdict(None)
    results["status"] = exchange_rates["success"]
    try:
        results["date"] = exchange_rates["date"]
        results["rates"] = exchange_rates["rates"]
    except Exception as e:
        results["date"] = None
        results["rates"] = None
  
    return results

async def get_rates_and_symbols() -> str:
    """Fetch currency data from external service"""
    api_key = os.environ["API_KEY"]
    symbols_endpoint = "https://api.apilayer.com/fixer/symbols"
    rates_endpoint = "https://api.apilayer.com/fixer/latest?&base=USD"
    header = {"apikey": api_key }
    symbols_results, exchange_rates_results = await asyncio.gather(get_symbols(symbols_endpoint, header), get_exchange_rates(rates_endpoint, header))
    return symbols_results, exchange_rates_results



def create_symbol(symbol: str,  name:str):
    """ This function returns a Currency symbol sqlmodel object """
    name = name
    symbol = symbol
    currency_symbol = CurrencySymbol(name=name, symbol=symbol)
    return currency_symbol


def create_exchange_rate(symbol: str, rate:float, date:str):
    """ This function returns an exchange rate sqlmodel object """
    symbol = symbol
    rate= rate
    date= date
    exchange_rate = CurrencyRate(symbol=symbol, exchange_date=date, exchange_rate=rate)
    return exchange_rate



async def fetch_data() -> None:
    """ Fetch currency data and check for updates before writing data into database"""
    symbols_results, exchange_rates_results = await get_rates_and_symbols()
    print("***** CREATING DATA ENTRIES *****")
    symbols = []
    exchange_rates = []
    if symbols_results["status"]== True:
        currency_symbols = symbols_results["symbols"]
        with Session(engine) as session:
            statement = select(CurrencySymbol)
            res = session.exec(statement).all()
            length = len(res)
            existing_symbols = [res[i].symbol for i in range(length)]  
        symbols = [create_symbol(i, currency_symbols[i]) for i in currency_symbols if i not in existing_symbols]

    if exchange_rates_results["status"] ==  True:
        currency_rates = exchange_rates_results["rates"]
        date = exchange_rates_results["date"]
        with Session(engine) as session:
            format = '%Y-%m-%d'
            date = datetime.datetime.strptime(date, format)
            statement = select(CurrencyRate).where(CurrencyRate.exchange_date == date )
            date_entry = session.exec(statement).first()
            if not date_entry:
                exchange_rates = [create_exchange_rate(i, currency_rates[i], date) for i in currency_rates]
            else:
                exchange_rates = []
        
    
    with Session(engine) as session:
        if symbols:
            session.add_all(symbols)
            print(" *** Currency symbols data written to db ***\n")
        if exchange_rates:
            session.add_all(exchange_rates)
            print(" ***  Exchange rates data written to db ***\n")
        if symbols or exchange_rates:             
            session.commit()
        else:
            print("\n\n **************     *************   *************** ")
            print("No data was written to database. Either no new currency record found, or there was a possible error during data fetch")
    print("Data Load Service Complete!")





