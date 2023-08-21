from starlette.middleware.cors import CORSMiddleware

from cash_shift.router import router as router_cash_shift
from check.router import router as router_check
from check_status.router import router as router_check_status
from position_check.router import router as router_position_check

from type_operation.router import router as router_type_operation
from type_payment.router import router as router_type_payment
from type_taxation.router import router as router_type_taxation
from fastapi import FastAPI, Request, status


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

import pika

app = FastAPI()

app.include_router(router_cash_shift)
app.include_router(router_check)
app.include_router(router_check_status)
app.include_router(router_position_check)
app.include_router(router_type_operation)
app.include_router(router_type_payment)
app.include_router(router_type_taxation)



# app.middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methos=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
#     allow_headers=['Content-Type',
#                    'Set-Cookie',
#                    'Access-Control-Allow-Headers',
#                    'Access-Control-Allow-Origin',
#                    'Authorization']
# )


# @app.on_event("startup")
# def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='hello')
#
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!6456456445645')
# print(" [x] Sent 'Hello World!'")
#
# connection.close()
