import json
import sys
import time

import paho.mqtt.client as mqtt

from discovery.libs.utils import retrieve_logger, get_traceback, get_ip_address

DEVICE_INFO = {
    "id": "0a9c8868-5ba4-4b18-bf92-320971118425",
    # "id": str(uuid.uuid4()),
    "type": "ON/OFF DEVICE",
    "name": "First Device",
    "protocol": "MQTT",
    "ip": get_ip_address(),
}


# DEVICE_INFO["id"] = sys.argv[1]


class MessagesReceiver(object):
    def __init__(self, device_uuid, broker_address):
        self.device_uuid = device_uuid
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect_callback
        self.mqtt.on_message = self._process_message_received
        self.mqtt.connect(broker_address, keepalive=65535)

        self.publish_topic = "devices/{}".format(self.device_uuid)

        self.logger = retrieve_logger("logger")

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        client.connected_flag = True

        device_forward_message_topic = "devices/{}/forward".format(self.device_uuid)
        self.mqtt.subscribe(device_forward_message_topic, qos=0)
        self.logger.debug("Subscribed to: {}".format(device_forward_message_topic))

    def _process_message_received(self, client, user_data, message):
        parsed_message = json.loads(message.payload.decode("utf-8"))
        new_value = parsed_message["message"]
        self.logger.info("Received message : {}".format(parsed_message))
        self.logger.info("Topic: {}".format(message.topic))

        self.logger.info("Send to the gateway the newly received value")
        send_message = {
            "id": self.device_uuid,
            "v": new_value,
            "t": time.time()
        }

        try:
            self.mqtt.publish(self.publish_topic, json.dumps(send_message), qos=0)
        except Exception as err:
            self.logger.error("Failed to publish the data. Reason: {}", get_traceback())

    def start(self):
        self.logger.debug("Waiting incoming messages for device: {}".format(self.device_uuid))

        self.mqtt.loop_forever()


if __name__ == '__main__':
    messages_receiver = MessagesReceiver(DEVICE_INFO["id"], "127.0.0.1")
    messages_receiver.start()
