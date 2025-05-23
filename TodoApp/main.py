from fastapi import FastAPI
import uvicorn

import DataBase.models as models
from DataBase.db import engine
from routers.business import todo
from routers.auth import auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(todo.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
