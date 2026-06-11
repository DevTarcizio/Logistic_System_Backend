from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class DriverCreate(BaseModel):
    name: str
    telephone_number: str


class DriverPublic(BaseModel):
    id: int
    name: str
    telephone_number: str

    model_config = ConfigDict(from_attributes=True)


class DriverList(BaseModel):
    drivers: list[DriverPublic]


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
