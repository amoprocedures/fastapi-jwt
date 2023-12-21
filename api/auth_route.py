from fastapi.routing import APIRouter
from config.auth import verified_user, authorize, pwd_context, create_access_jwt, create_refresh_jwt
from schemas.user import User, UserGet, UserPost, UserLogin
from fastapi import Depends, status, HTTPException

auth_router = APIRouter(prefix='/api/v1', tags=['AUTH'])


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(body: UserPost):
    # encrypt password
    body.password_hash = pwd_context.hash(body.password_hash)
    # turn play_load into dict
    data = body.model_dump(by_alias=False, exclude_unset=True)
    # check if email is taken
    existing = await User.filter(email=body.email).exists()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="email already taken"
        )
    # create the user
    user_obj = await User.create(**data)
    # return created user
    user = await UserGet.from_tortoise_orm(user_obj)
    # get the created user:id
    user_id = user.model_dump()['id']
    return user_id


@auth_router.post('/login')
async def login(body: UserLogin):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='wrong credentials'
    )
    # check if email exists
    user = await User.filter(email=body.email).first()
    if not user:
        raise error
    # check if password matches
    matches = pwd_context.verify(body.password, user.password_hash)
    if not matches:
        raise error
    # create jwt access token
    data = {'user_name': user.email}
    access_tkn = create_access_jwt(data)
    # create jwt refresh token
    refresh_tkn = create_refresh_jwt(data)
    # store the refresh token in memory||database|| any storage
    # in my case I am storing in users-table
    await User.filter(email=body.email).update(**{'refresh_token': refresh_tkn})

    return {
        'message': 'Login Successful',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'access_token': access_tkn,
        'refresh_token': refresh_tkn,
        'type': 'bearer'
    }


@auth_router.post('/refresh_token')
async def refresh(token_data: dict = Depends(authorize)):
    return token_data


@auth_router.get('/data')
async def protected_data(user: User = Depends(verified_user)):
    return {'status': 'authorized', 'email': user.email}
