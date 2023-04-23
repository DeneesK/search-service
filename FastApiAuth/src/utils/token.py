import time

import jwt

from core.config import app_settings


def get_access_token(user_id: str) -> dict:
    time_now = time.time()
    payload = {'id': user_id}
    payload.update(
        {
            'exp': time_now + app_settings.token_ttl,
            'iat': time_now - 10,
        }
    )
    jwt_ = jwt.encode(
        payload,
        app_settings.secret_key,
        algorithm='HS256',
    )
    return {'access_token': jwt_}
