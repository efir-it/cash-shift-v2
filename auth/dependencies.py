from datetime import datetime
from os.path import abspath, dirname
from typing import Dict

from fastapi import Depends, Request
from fastapi.security import SecurityScopes
from jose import JWTError, jwt

from auth.schemas import JWTUser
from config import settings
from exceptions import NotAuthenticated, PermissionDenied


def get_token(request: Request):
    """
    Получение токена из запроса с использованием библиотеки Request
    :param token:
    :return: dict
    """
    token = request.headers.get("Authorization")
    try:
        token = token.split()[-1]
    except:
        raise NotAuthenticated
    return token


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(get_token)):
    user = None
    try:
        user = JWTUser(
            role="owner",
            data=jwt.decode(
                token,
                settings.TOKEN_OWNER_KEY,
                algorithms=settings.ALGORITHM,
                audience=settings.TOKEN_OWNER_AUDIENCE,
                issuer=settings.TOKEN_ISSUER,
            ),
        )
    except JWTError:
        try:
            user = JWTUser(
                role="worker",
                data=jwt.decode(
                    token,
                    settings.TOKEN_WORKER_KEY,
                    algorithms=settings.ALGORITHM,
                    audience=settings.TOKEN_WORKER_AUDIENCE,
                    issuer=settings.TOKEN_ISSUER,
                ),
            )
        except JWTError:
            raise NotAuthenticated

    if user is None or int(user.data.get("exp")) < datetime.utcnow().timestamp():
        raise NotAuthenticated

    if user.role == "worker":
        for scope in security_scopes.scopes:
            if scope not in user.data.get("api-permission", []):
                raise PermissionDenied

    return user
