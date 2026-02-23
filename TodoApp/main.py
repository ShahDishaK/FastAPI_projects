from fastapi import FastAPI

from TodoApp.routers import auth, todos, admin
app = FastAPI()

@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
