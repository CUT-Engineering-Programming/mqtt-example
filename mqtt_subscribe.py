import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("Received message on topic '" + message.topic + "': "
          + str(message.payload.decode("utf-8")))

mqttBroker = "broker.hivemq.com"
client = None

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Smartphone")
    client.connect(mqttBroker, port=1883, keepalive=60)

    client.loop_start()
    client.subscribe("TEMPERATURE")
    client.subscribe("HUMIDITY")
    client.on_message = on_message
    time.sleep(30)
    client.loop_stop()
except ConnectionRefusedError:
    print("Connection refused. Check broker address and network.")
except KeyboardInterrupt:
    print("Subscriber stopped.")
    if client is not None:
        client.loop_stop()
        client.disconnect()
except Exception as e:
    print(f"An error occurred: {e}")
