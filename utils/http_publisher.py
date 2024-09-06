import random
import time

import requests
import threading
from config import Config as config
from get_device_id import DeviceList
from read_data_xlsx import ReadDataXlsx
dataframe = ReadDataXlsx().dataframe

dv = DeviceList()
devices_id = dv.devices_id
num_device= devices_id.__len__()
total_messages = 0
def send_telemetry(thread_id, start_index, stop_index):
    global total_messages
    while True:
        for i in range(int(start_index), int(stop_index)):
            device_id = devices_id[i]
            url = config.tb_url + f"api/v1/{dataframe.iloc[i]['Địa chỉ MAC']}/telemetry"
            headers = {
                "Content-Type": "application/json",
            }
            data = {
                "temperature": random.randint(20, 30),
                "humidity": random.randint(40, 60),
            }
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                # print(f"Thread {thread_id} sent telemetry to device {device_id}")
                total_messages += 1
                print(f"Total messages sent: {total_messages}\n")
            time.sleep(0.5)
        time.sleep(1)


threads = []
for i in range(0, config.num_threads):
    thread = threading.Thread(target=send_telemetry, args=(i, int(i*(num_device/config.num_threads)), int((i+1)*(num_device/config.num_threads))))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()