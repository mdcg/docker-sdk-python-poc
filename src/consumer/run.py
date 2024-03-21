import json
import logging
import time
from datetime import datetime, timedelta

import pika

from consumer.influxdb import InfluxDB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[consumer] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)


class Consumer:
    USE_INFLUXDB = True

    def __init__(self):
        self.__influxdb_connection_retry_time = None
        self.broker_setup()
        self.influxdb_setup()

    def broker_setup(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.1.11"))
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange="poc", exchange_type="fanout")
                result = self.channel.queue_declare(queue="poc_queue", durable=True)
                self.channel.queue_bind(exchange="poc", queue=result.method.queue)
            except Exception:
                logger.info("Unable to establish any connection to the RabbitMQ broker. Retrying in 5 seconds.")
                time.sleep(5)
                continue

            break

    def influxdb_setup(self, retry=0):
        if not self.USE_INFLUXDB:
            logger.info("InfluxDB is not currently required. Skipping.")
            return None

        while True:
            try:
                self.metrics = InfluxDB()
            except Exception:
                logger.info("Unable to connect to InfluxDB at this time. Retrying in 5 seconds.")
                time.sleep(5)
                continue

            break

    def collect_elapsed_time(self, elapsed_time):
        if not self.USE_INFLUXDB:
            logger.info("InfluxDB is not currently required. Skipping.")
            return None

        if self.metrics is None:
            self.influxdb_setup()

        self.metrics.collect(elapsed_time)

    def callback(self, ch, method, properties, body):
        payload = json.loads(body)
        end_time = datetime.now().timestamp()
        elapsed_time = end_time - payload["start_time"]
        self.collect_elapsed_time(elapsed_time)
        logger.info(f"Elapsed time: {elapsed_time}")

    def run(self):
        logger.info("Initializing. Waiting for messages...")
        self.channel.basic_consume(queue="poc_queue", on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()


if __name__ == "__main__":
    consumer = Consumer()
    while True:
        try:
            consumer.run()
        except Exception as err:
            logger.info("Some unexpected error occurred. Trying to reestablish connection with the broker...")
            logger.info(f"Error: {str(err)}")
            consumer = Consumer()
