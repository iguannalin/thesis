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

addies = [] # addresses i.e. 192.x.x
baddies = [] # tuples i.e. (192.x.x, 60530)

print('listening on', addr)

def findBaddy(addy):
    for x,_ in baddies:
        if x == addy:
            return(x,_)

def ping_client(msg, baddy):
    print("pinging client", baddy)
    try:
        cl = s.connect(baddy)
        s.sendto(msg, baddy)
        cl.send(response)
        print("Sent:" + response)
        cl.close()

    except OSError as e:
        # cl.close()
        print('could not reach ', baddy)

def listen():
    try:
        cl, addr = s.accept()
        if (addr[0] not in addies):
            addies.append(addr[0])
            baddies.append(addr)
        print("addies ", addies)
        request = cl.recv(1024)
        print(request)
        
        # send touch to random client that is not the touched client
        if ("touched" in request):
            if len(addies) > 1:
                aIndex = addies.index(addr[0])
                addy = random.choice(addies[:aIndex-1]+addies[:aIndex])
                baddy = findBaddy(addy)
                ping_client("touched", baddy)
                print("***", addr[0], " touched ", baddy)
            
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

# self test
def main():
    touched = False
    while True:
        if is_connnected:
            listen()
            # for badd in baddies:
            #     ping_client("", badd)
            time.sleep(0.01)

if __name__ == '__main__':
    main()


