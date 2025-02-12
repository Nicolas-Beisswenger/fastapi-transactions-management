from fastapi import APIRouter  # It's like a mini FastAPI app for defining routes
from fastapi import status, HTTPException, Query
from sqlmodel import select  # Allows making SELECT queries to the database
from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from db import SessionDep # Importing session dependency to interact with the database



router = APIRouter()  # Instead of '@app = FastAPI', use this for defining routes.

# ==>> Endpoints related to customers <==



# Create a new customer
@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())  # Validates the input data
    session.add(customer)  # Adds the customer to the session (in memory)
    session.commit()  # Executes the SQL command to save the customer to the DB
    session.refresh(customer)  # Refreshes the local variable with updated data from the DB
    return customer  # Returns the created customer



# List all customers
@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()  # Executes the SELECT query to get all customers



# Get a customer by ID
@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(session: SessionDep, customer_id: int):
    customer_db = session.get(Customer, customer_id)  # Retrieves the customer from the DB by ID
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist")  # Returns 404 if not found
    return customer_db  # Returns the found customer



# Delete a customer
@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(session: SessionDep, customer_id: int):
    customer_db = session.get(Customer, customer_id)  # Retrieves the customer from the DB by ID
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist")
    session.delete(customer_db)  # Marks the customer for deletion
    session.commit()  # Executes the DELETE query to remove the customer from the DB
    return {"detail": "Executed"}  # Returns a confirmation message



# Update customer data
@router.patch(
        "/customers/{customer_id}", 
        response_model=Customer,  # Specifies the model to be returned as a response
        status_code=status.HTTP_201_CREATED,
        tags=["customers"]
    )
async def update_customer(session: SessionDep, customer_data: CustomerUpdate, customer_id: int):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist") 
    customer_data_dict = customer_data.model_dump(exclude_unset=True)  # Only updates the fields that were changed
    
    # Checking for changes and keeping existing values for non-modified fields
    if customer_data_dict['name'] == "string":
        customer_data_dict['name'] = customer_db.name
    
    if customer_data_dict['description'] == "string":
        customer_data_dict['description'] = customer_db.description
    
    if customer_data_dict['email'] == "string":
        customer_data_dict['email'] = customer_db.email
    
    if customer_data_dict['age'] == 0:
        customer_data_dict['age'] = customer_db.age
    
    customer_db.sqlmodel_update(customer_data_dict)  # Updates the customer with new data
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db  # Returns the updated customer



# Subscribe a customer to a plan
@router.post("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: SessionDep, 
    plan_status: StatusEnum = Query()  # Allows only values defined in StatusEnum for status query parameter
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The customer or plan does not exist")
    
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)

    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db  # Returns the created customer-plan subscription



# Get all plans a customer is subscribed to
@router.get("/customers/{customer_id}/plans")
async def get_customer_plans(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist")
    
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )  # Queries the CustomerPlan table to find the customer's subscriptions with the given status
    plans = session.exec(query).all()  # Executes the query and retrieves all matching plans
    
    return plans  # Returns the list of plans the customer is subscribed to
