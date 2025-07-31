import fastapi
import sqlalchemy

import sqlalchemy.orm

from .. import schemas
from ..utils import oauth2
from ..db import models

from ..db.session import get_db
from ..crud import events as crud_events
from ..crud import event_owners as crud_events_owners


router = fastapi.APIRouter(
    prefix='/event',
    tags=['Event']
)


@router.get(
    path='',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=list[schemas.EventOut],
)
def get_all_user_events(
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: schemas.UserDetails = fastapi.Depends(oauth2.get_current_user)
):
    user_events: list[schemas.EventOut] = crud_events.get_all_event_by_user_id(
        db=db,
        user_id=current_user.id,
    )
    return user_events


@router.get(
    path='/{event_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schemas.EventOut,
)
def get_event(
    event_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: schemas.UserDetails = fastapi.Depends(oauth2.get_current_user)
):
    if crud_events_owners.validate_event_owner(
        db=db,
        event_id=event_id,
        user_id=current_user.id,
    ):
        return crud_events.get_event_by_id(
            db=db,
            event_id=event_id,
        )


@router.post(
    path='',
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=schemas.EventOut,
)
def create_event(
    event_details: schemas.Event,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: schemas.UserDetails = fastapi.Depends(oauth2.get_current_user)
):
    new_event = models.Event(
        **event_details.model_dump(),
        created_by=current_user.id,
    ) 
    event = crud_events.create_event(
        new_event=new_event,
        db=db,
    )
    new_event_owner: models.Event_Owners = models.Event_Owners(
        event_id=event.id,
        user_id=current_user.id,
    )
    crud_events_owners.create_event_owners(
        new_event_owner=new_event_owner,
        db=db,
    )
    return event

@router.patch(
    path='/{event_id}',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schemas.EventOut,
)
def update_event(
    event_id: int,
    event_update_details: schemas.EventUpdate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: schemas.UserDetails = fastapi.Depends(oauth2.get_current_user)
):
    is_there_field_to_update = len(event_update_details.model_dump(exclude_none=True)) > 0
    if is_there_field_to_update:
        crud_events_owners.validate_event_owner(
            db=db,
            event_id=event_id,
            user_id=current_user.id,
        )
        event_after_change = crud_events.change_event_data(
            db=db,
            event_id=event_id,
            event_update_details=event_update_details,
            user_id=current_user.id,
        )
        
        return event_after_change
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=f'No data To Update'
    )
