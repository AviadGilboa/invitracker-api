import fastapi
import fastapi.dependencies
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm

from ..db import models
from .. import schemas

def get_user_by_id(
    user_id: int,
    db: sqlalchemy.orm.Session,
):
    return db.get(
        entity=models.User,
        ident=user_id,
    )

def find_user_by_email(
    user_email: str,
    db: sqlalchemy.orm.Session,
):
    stmt_find_user_by_email = sqlalchemy.select(
        models.User,
    ).where(
        models.User.email == user_email,
    )
    return db.scalars(stmt_find_user_by_email).one_or_none()
    
def create_user(
    db: sqlalchemy.orm.Session,
    new_user: models.User,
):
    db.add(
        instance=new_user,
    )
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail='User Already Exist'
        )
    db.refresh(new_user)
    return new_user
