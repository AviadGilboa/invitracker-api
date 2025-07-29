import fastapi
import fastapi.dependencies
import sqlalchemy
import sqlalchemy.orm

from ..db import models, session

def get_user_by_id(
    user_id: int,
    db: sqlalchemy.orm.Session,
):
    return db.get(
        entity=models.User,
        ident=user_id,
    )
