FROM python:3.11.3

RUN mkdir /cash-shift-v2

WORKDIR /cash-shift-v2

COPY cash-shift-v2/requirements.txt .

RUN pip install -r requirements.txt

COPY cash-shift-v2/ .

RUN chmod a+x /cash-shift-v2/docker/*.sh

CMD ["gunicorn", 'main:app', '--workers', '4', '--worker-class', 'uvicorn.workers.UvicornWorker', '--bind=0.0.0.0:8000']

