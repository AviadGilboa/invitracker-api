import fastapi
import sqlalchemy

import sqlalchemy.orm

from .. import schemas
from ..utils import hash, oauth2
from ..db import models
from ..db.session import get_db
from ..crud import users as crud_users


router = fastapi.APIRouter(
    prefix='/login',
    tags=['Login']
)

@router.post(
    path='',
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schemas.Token,
)
def login(
    user_credentials: schemas.UserLogin,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db)
):
    user = crud_users.find_user_by_email(
        user_email=user_credentials.email,
        db=db,
    )
    if user is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail=f'Credentials not valid'
        )

    is_password_match = hash.verify(
        plain_password=user_credentials.password,
        hashed_password=user.password
    )

    if not is_password_match:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail=f'Credentials not valid'
        )
    access_token = oauth2.create_access_token(
        token_data= {
            'user_id': user.id,
        }
    )

    return {
        'token_type': 'Bearer',
        'access_token': access_token,
    }
