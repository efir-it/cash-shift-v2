import asyncio
from starlette.middleware.cors import CORSMiddleware
from event.base_consumer import Consumer
from cash_shift.router import router as router_cash_shift
from check.router import router as router_check
from position_check.router import router as router_position_check

from fastapi import FastAPI, Request, status


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer()


app = App()

app.include_router(router_cash_shift)
app.include_router(router_check)
app.include_router(router_position_check)

@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.consumer.consume(loop))
    await task
