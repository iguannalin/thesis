# Program to read RGB values from a local Pico Web Server
# Tony Goodhew 5th July 2022
# Connect to network
import network
import socket
import time
from machine import Pin, ADC

from secret import ssid, password

led = machine.Pin("LED", machine.Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)
 
# Should be connected and have an IP address
wlan.status() # 3 == success
wlan.ifconfig()
print(wlan.ifconfig()[0][-1])

while True:
    led.value(0)
    addr = socket.getaddrinfo("192.168.1.3", 80)[0][-1] # Address of Web Server

    # Create a socket and make a HTTP request
    s = socket.socket() # Open socket
    s.connect(addr)
    s.send("HI FROM " + wlan.ifconfig()[0][-1]) # Send request
    ss=str(s.recv(512)) # Store reply
    # Print what we received
    # print(ss)
    if ss:
        led.value(1)
    # Set RGB LED here
    s.close()          # Close socket
    time.sleep(0.7)    # wait


