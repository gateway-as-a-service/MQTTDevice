import json
import random
import time

import paho.mqtt.client as mqtt

from discovery.libs.utils import get_ip_address, retrieve_logger, get_traceback
from discovery_client import HubDiscoveryClient

DEVICE_INFO = {
    "id": "0a9c8868-5ba4-4b18-bf92-320971118425",
    # "id": str(uuid.uuid4()),
    "type": "ON/OFF DEVICE",
    "name": "First Device",
    "protocol": "MQTT",
    "ip": get_ip_address(),
}


# DEVICE_INFO["id"] = sys.argv[1]


class MQTTSmartObject(object):
    def __init__(self, device_info, *args, **kwargs):
        self.device_info = device_info
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect_callback
        self.mqtt_client.on_publish = self._on_publish_callback

        self.hub_address = None
        self.publish_topic = "devices/{}".format(self.device_info["id"])

        self.logger = retrieve_logger("mqtt")

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        self.logger.debug("Connected flags" + str(flags) + "result code " \
                          + str(rc) + "client1_id ")
        client.connected_flag = True

    def _on_publish_callback(self, client, userdata, mid):
        self.logger.debug("Published data")
        self.logger.debug(client)
        self.logger.debug(userdata)
        self.logger.debug(mid)

    def _discover_hub(self):
        hub_discovery_client = HubDiscoveryClient(self.device_info, logger=self.logger)
        hub_address = hub_discovery_client.discover()
        self.hub_address = hub_address

    def _connect_to_mqtt_broker(self):
        while True:
            try:
                self.mqtt_client.connect(self.hub_address)
                return
            except Exception as err:
                self.logger.error(
                    "Failed to connect to the broker. Reason: {}".format(get_traceback())
                )
                time.sleep(5)

    def start(self):
        self._discover_hub()

        self._connect_to_mqtt_broker()

        time.sleep(5)  # To wait for the container to start

        count = 0
        while count < 10:
            data = {
                "id": DEVICE_INFO["id"],
                "n": DEVICE_INFO["name"],
                "v": random.randint(15, 23),
                "u": "C",
                "t": time.time(),
            }

            self.logger.debug("Publish data: {}".format(data))

            try:
                self.mqtt_client.publish(self.publish_topic, json.dumps(data), qos=0)
            except Exception as err:
                self.logger.error("Failed to publish the data. Reason: {}", get_traceback())
            finally:
                count += 1

            self.logger.debug("Sleeping.....")
            time.sleep(random.uniform(0.5, 1))


if __name__ == '__main__':
    smart_object = MQTTSmartObject(DEVICE_INFO)
    smart_object.start()
