# utils/http_publisher.py
import random
import time
import requests
import threading
from config import Config as config
from utils.get_devices import DeviceList
from utils.read_data_xlsx import ReadDataXlsx

dataframe = ReadDataXlsx().dataframe
dv = DeviceList()
devices_id = dv.devices_id
devices_access_token = dv.devices_access_token
num_device = len(devices_id)
total_messages_sent = 0

def send_telemetry(thread_id, start_index, stop_index):
    global total_messages_sent
    while True:
        for i in range(int(start_index), int(stop_index)):
            device_id = devices_id[i]
            url = config.tb_url + f"api/v1/{devices_access_token[i][0:20]}/telemetry"
            headers = {
                "Content-Type": "application/json",
            }
            data = {
                "temperature": random.randint(20, 30),
                "humidity": random.randint(40, 60),
            }
            time.sleep(0.001)
            retry_count = 0
            max_retries = 5
            while retry_count < max_retries:
                try:
                    response = requests.post(url, json=data, headers=headers)
                    response.raise_for_status()  # Check for HTTP errors
                    total_messages_sent += 1
                    print("\rTotal messages sent: %d" % total_messages_sent, end="")
                    break
                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    # print(f"Failed to send telemetry for device {device_id}: {e}")
                    # print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            else:
                print(f"Failed to send telemetry for device {device_id} after {max_retries} attempts.")

def run():
    threads = []
    for i in range(0, config.num_threads):
        thread = threading.Thread(target=send_telemetry, args=(
        i, int(i * (num_device / config.num_threads)), int((i + 1) * (num_device / config.num_threads))))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

run()