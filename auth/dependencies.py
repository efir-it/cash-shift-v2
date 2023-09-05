from datetime import datetime
from typing import Optional, Dict
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
import os
import sys

from config import settings

from os.path import abspath, dirname
# sys.path.insert(0, dirname(dirname(dirname(abspath('dependencies.py')))))
# sys.path.insert(0, dirname(abspath(_file_)))
sys.path.append(r"C:/projects/store")
sys.path.append("..")

# current_path = os.path.dirname(os.path.abspath(_file_))
#
# app_path = os.path.abspath(os.path.join(current_path, "..", "store", "auth", "dependencies.py"))
# sys.path.append(app_path)





token_client = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJZCI6ImM4MDAwMTI4LTNlYTItNGJlOC1iOGM4LTQ1MDIxYjM0NDlkYiIsIm5iZiI6MTY5MzQ2MDM2NSwiZXhwIjoxNjkzNTQ2NzY1LCJpYXQiOjE2OTM0NjAzNjUsImlzcyI6IkV0aGVySVRfQXV0aF9Nb2R1bGUiLCJhdWQiOiJFdGhlcklUX0NsaWVudF9FbnRpdHkifQ.Dhig363HOJ8QKU3zaODAlQ1tO4nujK_wD5rqWgjD1trxzqG57uAkzeMEsTa9YbFW_xcAc51b2b8iBoPchOytNg'
toker_worker = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ3b3JrZXJJZCI6ImRkNzE4NTcwLTU3MDctNGMxYS1hYzEzLTJjZDVmNjIxNjFlMyIsImNsaWVudElkIjoiYzgwMDAxMjgtM2VhMi00YmU4LWI4YzgtNDUwMjFiMzQ0OWRiIiwib3JnYW5pemF0aW9uSWQiOiJjODAwMDEyOC0zZWEyLTRiZTgtYjhjOC00NTAyMWIzNDQ5ZGIiLCJuYmYiOjE2OTM0NjA4NzQsImV4cCI6MTY5MzU0NzI3NCwiaWF0IjoxNjkzNDYwODc0LCJpc3MiOiJFdGhlcklUX0F1dGhfTW9kdWxlIiwiYXVkIjoiRXRoZXJJVF9Xb3JrZXJfRW50aXR5In0.mOvqDBO699Kx6lJEwJGrRSi5o7Wfx8QBcGjtAY8bcvJRmKyTbXVEry8oD9inRvBb64I63A6Gpu2cUc6Hy-T9yw'



def get_token(request: Request):
    """
    Получение токена из запроса с использованием библиотеки Request
    :param token:
    :return: dict
    """
    token = request.cookies.get("Authorization: Bearer [token]")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect jwt token")
    return token


# async def get_current_user(token: str = Depends(get_token)):
def get_current_user(token: str):
    # try:
    #     client = jwt.decode(token, settings.TOKEN_CLIENT_KEY, algorithms=settings.ALGORITHM, audience=settings.TOKEN_CLIENT_AUDIENCE, issuer=settings.TOKEN_ISSUER)
    # except JWTError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    worker = jwt.decode(token, settings.TOKEN_WORKER_KEY, algorithms=settings.ALGORITHM, audience=settings.TOKEN_WORKER_AUDIENCE, issuer=settings.TOKEN_ISSUER)

    # if client:
    #     if client.get('clientId'):
    #         expire: str = client.get('exp')
    #         if expire and (int(expire) < datetime.utcnow().timestamp()):
    #             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if worker.get('workerId'):
        expire: str = worker.get('exp')
        if expire and (int(expire) < datetime.utcnow().timestamp()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # print(client)
    # print(worker)

    if 'workerId' in worker:
        return worker

    # item_id: str = ''
    # if client.get('clientId'):
    #     item_id = client.get('clientId')
    # if worker.get('workerId'):
    #     item_id = worker.get('workerId')
    # if not item_id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # await item_id  ## item = await UserDAO.find_by_id(user_id)
    # return item_id











# async def get_current_client_or_worker(client_or_worker: str = Depends(get_current_item())):
#     if client_or_worker == client_id:
#         return client_or_worker
#     else:
#           return '...'


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