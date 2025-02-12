import zoneinfo
import time
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from db import create_all_tables
from models import Invoice
from .routers import customers, transactions, plans



# Start the FastAPI class and create the tables for the database
app = FastAPI(lifespan=create_all_tables)

# API Routers
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)



# Middleware example
# Print in the console the time it takes to complete the request in seconds
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request completed in: {process_time:.4f} seconds")
    return response


# First endpoint created to test the API concept
@app.get("/")  # http://localhost:8000/
async def root():
    return {"message": "Hi from the API"}


# Example to test the API concept by modifying the URL
country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}

@app.get("/time/{iso_code}")  # hosturl/time/{iso_code_from_country_timezones}
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if not timezone_str:
        raise HTTPException(status_code=400, detail="Invalid ISO country code")

    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz).isoformat()}



# Invoice endpoint =======================================================================================================
@app.post("/invoices")
async def create_customer(invoice_data: Invoice):
    return invoice_data