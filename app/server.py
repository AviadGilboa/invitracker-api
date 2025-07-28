import fastapi

from sqlalchemy.orm import Session

from .db import models, session

from .api import user
from . import schemas




app = fastapi.FastAPI()

models.Base.metadata.create_all(
    bind=session.engine
)

app.include_router(
    router=user.router
)

@app.get('/')
def root():
    return {'message': 'Hello from Invite-Tracker app'}
