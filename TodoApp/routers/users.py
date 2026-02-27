from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from TodoApp.models import Todos,Users
from TodoApp.routers.auth import get_current_user
from TodoApp.database import dp_dependency
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field

# from models import Users


router=APIRouter(
    prefix='/users',
    tags=['users']
)

SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:dp_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()



@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user:user_dependency,
    db:dp_dependency,
    payload: ChangePasswordRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(payload.current_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Password not changed")

    user_model.hashed_password = bcrypt_context.hash(payload.new_password)
    db.commit()
