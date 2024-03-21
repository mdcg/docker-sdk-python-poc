from influxdb_client import InfluxDBClient, Point


class InfluxDB:
    def __init__(self):
        client = InfluxDBClient(url="192.168.1.11:8086", token="SUPERTOKEN!", org="poc")
        self.write_api = client.write_api()

    def collect(self, elapsed_time):
        point = Point("rabbitmq").tag("service", "consumer").field("elapsed_time", elapsed_time)
        self.write_api.write(bucket="eeg", record=point)
