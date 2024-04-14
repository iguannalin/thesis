# this will run on one node that will be the server

# Webserver to send RGB data
# Tony Goodhew 5 July 2022
import network
import socket
import time
from machine import Pin, ADC, PWM
from secret import ssid,password
import random
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

pwm = PWM(Pin(28))

pwm.freq(1000)
led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)
       
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

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

def send_request(msg):
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        
        response = msg

        cl.send(response)
        print("Sent:" + response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

    
# Listen for connections
duty = 0
while True:
    if (duty==0):
        duty = 65025
    else:
        duty = 0
    send_request(str(duty))
    pwm.duty_u16(duty)
    time.sleep(0.1)