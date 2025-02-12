from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select
from models import Transaction, TransactionCreate, Customer
from db import SessionDep


router = APIRouter()

# ==>> Endpoints related to transactions <==



# Create a new transaction
@router.post("/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep) -> Transaction:
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )

    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db



# List transactions (with optional filtering by customer_id)
@router.get("/transactions", tags=["transactions"])
async def list_transactions(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Número de registros"),
    customer_id: int | None = Query(None, description="Filtrar por ID de cliente"),
) -> list[Transaction]:
    query = select(Transaction)
    if customer_id:
        query = query.where(Transaction.customer_id == customer_id)

    transactions = session.exec(query.offset(skip).limit(limit)).all()
    return transactions
