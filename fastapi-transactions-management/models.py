from pydantic import BaseModel, EmailStr
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship, select
from enum import Enum
from db import Session, engine



# Enum defines a set of constant values with readable names, useful for fixed options.
class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"



# Plan section ==========================================================================================================
# Intermediate table to link customers and plans
class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)  # Field represents a database column.
    plan_id: int = Field(foreign_key="plan.id")  # Foreign key to Plan table.
    customer_id: int = Field(foreign_key="customer.id")  # Foreign key to Customer table.
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)  # Default status is ACTIVE.

# Plan model representing a subscription plan
class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list['Customer'] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )  # Defines a many-to-many relationship with customers.



# Customer section ======================================================================================================
class CustomerBase(SQLModel):  # Base model without a database table, only attributes.
    name: str
    description: str | None = None  # Allows null values.
    email: EmailStr = Field(default=None)
    age: int

    # Validator to check if an email already exists in the database
    @field_validator("email")  # Specifies that the 'email' field is being validated.
    @classmethod
    def validate_email(cls, value):  # 'cls' refers to the class that calls the method (CustomerBase).
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()  # Retrieves the first match, returns None if not found.
        if result:  # If a match is found, raise an error because the email is already in use.
            raise ValueError("This email is already registered")
        return value

# Models for creating and updating customers (inherit from CustomerBase)
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

# Customer model representing a database table
class Customer(CustomerBase, table=True):  # Inherits from CustomerBase and creates a database table.
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )  # Many-to-many relationship with plans.



# Transaction section ===================================================================================================
class TransactionBase(SQLModel):
    amount: int  # Fixed typo: 'ammount' -> 'amount'
    description: str

# Transaction model representing a database table
class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

# Model for creating transactions (does not need a foreign key)
class TransactionCreate(TransactionBase):
    customer_id: int  # Removed Field(foreign_key), not needed in input models.



# Invoice section =======================================================================================================
class Invoice(BaseModel):  # Not a database table, just a response model.
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self):  # Fixed typo: 'ammount_total' -> 'amount_total'
        return sum(transaction.amount for transaction in self.transactions)  # Fixed typo: 'ammount' -> 'amount'
