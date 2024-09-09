import threading
import json
import time

from numpy.ma.core import floor
from websockets.sync.client import connect
from config import Config as config
from auth.auth_user import auth_token
from utils.get_device_id import DeviceList

dv = DeviceList()
devices_id = dv.devices_id
num_device= devices_id.__len__()
num = 0
total_messages = - num_device
def websocket_handler(thread_id, start_index, stop_index):
    connections = []
    global num
    websocket = connect(f"ws://{config.tb_host}:{config.tb_port}/api/ws")
    for i in range(int(start_index),int(stop_index)):
        try:
            connections.append((websocket, devices_id[i]))
            object = {"authCmd": {"cmdId": 0,
                                  "token": auth_token},
                      "cmds": [{"entityType": "DEVICE", "entityId": devices_id[i],
                                "scope": "LATEST_TELEMETRY", "cmdId": thread_id, "type": "TIMESERIES"}]}
            time.sleep(0.1)
            websocket.send(json.dumps(object))
            num += 1
            print(f"Thread {thread_id} connected to device {devices_id[i]}, devices connected {num}\n")

        except Exception as e:
            print(f"With id: {i}")
            print(f"Thread {thread_id} failed to connect to device {devices_id[i]}: {e}")


    while True:
        for websocket, device_id in connections:
            try:
                message = websocket.recv()
                if message:
                    # print(f"Thread {thread_id} received message from device {device_id}: {message}")
                    global total_messages
                    total_messages += 1
                    print(f"Total messages received: {total_messages}\n")
            except Exception as e:
                print(f"Thread {thread_id} encountered an error with device {device_id}: {e}")
                time.sleep(0.5)  # Wait before attempting to reconnect


threads = []
for i in range(0, config.num_threads):
    thread = threading.Thread(target=websocket_handler, args=(i, int(floor(i*(num_device/config.num_threads))) , floor((i+1)*(num_device/config.num_threads))))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
