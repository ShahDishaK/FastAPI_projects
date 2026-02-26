from fastapi import FastAPI, Request,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from routers import auth, todos, admin
from core.templates import templates
from fastapi.responses import RedirectResponse


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)