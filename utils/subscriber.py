import threading
import json
import time
from numpy.ma.core import floor
from websockets.sync.client import connect
from config import Config as config
from auth.auth_user import auth_token
from utils.get_devices import DeviceList

dv = DeviceList()
devices_id = dv.devices_id
num_device = len(devices_id)
num = 0
total_messages = -num_device

def websocket_handler(thread_id, start_index, stop_index):
    connections = []
    global num
    retry_count = 0
    max_retries = 5
    while retry_count < max_retries:
        try:
            websocket = connect(f"ws://{config.tb_host}:{config.tb_port}/api/ws")
            for i in range(int(start_index), int(stop_index)):
                try:
                    connections.append((websocket, devices_id[i]))
                    object = {"authCmd": {"cmdId": 0, "token": auth_token},
                              "cmds": [{"entityType": "DEVICE", "entityId": devices_id[i],
                                        "scope": "LATEST_TELEMETRY", "cmdId": thread_id, "type": "TIMESERIES"}]}
                    websocket.send(json.dumps(object))
                    num += 1
                except Exception as e:
                    # print(f"With id: {i}")
                    # print(f"Thread {thread_id} failed to connect to device {devices_id[i]}: {e}")
                    pass
            break
        except Exception as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # Exponential backoff
            # print(f"Failed to connect websocket: {e}")
            # print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    else:
        print(f"Failed to connect websocket after {max_retries} attempts.")
        return

    while True:
        for websocket, device_id in connections:
            try:
                message = websocket.recv()
                if message:
                    global total_messages
                    total_messages += 1
                    print("\rTotal messages received: %d" % total_messages, end="")
            except Exception as e:
                # print(f"Thread {thread_id} encountered an error with device {device_id}: {e}")
                pass
def run():
    threads = []
    for i in range(0, config.num_threads):
        thread = threading.Thread(target=websocket_handler, args=(
        i, int(floor(i * (num_device / config.num_threads))), floor((i + 1) * (num_device / config.num_threads))))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

run()