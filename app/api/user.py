import fastapi

from sqlalchemy.orm import Session

from .. import schemas
from ..db import models
from ..db.session import get_db

router = fastapi.APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post(
    path='/',
    status_code=fastapi.status.HTTP_201_CREATED,
    # response_model=schemas.UserOut,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = fastapi.Depends(get_db),
):
    new_user = models.User(
        **user.model_dump()
    )
    db.add(
        instance=new_user,
    )
    db.commit()
    db.refresh(new_user)
    return new_user