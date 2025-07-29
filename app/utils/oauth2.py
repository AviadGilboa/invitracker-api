import fastapi
import fastapi.security
import jwt
import sqlalchemy
import sqlalchemy.orm

from datetime import datetime, timedelta, timezone

from ..configuration.setting import settings
from ..crud import users as crud_users
from ..db import models, session
from .. import schemas 


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(
    token_data: dict,
):
    data_to_encode = token_data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data_to_encode.update(
        {
            'exp': expire
        }
    )

    encoded_jwt = jwt.encode(
        data_to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(
    token:str,
    credentials_exception: fastapi.HTTPException,
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')

        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(
            id=user_id,
        )
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception

    return token_data

def get_current_user(
    token: str = fastapi.Depends(fastapi.security.OAuth2PasswordBearer(tokenUrl='login')),
    db: sqlalchemy.orm.Session = fastapi.Depends(session.get_db),
):

    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    token_data = verify_access_token(
        token=token,
        credentials_exception=credentials_exception,
    )
    return crud_users.get_user_by_id(
        user_id=token_data.id,
        db=db,
    )
    
    
