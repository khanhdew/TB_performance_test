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
num_device = len(devices_id)
total_messages = 0

def send_telemetry(thread_id, start_index, stop_index):
    global total_messages
    while True:
        for i in range(int(start_index), int(stop_index)):
            device_id = devices_id[i]
            time.sleep(1/1000)
            url = config.tb_url + f"api/v1/{dataframe.iloc[i]['Địa chỉ MAC']}/telemetry"
            headers = {
                "Content-Type": "application/json",
            }
            data = {
                "temperature": random.randint(20, 30),
                "humidity": random.randint(40, 60),
            }
            try:
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                total_messages += 1
                print(f"Total messages sent: {total_messages}\n")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send telemetry for device {device_id}: {e}")
                time.sleep(1)  # Chờ 1 giây trước khi thử lại

threads = []
for i in range(0, config.num_threads):
    thread = threading.Thread(target=send_telemetry, args=(i, int(i*(num_device/config.num_threads)), int((i+1)*(num_device/config.num_threads))))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()