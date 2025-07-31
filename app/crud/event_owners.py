import fastapi
import fastapi.dependencies
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm

from . import events

from .. import schemas
from ..db import models

def get_all_event_id_by_user_id(
    db: sqlalchemy.orm.Session,
    user_id: int,
) -> list[int]:
    select_all_events_by_user = sqlalchemy.select(
        models.Event_Owners.event_id,
    ).where(
        models.Event_Owners.user_id == user_id,
    )
    return db.execute(
        statement=select_all_events_by_user,
    ).scalars().all()

def create_event_owners(
    db: sqlalchemy.orm.Session,
    new_event_owner: models.Event_Owners,
) -> models.Event_Owners:
    db.add(
        instance=new_event_owner,
    )
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail='Problem Creating Event'
        )
    db.refresh(new_event_owner)
    return new_event_owner

def validate_event_owner(
    db: sqlalchemy.orm.Session,
    event_id: int,
    user_id: int
) -> bool:
    stmt_check_event_user = (
        sqlalchemy.select(
            1
        )
        .select_from(models.Event_Owners)
        .where(
            models.Event_Owners.event_id == event_id,
            models.Event_Owners.user_id == user_id,
        )
    )
    result = db.execute(
        statement=stmt_check_event_user
    ).scalar()
    if not result:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail=f'''You don't have pressions manage this event'''
        )
    return True
