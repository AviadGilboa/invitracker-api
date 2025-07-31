import datetime
import pydantic

from typing import Optional

from .db.models import UserRole
class UserCreate(
    pydantic.BaseModel,
):
    full_name: str
    email: pydantic.EmailStr
    password: str
    phone_number: str


class UserOut(
    pydantic.BaseModel,
):
    id: int
    full_name: str
    email: pydantic.EmailStr
    phone_number: str    

class UserDetails(
    UserOut
):
    role: UserRole
class UserLogin(
    pydantic.BaseModel
):
    email: pydantic.EmailStr
    password: str

class Token(
    pydantic.BaseModel,
):
    access_token: str
    token_type: str

class TokenData(
    pydantic.BaseModel,
):
    id: Optional[int] = None

class Event(
    pydantic.BaseModel,
):
    title: str
    date: datetime.datetime
    location: str
    photo_path: Optional[str] = None
    custom_message: Optional[str] = None
    
class EventOut(
    Event,
):
    id: int

class EventUpdate(
    pydantic.BaseModel,
):
    title: str = None
    date: datetime.datetime = None
    location: str = None
    photo_path: Optional[str] = None
    custom_message: Optional[str] = None
    