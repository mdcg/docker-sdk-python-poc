from python:3.11-slim-bullseye

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./src/publisher/run.py /app/run.py
COPY ./src/publisher/eeg_raw.csv /app/eeg_raw.csv

WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD python run.py
