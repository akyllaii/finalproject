CloudShop AI 
About the project
This is a simple cloud e-commerce API made with FastAPI.
It has users, products, and orders. It also has login system, database, logs, and simple AI that detects suspicious activity.


Tech used
FastAPI (backend)
PostgreSQL (Supabase database)
JWT (login system)
scikit-learn (AI part)
pytest (tests)

How it works
User can:
register and login
add and view products
create orders
Every request is saved in logs.
Then AI reads logs and checks if activity is normal or suspicious.


How it works
User can:
register and login
add and view products
create orders
Every request is saved in logs.
Then AI reads logs and checks if activity is normal or suspicious.


API Endpoints
Users
POST /register - create user
POST /login - login and get token


Products
GET /products - get all products
POST /products - create product
PUT /products/{id} - update product
DELETE /products/{id} - delete product

 Orders
POST /orders - create order

AI / Security
GET /threat-report - checks logs and returns:
normal
suspicious


Logs
All requests are saved in:
logs/app.log
Example:
{"time": "2026-05-11 14:41:48.414688", "method": "GET", "path": "/threat-report", "status": 200, "ip": "127.0.0.1"}


AI part
AI uses simple machine learning (scikit-learn).
It checks:
failed logins (401)
unknown pages (404)
too many requests from same IP
Then it decides if user is normal or suspicious.


How to run
pip install -r requirements.txt
uvicorn app.main:app --reload
Open:
http://127.0.0.1:8000/docs



Database
I used Supabase (cloud PostgreSQL) to store users, products and orders.

Notes
This project shows:
backend API
database connection
authentication
logging system
simple AI detection