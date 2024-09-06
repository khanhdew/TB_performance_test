import requests
import threading

from numpy.ma.core import floor

from auth.auth_user import auth_header
from config import Config as config
from utils.read_data_xlsx import ReadDataXlsx
import config

number_of_devices = ReadDataXlsx().number_of_devices

class DeviceList:
    devices_id = []
    initial = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DeviceList, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.initial:
            self.devices_id = self.get_all_device_id()
            self.initial = True

    def get_device_api(self, page_size, page):
        url = config.tb_url + "/api/tenant/devices?pageSize=" + page_size + "&page=" + page
        x = requests.get(url, headers=auth_header)
        return x.json()

    def process_device_id(self, startIndex, stopIndex):
        with open('device_id.txt', 'a') as f:
            for i in range(startIndex, stopIndex):
                data = self.get_device_api("100", str(i))
                for device in data["data"]:
                    f.write(device['id']['id'] + '\n')

    def get_all_device_id(self):
        try:
            with open('device_id.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    self.devices_id = [line.strip() for line in lines]
                else:
                    raise FileNotFoundError
        except FileNotFoundError:
            threads = []
            for i in range(0, config.num_threads):
                thread = threading.Thread(target=self.process_device_id, args=(floor(i*(number_of_devices/config.num_threads)), floor((i+1)*(number_of_devices/config.num_threads))))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            with open('device_id.txt', 'r') as f:
                self.devices_id = [line.strip() for line in f]
        return self.devices_id
