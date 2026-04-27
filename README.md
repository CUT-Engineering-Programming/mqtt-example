# MQTT Example

These three scripts demonstrate the **publish/subscribe (pub/sub)** messaging pattern using the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library and the free public broker at `broker.hivemq.com`.

---

## How MQTT Pub/Sub Works

```
[Temperature Publisher] ──┐
                          ├──► [broker.hivemq.com] ──► [Subscriber]
[Humidity Publisher]    ──┘
```

- **Publishers** send data to a named **topic** on the broker.
- **Subscribers** register interest in one or more topics and receive any messages posted to them.
- The broker routes messages between publishers and subscribers — they never communicate directly.

---

## 1. `mqtt_publish_temperature.py`

**Role:** Publisher — simulates a temperature sensor.

**What it does:**
- Connects to `broker.hivemq.com` as the client `"Temperature_Sensor"`.
- Every second, generates a random float between **20.0 and 30.0** (°C).
- Publishes that value to the topic `"TEMPERATURE"`.
- Runs indefinitely until stopped with `Ctrl+C`.

**Key lines:**
```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Temperature_Sensor")
client.connect(mqttBroker, port=1883, keepalive=60)

randNumber = uniform(20.0, 30.0)
client.publish("TEMPERATURE", randNumber)
```

---

## 2. `mqtt_publish_humidity.py`

**Role:** Publisher — simulates a humidity sensor.

**What it does:**
- Connects to `broker.hivemq.com` as the client `"Humidity_Sensor"`.
- Every second, generates a random float between **40.0 and 80.0** (%).
- Publishes that value to the topic `"HUMIDITY"`.
- Runs indefinitely until stopped with `Ctrl+C`.

**Key lines:**
```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Humidity_Sensor")
client.connect(mqttBroker, port=1883, keepalive=60)

randNumber = uniform(40.0, 80.0)
client.publish("HUMIDITY", randNumber)
```

---

## 3. `mqtt_subscribe.py`

**Role:** Subscriber — simulates a smartphone or dashboard receiving sensor data.

**What it does:**
- Connects to `broker.hivemq.com` as the client `"Smartphone"`.
- Subscribes to **both** the `"TEMPERATURE"` and `"HUMIDITY"` topics.
- Whenever a message arrives on either topic, the `on_message` callback prints it.
- Listens for **30 seconds** then exits cleanly.

**Key lines:**
```python
def on_message(client, userdata, message):
    print("Received message on topic '" + message.topic + "': "
          + str(message.payload.decode("utf-8")))

client.loop_start()          # starts background network thread
client.subscribe("TEMPERATURE")
client.subscribe("HUMIDITY")
client.on_message = on_message
time.sleep(30)               # listen for 30 seconds
client.loop_stop()
```

`loop_start()` runs the MQTT network loop in a background thread so the main thread can sleep and wait for incoming messages.

---

## Error Handling

All three scripts share the same exception structure:

| Exception | Meaning | Action |
|---|---|---|
| `ConnectionRefusedError` | Broker unreachable or network down | Prints a helpful message and exits |
| `KeyboardInterrupt` | User pressed `Ctrl+C` | Gracefully disconnects and exits |
| `Exception` | Any other unexpected error | Prints the error message and exits |

---

## Running the Scripts

Open **three separate terminals** and run:

```bash
# Terminal 1
python mqtt_publish_temperature.py

# Terminal 2
python mqtt_publish_humidity.py

# Terminal 3
python mqtt_subscribe.py
```

The subscriber will print temperature and humidity readings as they arrive from both publishers.
