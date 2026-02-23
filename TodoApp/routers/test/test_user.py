from TodoApp.routers.test.utils import *
from TodoApp.routers.admin import get_current_user
from TodoApp.database import get_db
from fastapi import status


app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user



def test_return_user(test_user):
    response=client.get("/users/")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()['username']=='admin'
    assert response.json()['email']=='admin123@gmail.com'
    assert response.json()['first_name']=='abc'
    assert response.json()['last_name']=='xyz'
    assert response.json()['role']=='admin'



def test_change_password_success(test_user):
    response=client.put("/users/change_password/",json={"hashed_password":"admin","new_password":"admin2"})

    assert response.status_code==status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response=client.put("/users/change_password/",json={"hashed_password":"admin3","new_password":"admin2"})

    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':"Password not changed"}


