import fastapi
import fastapi.dependencies
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm

from .. import schemas
from ..db import models

from . import event_owners as crud_event_owners

def create_event(
    db: sqlalchemy.orm.Session,
    new_event: models.Event,
):
    db.add(
        instance=new_event,
    )
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail=f'Problem Creating Event\n {e}'
        )
    db.refresh(new_event)
    return new_event


def get_event_by_id(
    db: sqlalchemy.orm.Session,
    event_id: int,
) -> models.Event:
    result = db.get(
        entity=models.Event,
        ident=event_id,
    )
    if not result:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f'Event ID Not Exist',
        )
    return result

def change_event_data(
    db: sqlalchemy.orm.Session,
    event_update_details: schemas.EventUpdate,
    event_id: int,
    user_id: int
):
    current_event = get_event_by_id(
        db=db,
        event_id=event_id,
    )
    current_event.updated_by = user_id
    current_event.updated_at = sqlalchemy.func.now()
    
    update_data = event_update_details.model_dump(exclude_none=True).items()
    for key, value in update_data:
        setattr(
            current_event,
            key,
            value
        )
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail=f'Problem patching Event\n {e}'
        )
    db.refresh(current_event)
    return current_event

def get_all_event_by_user_id(
    db: sqlalchemy.orm.Session,
    user_id: int,
):
    user_event_ids: list[int] = crud_event_owners.get_all_event_id_by_user_id(
        db=db,
        user_id=user_id,
    )
    result: list[schemas.EventOut] = []
    for event_id in user_event_ids:
        result.append(
            get_event_by_id(
                db=db,
                event_id=event_id
            ),
        )
    return result
