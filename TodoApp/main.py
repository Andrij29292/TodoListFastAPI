from fastapi import FastAPI
import uvicorn

import DataBase.models as models
from DataBase.DB import engine
from routers import todo, auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(todo.router, prefix="/todos", tags=["Todo list"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
