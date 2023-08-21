from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
# from jose import jwt, JWTError

from app.config import settings


def get_token(request: Request):
    token = request.cookies.get('')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# async def get_current_item(token: str = Depends(get_token)):
#     try:
#         payload = jwt.decode(token, settings.SECRETKEY, settings.ALGORITHM)
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     expire: str = payload.get('exp')
#     if not expire or (int(expire) < datetime.utcnow().timestamp()):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     item_id: str = payload.get('sub')
#     if not item_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     item = await item_id  ## item = await UserDAO.find_by_id(user_id)
#     return item


# async def get_current_client_or_worker(client_or_worker: str = Depends(get_current_item())):
#     if client_or_worker == client_id:
#         return client_or_worker
#     else:
#           return '...'