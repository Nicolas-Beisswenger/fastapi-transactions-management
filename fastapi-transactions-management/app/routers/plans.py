from fastapi import APIRouter
from fastapi import status, HTTPException
from sqlmodel import select
from models import Transaction, TransactionCreate, Customer, Plan
from db import SessionDep  # Importing session dependency to interact with the database


router = APIRouter()

# ==>> Endpoints related to plans <==



# Create a new plan
@router.post("/plans", tags=["plans"])
async def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())  # Validates and prepares the plan data
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db  # Returns the newly created plan



# List all plans
@router.get("/plans", response_model=list[Plan], tags=["plans"])
async def list_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans  # Returns the list of plans
