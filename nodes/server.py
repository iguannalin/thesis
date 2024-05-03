# Save this as main.py on the pico that will be the SERVER node

# Program to read RGB values from a local Pico Web Server:
# Tony Goodhew 5th July 2022
# Program for capacitive touch on micropython:
# https://github.com/AncientJames/jtouch/tree/main

import network
import socket
import time
import machine
import rp2
import random
from secret import ssid,password

# turn board LED on
led = machine.Pin("LED", machine.Pin.OUT)

# *
# * NETWORK CONNECTION
# *

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
is_connnected = False

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if max_wait % 2 == 0:
        led.value(1)
    else:
        led.value(0)
    #print(wlan.status())
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    #print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    led.value(1)
    is_connnected = True
    #print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

def ping_client(msg, addy):
    try:
        cl = s.connect(addy)
        s.sendto(msg, addy)
        cl.send(response)
        print("Sent:" + response)
        cl.close()

    except OSError as e:
        cl.close()
        #print('connection closed')

def listen():
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        print("addresses", addresses)
        if (addr[0] not in addresses):
            addresses.append(addr[0])
        request = cl.recv(1024)
        print(request)
        if ("touched" in request):
            addy = random.choice(addresses)
            while addy != addr[0] and len(addresses) > 1:
                addy = random.choice(addresses)
            # send touch to random client that is not the touched client
            ping_client("touched", addy)
        cl.send(response)
        print("Sent:" + response)
        cl.close()

    except OSError as e:
        cl.close()
        #print('connection closed')

addresses = []
# self test
def main():
    touched = False
    while True:
        if is_connnected:
            listen()
            for add in addresses:
                ping_client("", add)
            time.sleep(0.01)

if __name__ == '__main__':
    main()

