from distutils.log import error
from fastapi import FastAPI
# from src.app.users.controller import router
# from src.app.scraps.controller import scraps_router
from settings import load_apps, APPS

app_modules = load_apps(APPS)
app = FastAPI()
for single_app in app_modules:
    app.include_router(single_app)
# app.include_router(router)
# app.include_router(scraps_router)
