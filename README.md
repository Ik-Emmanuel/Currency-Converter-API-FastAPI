# Currency-Converter-API-FastAPI 
This API is built with FastAPI, sqlmodel and sqlite database. It helps with currency conversion from one available currency type to another with access to historical currency conversion too

## EXTERNAL SERVICES 
- Currency API endpoint : https://apilayer.com/marketplace/fixer-api
- Currency symbols endpoint: https://api.apilayer.com/fixer/symbols
- Currency rate with USD baseline: https://api.apilayer.com/fixer/latest?&base=USD

## ENDPOINTS
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *GET* | ```/``` | _Home_| _All users_|
| *GET* | ```/docs/``` | _API documentation_| _All users_|
| *POST* | ```/auth/registration/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_| _All users_|
| *GET* | ```/auth/me/``` | _Fetch user profile_|_Authenticated users only_|
| *POST* | ```/convert/``` | _Convert Currencies_|_Authenticated users only_|
| *GET* | ```/symbols``` | _Fetch available currencies_|_Authenticated users only_|

# USER AUTHENTICATION 
- JWT  with Bearer Token used for user authentication 

# DATABASE
- SQLite database is used

# HOW TO RUN
- pip install requirements.txt file to install dependencies 
- run command:  uvicorn main:app --reload

# SUGGESTIONS
- After initial start-up, you could comment out start up event functions: `create_db_tables()` and `fetch_data()` to prevent fetching data multiple times from external service and only run when needed
