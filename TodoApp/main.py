from fastapi import FastAPI
import uvicorn

import DataBase.models as models
from DataBase.DB import engine
from routers.todo import todo


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(todo)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
