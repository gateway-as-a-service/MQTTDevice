import sys
import subprocess
import random

DEVICES_UUIDS = [
    'd788f2b1-6080-4570-ae55-ed71eb146a1a', '0273cbca-7a4a-4dca-87db-1268761337e4',
    '6201d03d-640f-4a2e-aed9-9d6dc037f73b', 'b8758601-4726-48ff-9457-87b6240c70ac',
    '7115f32b-c84b-4dbc-9e53-b56476d68fc7', '7e2f23a3-fbea-4843-bc79-0f04b9596abe',
    'ff82767e-6bab-4af7-bfe3-534100f3b2eb', 'a9cc8991-a99a-420f-8865-a29d745631fe',
    'f8bcf0f9-fadb-46fe-a251-472e559e91df', '286d0581-3296-4923-ba90-7bd343bf17e0',
    '8730862f-84da-4916-9c82-4889aa768aec', '0dea48da-3f48-4ba4-ab88-9d0f1de41bec',
    '9e75730e-c0a8-433d-b8f1-004e8908414a', 'cc367153-3ba2-4e86-b673-002210612094',
    '4c77b947-e8d0-49bc-9a92-e0cfa5c45346', 'a4c2c5fc-939e-408f-b1c3-238aa280a4e0',
    '3acc2551-e70d-467c-b755-e6b7820dbbfb', 'b99db5ed-9a8a-4684-b21b-18ea21c8baab',
    '53486061-90dc-4bac-9afd-7460bac9463f', '83a3f6f8-23bd-4df0-b307-795abbdce7f7'
]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Must provide the number of devices")

    number_of_devices = int(sys.argv[1])
    selected_devices_uuids = random.sample(DEVICES_UUIDS, number_of_devices)
    for device_uuid in selected_devices_uuids:
        device_command = ["start", r"E:\VirtualEnvs\Python3\MQTT_Device\Scripts\python.exe", "./device.py",
                          device_uuid]
        subprocess.Popen(device_command, shell=True)

        # receiver_command = ["start", r"E:\VirtualEnvs\Python3\MQTT_Device\Scripts\python.exe", "./receiver.py",
        #                     device_uuid]
        # subprocess.Popen(receiver_command, shell=True)
