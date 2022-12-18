import sys
import os
import json
import time
import paho.mqtt.client as mqtt

MQTT_HOST = os.environ.get("MQTT_HOST")
TEMP_THRESHOLD = float(os.environ.get("TEMP_THRESHOLD"))

def on_connect(client, userdata, flags, rc):
  client.subscribe([("house/temp/0", 0)])


def on_temperature(client, userdata, message):
  temperature = float(message.payload)
  print(F'Temperature: {temperature}')
  state = "off"
  if temperature < TEMP_THRESHOLD:
    state = "on"
  print(F'Set state to: {state}')
  client.publish("house/fireplace/set_state", payload=state)


client = mqtt.Client(client_id="fireplace-controller")
client.on_connect = on_connect
client.connect(MQTT_HOST)
client.message_callback_add("house/temp/0", on_temperature)
client.loop_forever()