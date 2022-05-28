
'''
https://github.com/David-Lor/FastAPI-Pydantic-Mongo_Sample_CRUD_API/tree/master/people_api
'''

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from serve.middlewares import request_handler
from serve.cfg import api_settings as settings
from serve.routes import projects
from serve.routes import videos


app = FastAPI(
    title=settings.title
)
app.middleware("http")(request_handler)


app.include_router(projects.router)
app.include_router(videos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run():
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )

