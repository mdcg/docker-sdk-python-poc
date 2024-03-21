from python:3.11-slim-bullseye

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./src/consumer/run.py /app/consumer/run.py
COPY ./src/consumer/influxdb.py /app/consumer/influxdb.py

WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD python -m consumer.run
