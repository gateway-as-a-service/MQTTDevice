import json

import paho.mqtt.client as mqtt

from config import DEVICE_UUID
from discovery.libs.utils import retrieve_logger


class MessagesReceiver(object):
    def __init__(self, device_uuid, broker_address):
        self.device_uuid = device_uuid
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect_callback
        self.mqtt.on_message = self._process_message_received
        self.mqtt.connect(broker_address)

        self.logger = retrieve_logger("logger")

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        client.connected_flag = True

        device_forward_message_topic = "devices/{}/forward".format(self.device_uuid)
        self.mqtt.subscribe(device_forward_message_topic, qos=1)
        self.logger.debug("Subscribed to: {}".format(device_forward_message_topic))

    def _process_message_received(self, client, user_data, message):
        self.logger.info("Topic: {}".format(message.topic))
        self.logger.info("QoS: {}".format(message.qos))
        parsed_message = json.loads(message.payload.decode("utf-8"))
        self.logger.info("Message: {}".format(parsed_message))

    def start(self):
        self.logger.debug("Waiting incoming messages")

        self.mqtt.loop_forever()


if __name__ == '__main__':
    messages_receiver = MessagesReceiver(DEVICE_UUID, "127.0.0.1")
    messages_receiver.start()
