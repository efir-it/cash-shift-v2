import asyncio
import time
from pprint import pprint
# from urllib.request import Request
import json
from fastapi import APIRouter, FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from cash_shift.router import router as router_cash_shift
from check.router import router as router_check
from position_check.router import router as router_position
from config import settings
from event.base_consumer import Consumer
from logger import logger


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer()


app = App(title="Efirit CheckoutShift Module", version="0.2")
cash_router = APIRouter(prefix="/checkoutShift")
cash_router.include_router(router_cash_shift)
cash_router.include_router(router_check)
cash_router.include_router(router_position)

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    start_time = time.time()

    body = await request.body()
    body_json = None
    if body:
        body_text = body.decode('utf-8')
        try:
            body_json = json.loads(body_text)
        except json.JSONDecodeError:
            body_json = body_text
        request._body = body

    async def receive_body():
        return {'type': 'http.request', 'body': body}

    request = Request(request.scope, receive=receive_body)

    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    response = Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

    process_time = time.time() - start_time

    status_code = response.status_code
    url = str(request.url)
    ip_address = request.client.host
    method = request.method

    if status_code == 200:
        logger.info(
            f"|| Status_code: {status_code}"
            f"|| URL: {url}"
            f"|| IP: {ip_address}"
            f"|| Method: {method}"
            f"|| Body: {body_json}"
            f"|| Response: {response_body.decode('utf-8')}",
            extra={"process_time": round(process_time, 2)}
        )
    else:
        logger.error(
            f"|| Status_code: {status_code}"
            f"|| URL: {url}"
            f"|| IP: {ip_address}"
            f"|| Method: {method}"
            f"|| Body: {body_json}"
            f"|| Response: {response_body.decode('utf-8')}"
            f"|| Query_params: {dict(request.query_params)}",
            extra={"process_time": round(process_time, 2)}
        )

    return response


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.consumer.consume(loop))
    await task
