from demo.smart_house.devices.bathroom_fan_device import DEVICE_INFO
from receiver import MessagesReceiver

if __name__ == '__main__':
    device_id = DEVICE_INFO["id"]
    broker_address = "127.0.0.1"
    bathroom_fan_devices_receiver = MessagesReceiver(device_id, broker_address)
    bathroom_fan_devices_receiver.start()
