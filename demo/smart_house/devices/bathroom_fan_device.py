import json
import random
import time

import paho.mqtt.client as mqtt

from config import Operations, PROTOCOL
from discovery.libs.utils import get_traceback, retrieve_logger, get_ip_address
from discovery_client import HubDiscoveryClient

DEVICE_INFO = {
    "bver": 1.1,
    "id": "a976a385-473e-4b55-9f50-ce657e69eeb4",
    "type": "Actuator",
    "operations": [
        Operations.READ_OPERATION,
        Operations.WRITE_OPERATION
    ],
    "n": "BathroomFan",
    "protocol": PROTOCOL,
    "ip": get_ip_address(),
    "values": ["on", "off"],
    "v": "on",
}


class BathroomFanDevice(object):

    def __init__(self, device_info):
        self.device_info = device_info
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect_callback
        self.mqtt_client.on_publish = self._on_publish_callback

        self.hub_address = None
        self.publish_topic = "devices/{}".format(self.device_info["id"])

        self.logger = retrieve_logger("bathroom_fan")

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        self.logger.debug("Connected flags" + str(flags) + "result code " \
                          + str(rc) + "client1_id ")
        client.connected_flag = True

    def _on_publish_callback(self, client, userdata, mid):
        self.logger.debug("Published data")
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

        time.sleep(1000)

        count = 0
        while count < 10:
            data = {
                "id": self.device_info["id"],
                "n": self.device_info["n"],
                "v": random.choice(self.device_info["values"]),
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
    bathroom_fan = BathroomFanDevice(DEVICE_INFO)
    bathroom_fan.start()
