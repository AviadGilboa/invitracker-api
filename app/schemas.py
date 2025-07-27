import pydantic

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