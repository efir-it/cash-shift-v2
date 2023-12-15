import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cash_shift.router import router as router_cash_shift
from check.router import router as router_check
from config import settings
from event.base_consumer import Consumer


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer()


app = App(title="Efirit CheckoutShift Module", version="0.2")
cash_router = APIRouter(prefix="/checkoutShift")
cash_router.include_router(router_cash_shift)
cash_router.include_router(router_check)

app.include_router(cash_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS.split(";"),
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
