import paho.mqtt.client as mqtt
from random import uniform
import time

mqttBroker = "broker.hivemq.com"
client = None

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Humidity_Sensor")
    client.connect(mqttBroker, port=1883, keepalive=60)

    while True:
        randNumber = uniform(40.0, 80.0)
        client.publish("HUMIDITY", randNumber)
        print("Just published " + str(randNumber) + " to Topic HUMIDITY")
        time.sleep(1)
except ConnectionRefusedError:
    print("Connection refused. Check broker address and network.")
except KeyboardInterrupt:
    print("Publisher stopped.")
    if client is not None:
        client.disconnect()
except Exception as e:
    print(f"An error occurred: {e}")
