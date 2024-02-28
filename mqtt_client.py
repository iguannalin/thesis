import paho.mqtt.client as mqtt
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
NODE = "P1"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ITPtest")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if (NODE in str(msg.payload)):
        led.value = True # light when button is pressed!
        time.sleep(1) # sleep 2 for p2
        led.value = False

mqttc = mqtt.Client(NODE)
# mqttc.username_pw_set("theyonetwork","ConnDevSP24")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# broker.hivemq.com
mqttc.connect("broker.hivemq.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# mqttc.loop()

while True:
    mqttc.loop()
    # mqttc.publish("ITPtest", "P1")
    time.sleep(1)
    if not button.value:
      led.value = True
      if NODE == "P1":
        mqttc.publish("ITPtest", "P2")
      else:
        mqttc.publish("ITPtest", "P1")
      led.value = False
