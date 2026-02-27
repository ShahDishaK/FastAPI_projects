from multiprocessing.dummy import connection

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from TodoApp.database import Base
from TodoApp.main import app
from TodoApp.models import Todos,Users
from fastapi.testclient import TestClient
import pytest 
from sqlalchemy import  create_engine, text
from TodoApp.routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"


engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)


TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username':'admin','id':1,'user_role':'admin'}



client=TestClient(app)



@pytest.fixture
def test_todo():
    todo=Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        # connection.execute(text("DELETE FROM sqlite_sequence WHERE name='todos'"))  # reset autoincrement
        connection.commit()





@pytest.fixture
def test_user():
    user=Users(
        username='admin',
        email='admin123@gmail.com',
        first_name='abc',
        last_name='xyz',
        hashed_password=bcrypt_context.hash('admin'),
        role='admin',
    )
    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()