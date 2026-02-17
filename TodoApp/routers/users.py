from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from models import Todos
from .auth import get_current_user
from database import dp_dependency
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from models import Users


router=APIRouter(
    prefix='/admin',
    tags=['admin']
)

SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')


user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/get_user/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:dp_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Todos).all()

@router.put("/change_password",status_code=status.HTTP_200_OK)
async def change_password(user:user_dependency,db:dp_dependency,new_password:str):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.hashed_password=bcrypt_context.hash(new_password)
    db.commit()

