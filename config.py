import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

GASS_REDIS_HOSTNAME = "127.0.0.1"
GASS_REDIS_PORT = 6379

DEVICE_UUID = "0a9c8868-5ba4-4b18-bf92-320971118425"

PROTOCOL = "MQTT"


class Operations:
    READ_OPERATION = "READ"
    WRITE_OPERATION = "WRITE"


class Values:
    STRING = "STRING"
    NUMERIC = "NUMERIC"
