# fastapi-transactions-management

This project is an API built with FastAPI and SQLModel for managing transactions and customers.
It allows transaction registration, transaction listing, and customer management.


# Features
  - Full CRUD operations for transactions and customers
  - Data validation with Pydantic
  - SQLModel for database interaction
  - Modular routing with APIRouter
  - Automatic API documentation with Swagger UI and ReDoc


# Prerequisites
Before starting, make sure you have installed:
	- Python 3.10 or higher
	- Git (optional)


# Installation
  1. Clone the repository (bash):
    git clone <repository-url>
		cd <repository-folder>

  2. Create and activate a virtual environment:
   		On Windows (PowerShell):
			  python -m venv your_virtual_env
			  your_virtual_env\Scripts\activate

   		On macOS/Linux:
			  python -m venv your_virtual_env
			  source your_virtual_env/bin/activate

  3. Install dependencies:
    pip install -r requirements.txt


# Run the API
Start the FastAPI server:
	uvicorn app.main:app --reload


# Access the interactive documentation at:
  - Swagger UI: http://127.0.0.1:8000/docs
	- ReDoc: http://127.0.0.1:8000/redoc
