import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cash_shift.router import router as router_cash_shift
from check.router import router as router_check
from event.base_consumer import Consumer


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer()


app = App()
app.include_router(router_cash_shift)
app.include_router(router_check)

origins = [
    "http://localhost:3000",
    "http://192.168.50.139:3000",
    "http://192.168.50.11:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.consumer.consume(loop))
    await task
