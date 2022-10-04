from distutils.log import error
from fastapi import FastAPI
from settings import load_apps, APPS
from fastapi.middleware.cors import CORSMiddleware

app_modules = load_apps(APPS)
app = FastAPI()
# MIDDLEWARES 
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for single_app in app_modules:
    app.include_router(single_app)
# app.include_router(router)
# app.include_router(scraps_router)
