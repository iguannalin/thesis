# Program to read RGB values from a local Pico Web Server
# Tony Goodhew 5th July 2022
# Connect to network
import network
import time
from secret import ssid, password
import socket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# set up a server on this client as well
# Open socket
address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(address)
s.listen(1)

print('listening on', address)

while True:
    try:
        cl, address = s.accept()
        print('client connected from', address)
        request = cl.recv(1024)
        print(request)

        response = "hello" # This is what we send in reply
        cl.send(response)
        print("Sent:" + response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

    ai = socket.getaddrinfo("192.168.0.15", 80)[0][-1] # Address of other node's Web Server

    # Create a socket and make a HTTP request
    so = socket.socket() # Open socket
    so.connect(ai)
    so.send(b"GET Data") # Send request
    ss=str(so.recv(512)) # Store reply
    # Print what we received
    print(ss)
    # Set RGB LED here
    so.close()          # Close socket
    time.sleep(0.2)    # wait
