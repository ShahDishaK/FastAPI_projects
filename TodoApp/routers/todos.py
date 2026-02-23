from fastapi import Depends, APIRouter, HTTPException, Path
# from database import dp_dependency
from TodoApp.database import dp_dependency
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from TodoApp.models import Todos
# from models import Todos
from starlette import status
from pydantic import BaseModel, Field
from TodoApp.routers.auth import get_current_user
from typing import List


router=APIRouter()
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int

    # class Config:
    #     orm_mode = True

user_dependency = Annotated[dict, Depends(get_current_user)]
class TodoRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(min_length=3,max_length=100)
    priority:int=Field(gt=0,lt=6)
    complete:bool


@router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def readAll(user:user_dependency, db:dp_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Todo not found')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()


@router.get("/todo/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def readTodo(user:user_dependency,db:dp_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model= db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model 
    raise HTTPException(status_code=404,detail="Todo not found")


@router.post("/todo", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def createTodo(user:user_dependency,db:dp_dependency,todo_request:TodoRequest):

    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model=Todos(**todo_request.dict(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(user:user_dependency,db:dp_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.add(todo_model)
    db.commit()



@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user:user_dependency,db:dp_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()
