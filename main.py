from distutils.log import error
from fastapi import FastAPI
from src.app.users.controller import user_router
from src.app.scraps.controller import scraps_router

app = FastAPI()

app.include_router(user_router)
app.include_router(scraps_router)
