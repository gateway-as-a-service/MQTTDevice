import json
import time

import paho.mqtt.client as mqtt

from config import DEVICE_UUID
from discovery.libs.utils import retrieve_logger, get_traceback


class MQTTSubscriber(object):
    REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL = "devices_messages"

    def __init__(self, broker_address):
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect_callback
        self.mqtt.on_message = self._process_message_received
        self.mqtt.on_publish = self._on_publish_callback
        self.publish_topic = "devices/{}".format(DEVICE_UUID)
        self._connect_to_mqtt_broker(broker_address)

        self.logger = retrieve_logger("mqtt_subscriber")

    def _connect_to_mqtt_broker(self, broker_address):
        while True:
            try:
                self.mqtt.connect(broker_address)
                return
            except Exception as err:
                self.logger.error(
                    "Failed to connect to the broker. Reason: {}".format(get_traceback())
                )
                time.sleep(5)

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        client.connected_flag = True
        self.mqtt.subscribe("devices/+", qos=0)

    def _on_publish_callback(self, client, userdata, mid):
        self.logger.debug("Published data")
        self.logger.debug(client)
        self.logger.debug(userdata)
        self.logger.debug(mid)

    def _process_message_received(self, client, user_data, message):
        try:
            self.logger.info("Topic: {}".format(message.topic))
            parsed_message = json.loads(message.payload.decode("utf-8"))
            self.logger.info("Device has received a new message {}".format(parsed_message))

            self.mqtt.publish(self.publish_topic, json.dumps(parsed_message))
            self.logger.info("Send message to the gateway to be parse")

        except Exception as err:
            print(err)

    def start(self):
        self.mqtt.loop_forever()


if __name__ == '__main__':
    mqtt_subscriber = MQTTSubscriber("127.0.0.1")
    mqtt_subscriber.start()
