from passlib.context import CryptContext
from jose import jwt
from datetime import datetime
from config.settings import Config
from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordBearer
from models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/token')

error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='invalid authorization credentials'
)


def create_access_jwt(data: dict):
    data['exp'] = datetime.utcnow() + Config.JWT_ACCESS_EXP
    data['mode'] = 'access_token'
    return jwt.encode(data, Config.SECRET, Config.ALGORITHM)


def create_refresh_jwt(data: dict):
    data['exp'] = datetime.utcnow() + Config.JWT_REFRESH_EXP
    data['mode'] = 'refresh_token'
    return jwt.encode(data, Config.SECRET, Config.ALGORITHM)


async def authorize(token: str = Depends(oauth_scheme)) -> dict:
    # validate the refresh jwt token
    try:
        data = jwt.decode(token, Config.SECRET, Config.ALGORITHM)
        # check if "mode": "refresh_token"
        if 'user_name' not in data and 'mode' not in data:
            raise error
        if data['mode'] != 'refresh_token':
            raise error
        # check if user exists
        user = await User.filter(email=data['user_name']).first()
        if not user or token != user.refresh_token:
            raise error
        # generate new refresh token and update user
        data = {'user_name': user.email}
        refresh_tkn = create_refresh_jwt(data)
        await User.filter(email=user.email).update(**{'refresh_token': refresh_tkn})
        # generate new access token
        access_tkn = create_access_jwt(data)
        return {
            'access_token': access_tkn,
            'refresh_token': refresh_tkn,
            'type': 'bearer'
        }
    except JWTError:
        raise error


async def verified_user(token: str = Depends(oauth_scheme)) -> User:
    # validate the access jwt token
    try:
        data = jwt.decode(token, Config.SECRET, Config.ALGORITHM)
        # check if "mode": "refresh_token"
        if 'user_name' not in data and 'mode' not in data:
            raise error
        if data['mode'] != 'access_token':
            raise error
        # check if user exists
        user = await User.filter(email=data['user_name']).first()
        if not user:
            raise error

        return user
    except JWTError:
        raise error
