FROM python:3.11.3

RUN mkdir /cash

WORKDIR /cash

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /cash/docker/*.sh