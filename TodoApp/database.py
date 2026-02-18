from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing_extensions import Annotated
from sqlalchemy.orm import Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# SQLALCHEMY_DATABASE_URL="postgresql://api_user:strongpassword@localhost:5432/fastapi"

# engine=create_engine(SQLALCHEMY_DATABASE_URL)

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()
 
def get_db() :
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For connection pulling
dp_dependency= Annotated[Session, Depends(get_db)]