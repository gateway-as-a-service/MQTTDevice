import json
import socket
import time
import uuid

from discovery.config import DISCOVERY_RESPONSE_PORT, DISCOVERY_REQUEST_BROADCAST_PORT
from discovery.libs.utils import get_ip_address, FakeLogger


class HubDiscoveryClient(object):

    def __init__(self, device_info, *args, **kwargs):
        self.device_info = device_info
        self.logger = kwargs.get("logger", FakeLogger())
        self.discovery_service_port = kwargs.get("discovery_port", DISCOVERY_REQUEST_BROADCAST_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(50)

    def discover(self):

        self.logger.info("Waiting for discovery message")

        discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        discovery_sock.settimeout(50)
        discovery_sock.bind(("", 9000))

        discovery_server_address = ""
        while True:
            try:
                data, address = discovery_sock.recvfrom(4096)
                self.logger.info("Received discovery message: {}".format(data))

                data = json.loads(data.decode("utf-8"))
                discovery_server_address = data["ip"]

                break

            except Exception as err:
                # self.logger.error("Timeout")
                # self.logger.error(err)
                self.logger.error(err, exc_info=True)

        binding_address = ("", self.discovery_service_port)
        self.sock.bind(binding_address)

        self.logger.debug("Contacting discovery service")
        while True:
            broadcast_address = (discovery_server_address, DISCOVERY_RESPONSE_PORT)
            self.sock.sendto(json.dumps(self.device_info).encode("utf-8"), broadcast_address)
            self.logger.debug("Send info about device {}".format(self.device_info["id"]))

            try:
                data, address = self.sock.recvfrom(4096)
            except Exception as err:
                self.logger.info("Timeout for receiving discovery confirmation")
                time.sleep(5)
                continue

            if data != b'OK':
                continue

            hub_address = address[0]
            self.logger.debug(
                "Device {} has been registered".format(self.device_info["id"])
            )

            return hub_address


if __name__ == '__main__':
    DEVICE_INFO = {
        'id': str(uuid.uuid4()),
        "type": "ON/OFF DEVICE",
        "name": "First Device",
        "protocol": "MQTT",
        "ip": get_ip_address(),
        "unit": "C",
    }

    hub_discovery_client = HubDiscoveryClient(DEVICE_INFO)
    hub_discovery_client.discover()
