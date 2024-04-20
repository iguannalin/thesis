# Webserver to send RGB data
# Tony Goodhew 5 July 2022
# server1.py
import network
import socket
import time
from machine import Pin, ADC
from secret import ssid,password
import random

led = machine.Pin("LED", machine.Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if max_wait % 2 == 0:
        led.value(1)
    else:
        led.value(0)
    # print(wlan.status())
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    # print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)
print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        # Do not unpack request
        # We reply to any request the same way
        # Generate 3 values to send back
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        # Join to make a simple string with commas as separators
        rgb = str(r) + "," + str(g) + ","+str(b)
        
        response = rgb # This is what we send in reply

        cl.send(response)
        print("Sent:" + rgb)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')



