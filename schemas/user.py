from pydantic import Field, EmailStr, BaseModel
from typing import Optional
from models.user import User
from tortoise.contrib.pydantic import pydantic_model_creator

UserGet = pydantic_model_creator(User, name='User')


class UserPost(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password_hash: str = Field(alias='password', min_length=8, max_length=20)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
