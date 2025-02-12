from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Depends
from fastapi import FastAPI



# SQLite connection
sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"  # The three '/' indicate a local path.


# Create a database connection using the 'engine' variable.
engine = create_engine(sqlite_url)


# Function to create all tables in the database
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


# Function to get a database session
def get_session():
    with Session(engine) as session:  # Opens a session connected to the database engine.
        yield session  # Returns the active session to perform operations.


# Dependency injection for database session
SessionDep = Annotated[Session, Depends(get_session)]
