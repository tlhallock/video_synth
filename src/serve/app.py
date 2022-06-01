
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
from serve.routes import things


app = FastAPI(
    title=settings.title
)
app.middleware("http")(request_handler)


app.include_router(projects.router)
app.include_router(videos.router)
app.include_router(things.router)

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

"""


alias r="python -m cli"

r project list
r project list -o yaml
r project list -o csv

r project create newone

r project delete c8390251-f09c-4275-ae2c-372bdb70beb6


r things list
r things list -p 115
r things create -f example_thing.yaml -e
r thing delete 1e80a2 


"""