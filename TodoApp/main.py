from fastapi import FastAPI

import DataBase.models as models
from DataBase.DB import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
