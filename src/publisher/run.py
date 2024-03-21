import csv
import json
import logging
import time
from datetime import datetime

import pika

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[publisher] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)


def generate_eeg_data():
    with open("eeg_raw.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def broker_setup():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.1.11"))
            channel = connection.channel()
            channel.exchange_declare(exchange="poc", exchange_type="fanout")
            result = channel.queue_declare(queue="poc_queue", durable=True)
            channel.queue_bind(exchange="poc", queue=result.method.queue)
        except Exception:
            logger.info("Unable to establish any connection to the RabbitMQ broker. Retrying in 5 seconds.")
            time.sleep(5)
            continue

        return connection, channel


def main(connection, channel):
    logger.info("Sending EEG data to the queue...")
    for data in generate_eeg_data():
        current_timestamp = datetime.now().timestamp()
        payload = json.dumps({"start_time": current_timestamp, "data": data})
        channel.basic_publish(exchange="poc", routing_key="", body=payload)


if __name__ == "__main__":
    connection, channel = broker_setup()
    while True:
        try:
            main(connection, channel)
        except Exception as err:
            logger.info("Some unexpected error occurred. Trying to reestablish connection with the broker...")
            logger.info(f"Error: {str(err)}")
            connection, channel = broker_setup()
