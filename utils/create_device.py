import requests as rq
import threading

from numpy.ma.core import floor

from auth import auth_user
import config
import read_data_xlsx
from config import Config as config
from utils.read_data_xlsx import ReadDataXlsx

dataframe = ReadDataXlsx.dataframe

num_device = ReadDataXlsx.number_of_devices

# read row in dataframe
def create_device(startIndex, stopIndex):
    for i in range(startIndex, stopIndex):
        print(dataframe["Tên HC"].iloc[i] + " | " + dataframe["Địa chỉ MAC"].iloc[i])
        device = {
            "device": {
                "name": f'{dataframe["Tên HC"].iloc[i]}',
                "label": "",
                "additionalInfo": {
                    "gateway": True,
                    "description": "",
                    "overwriteActivityTime": False
                }
            },
            "deviceProfileId": {
                "id": "cdc55580-6414-11ef-8752-7307fa6d141d",
                "entityType": "DEVICE_PROFILE"
            }
            ,
            "credentials": {
                "credentialsType": "ACCESS_TOKEN",
                "credentialsId": f'{dataframe["Địa chỉ MAC"].iloc[i]}'
            }
        }
        x = rq.post(config.tb_url + "api/device-with-credentials", json=device, headers=auth_user.auth_header)
        print(x.json())
        with open('device_id.txt', 'a') as f:
            try:
                f.write(x.json()['id']['id'] + '\n')
            except:
                pass

        global num_device
        if x.status_code == 200 : num_device -= 1
        print(num_device)


# start thread
def main():
    threads = []
    for i in range(0, config.num_threads):
        thread = threading.Thread(target=create_device, args=(
        int(floor(i * num_device / config.num_threads)), int(floor((i + 1) * num_device / config.num_threads - 1))))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

