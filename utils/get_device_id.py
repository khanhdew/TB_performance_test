import requests
import threading

from numpy.ma.core import floor

from auth.auth_user import auth_header
from config import num_threads
from utils.read_data_xlsx import number_of_devices
import config

devices_id = []

def get_device_api(page_size, page):
    url = config.tb_url + "/api/tenant/devices?pageSize=" + page_size + "&page=" + page
    x = requests.get(url, headers=auth_header)
    return x.json()

def process_device_id(startIndex, stopIndex):
    with open('device_id.txt', 'a') as f:  # Use 'a' to append to the file
        for i in range(startIndex, stopIndex):
            data = get_device_api("100", str(i))
            for device in data["data"]:
                f.write(device['id']['id'] + '\n')

def get_all_device_id():
    global devices_id
    try:
        with open('device_id.txt', 'r') as f:
            lines = f.readlines()
            if lines:
                devices_id = [line.strip() for line in lines]
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        threads = []
        for i in range(0, num_threads):
            thread = threading.Thread(target=process_device_id, args=(floor(i*(number_of_devices/num_threads)), floor((i+1)*(number_of_devices/num_threads))))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        with open('device_id.txt', 'r') as f:
            devices_id = [line.strip() for line in f]
    return devices_id

