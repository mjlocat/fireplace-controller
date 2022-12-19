import os
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_HOST = os.environ.get("MQTT_HOST")
TEMP_THRESHOLD = float(os.environ.get("TEMP_THRESHOLD"))
MIN_OFF_TIME = float(os.environ.get("MIN_OFF_TIME"))
current_state = "on"
last_state_switch = datetime.now().timestamp()

def on_connect(client, userdata, flags, rc):
  print(F'Connected to {MQTT_HOST}')
  client.subscribe([("house/temp/0", 0)])


def on_temperature(client, userdata, message):
  temperature = float(message.payload)
  print(F'Temperature: {temperature}')
  new_state = "on"
  if temperature >= TEMP_THRESHOLD:
    new_state = "off"
  if new_state != current_state:
    if new_state == "on" and datetime.now().timestamp() > last_state_switch + MIN_OFF_TIME:
      current_state = "on"
      last_state_switch = datetime.now().timestamp()
      print(F'Set state to: {current_state}')
    elif new_state == "off":
      current_state = "off"
      last_state_switch = datetime.now().timestamp()
      print(F'Set state to: {current_state}')

  client.publish("house/fireplace/set_state", payload=current_state)


client = mqtt.Client(client_id="fireplace-controller")
client.on_connect = on_connect
print(F'Connecting to {MQTT_HOST}')
client.connect(MQTT_HOST)
client.message_callback_add("house/temp/0", on_temperature)
client.loop_forever()