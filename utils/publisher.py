import time
from math import floor
import random

from paho.mqtt import client as mqtt_client
import threading

from config import Config as config
from get_device_id import DeviceList
from read_data_xlsx import ReadDataXlsx
dataframe = ReadDataXlsx().dataframe

dv = DeviceList()
devices_id = dv.devices_id
num_device= devices_id.__len__()
print(num_device)
class MqttConn():
    def __init__(self, broker, port, topic, access_token):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.access_token = access_token
        self.client = self.connect_mqtt()
        self.last_time = time.time()

    def connect_mqtt(self, timeout=60) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                pass
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client()
        client.username_pw_set(self.access_token)
        client.on_connect = on_connect
        try:
            client.connect(self.broker, self.port, keepalive=timeout)
        except TimeoutError:
            print(f"Connection to {self.broker}:{self.port} timed out")
        return client

    def publish(self, message):
        if time.time() - self.last_time >= 300:
            self.last_time = time.time()
            self.client.publish(self.topic, message)
            print("message published")


total_messages = 0
devices_connected = 0
def mqtt_handler(thread_id, start_index, stop_index):
    global total_messages, devices_connected
    mqttConnections = []
    for i in range(int(start_index),int(stop_index)):
        mqtt = MqttConn(f'{config.tb_host}', 5883, "v1/devices/me/telemetry", f'{dataframe.iloc[i]["Địa chỉ MAC"]}')

        mqttConnections.append(mqtt.connect_mqtt())
        devices_connected += 1
        print(f"Thread {thread_id} devices connected {devices_connected}\n")
        time.sleep(0.5)
    while True:
        for mqtt in mqttConnections:
            mqtt.publish(
                f'{{"temp": {random.randint(20, 30)}, "humid": {random.randint(40, 60)}, "soil": {random.randint(0, 100)}, "timestamp": {int(time.time())}}}')
            total_messages += 1
            print(f"Total messages published: {total_messages}\n")
threads = []

for i in range(0, config.num_threads):
    thread = threading.Thread(target=mqtt_handler, args=(i, int(floor(i*(num_device/config.num_threads))) , floor((i+1)*(num_device/config.num_threads))))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()