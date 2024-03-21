from python:3.11-slim-bullseye

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./src/orchestrator/server.py /app/orchestrator/server.py

WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD flask --app orchestrator.server run --host 0.0.0.0
