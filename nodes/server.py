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
    print(wlan.status())
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    led.value(1)
    is_connnected = True
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
addresses = []
bars = ['⠀', '⡀', '⣀', '⣄', '⣤', '⣦', '⣶', '⣷', '⣿']
# self test
def main():
    while True:
        try:
            cl, addr = s.accept()
            add = addr[0]
            if (add in addresses):
                print('client connected from', add)
            else:
                print('new client', add)
                addresses.append(add)

            request = cl.recv(1024)
            # c = int(request)
            #print(f'   {bars[min(len(bars)-1, int(c * len(bars)))]}', end='')
            print(request)
            print("addresses", addresses)
            cl.send("HI")
            
            # response = msg

            # cl.send(response)
            # print("Sent:" + response)
            cl.close()

        except OSError as e:
            cl.close()
            print('connection closed')

if __name__ == '__main__':
    main()


