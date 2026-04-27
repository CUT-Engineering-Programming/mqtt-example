import paho.mqtt.client as mqtt
from random import uniform
import time

mqttBroker = "broker.hivemq.com"
client = None

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Temperature_Sensor")
    client.connect(mqttBroker, port=1883, keepalive=60)

    while True:
        randNumber = uniform(20.0, 30.0)
        client.publish("TEMPERATURE", randNumber)
        print("Just published " + str(randNumber) + " to Topic TEMPERATURE")
        time.sleep(1)
except ConnectionRefusedError:
    print("Connection refused. Check broker address and network.")
except KeyboardInterrupt:
    print("Publisher stopped.")
    if client is not None:
        client.disconnect()
except Exception as e:
    print(f"An error occurred: {e}")
