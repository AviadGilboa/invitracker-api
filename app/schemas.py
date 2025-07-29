import pydantic

from typing import Optional

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
    
class UserLogin(
    pydantic.BaseModel
):
    email: pydantic.EmailStr
    password: str

class Token(
    pydantic.BaseModel
):
    access_token: str
    token_type: str

class TokenData(
    pydantic.BaseModel
):
    id: Optional[int] = None
    role: Optional[str] = None
