from fastapi import APIRouter, status, Depends

from services.user import get_user_service, UserService
from .schemas import User, UserData, Token


router = APIRouter()


@router.post(
    '/registration',
    description='Create new user',
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
async def create_user(
    body: UserData,
    user_service: UserService = Depends(get_user_service)
) -> User:
    new_user, token_ = await user_service.create_user(body.login, body.password)
    user = User.parse_obj(new_user.__dict__)
    user.access_token = token_['access_token']
    return user


@router.post(
    '/get-token',
    description='Refresh or get new token',
    status_code=status.HTTP_200_OK,
    response_model=User
)
async def get_token(
    body: UserData,
    user_service: UserService = Depends(get_user_service)
) -> User:
    userdata, token_ = await user_service.get_jwt(body.login, body.password)
    if userdata:
        user = User.parse_obj(userdata.__dict__)
        user.access_token = token_['access_token']
        return user
    return status.HTTP_403_FORBIDDEN


@router.post(
    '/check-token',
    description='Refresh or get new token',
    status_code=status.HTTP_200_OK
)
async def check_token(
    body: Token,
    user_service: UserService = Depends(get_user_service)
):
    if await user_service.check_token(body.access_token):
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
