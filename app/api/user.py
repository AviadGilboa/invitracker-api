import fastapi

from sqlalchemy.orm import Session



from .. import schemas
from ..utils import hash, oauth2
from ..db import models
from ..db.session import get_db
from ..crud import users as crud_users

router = fastapi.APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post(
    path='/',
    response_model=schemas.UserOut,
    status_code=fastapi.status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = fastapi.Depends(get_db),
):
    new_user_hash_password = hash.hash(
        password=user.password,
    )
    user.password = new_user_hash_password

    new_user = models.User(
        **user.model_dump()
    )
    return crud_users.create_user(
        db=db,
        new_user=new_user
    )



@router.get(
    path='/{id}',
    response_model=schemas.UserOut,
    status_code=fastapi.status.HTTP_200_OK,
)
def get_user_by_id(
    id: int,
    db: Session=fastapi.Depends(get_db),
    current_user: schemas.UserDetails = fastapi.Depends(oauth2.get_current_user)
):
    if current_user.id == id or current_user.role ==  models.UserRole.admin:
        user = crud_users.get_user_by_id(
            user_id=id,
            db=db,
        )

        if not user:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f'User with id: {id} does not exist',
            )
        return user
    raise fastapi.HTTPException(
        fastapi.status.HTTP_401_UNAUTHORIZED,
    )
