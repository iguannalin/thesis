# Save this as main.py on the pico that will be the CLIENT node

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
while not wlan.isconnected() and wlan.status() >= 0:
    # print("Waiting to connect:")
    led.value(1)
    time.sleep(1)
    led.value(0)
 
# Should be connected and have an IP address
wlan.status() # 3 == success
wlan.ifconfig()
led.value(1)
# print(wlan.ifconfig()[0][-1])

# *
# * CAPACITIVE TOUCH
# *

machine.freq(125_000_000)

@rp2.asm_pio(set_init=[rp2.PIO.OUT_LOW])
def capsense():
    mov(isr,null)
    
    # set y to the sample period count, by shifting in a 1 and a bunch of 0s
    set(y, 1)
    in_(y, 1)
    in_(null, 20)
    mov(y, isr)
    
    # clear the counter
    mov(x, invert(null))
    
    label('resample')

    # set pin to input...
    set(pindirs, 0)
    
    label('busy')
    # ...and wait for it to pull high
    jmp(pin, 'high')
    jmp(y_dec, 'busy')
    jmp('done')
    
    label('high')
    # set pin to output and pull low
    set(pindirs, 1)
    set(pins, 0)
    
    # while that's going on, count the time spent outside of the busy loop
    jmp(y_dec, 'dec1')
    jmp('done')
    label('dec1')
    jmp(y_dec, 'dec2')
    jmp('done')
    label('dec2')
    jmp(y_dec, 'dec3')
    jmp('done')
    label('dec3')
    jmp(y_dec, 'dec4')
    jmp('done')
    label('dec4')
    jmp(y_dec, 'dec5')
    jmp('done')
    label('dec5')
    
    # count this cycle and repeat
    jmp(x_dec, 'resample')
    
    
    label('done')
    # time's up - push the count
    mov(isr,x)
    push(block)

u32max = const((1<<32)-1)

class Channel:
    def __init__(self, pin, sm):
        self.warmup = 100
        
        self.level = 0
        self.level_lo = u32max
        self.level_hi = 0
        
        machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.state_machine = rp2.StateMachine(sm, capsense, freq=125_000_000, set_base=machine.Pin(pin), jmp_pin=machine.Pin(pin))
        self.state_machine.active(1)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.active(0)
            
    def active(self, active):
        self.state_machine.active(active)

    @micropython.native
    def update(self):
        if self.state_machine.rx_fifo() > 0:
            for f in range(5):
                level = u32max - self.state_machine.get()
                
                if self.state_machine.rx_fifo() == 0:
                    break
                
            if self.warmup > 0:
                self.warmup -= 1
            else:
                self.level_lo = min(level, self.level_lo)
                self.level_hi = max(level, self.level_hi)
                
            window = self.level_hi - self.level_lo
                
            if window > 64:
                self.level = 1 - ((level - self.level_lo) / window)
       
class Device:
    def __init__(self, pins):
        self.channels = []
        for i in range(len(pins)):
            self.channels.append(Channel(pins[i], i))
            
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        for c in self.channels:
            c.active(0)
            
    def update(self):
        for c in self.channels:
            c.update()
            
    def level(self, channel):
        return self.channels[channel].level

# motor pin
pwm = machine.PWM(machine.Pin(28))
pwm2 = machine.PWM(machine.Pin(27))
pwm.freq(1000)
pwm2.freq(1000)
# cap. touch pins
caps = [0, 4]
PWM_MAX = 65025

# self test
def main():
    touched = False
    with (Device(caps)) as touch:
        while True:
            addr = socket.getaddrinfo("192.168.1.5", 80)[0][-1] # Address of Web Server

            # Create a socket and make a HTTP request
            s = socket.socket() # Open socket
            s.connect(addr)
            s.send(b"HI from " + wlan.ifconfig()[0][-1]) # Send request
            ss=str(s.recv(512)) # Store reply
            # print(ss)

            # Listen for messages from SERVER
            if ss:
                # Print what we received
                print(ss)
                if len(ss)>3:
                    ss=ss[2:-1] # Store reply
                    if int(ss):
                        print('received: ', ss)
                        pwm.duty_u16(int(ss))
                        pwm2.duty_u16(int(ss))
                else:
                    pwm.duty_u16(0)
                    pwm2.duty_u16(0)
                    touch.update()
                    print('received zero ', ss)
                    #print('\r', end='')
                    for c in touch.channels:
                        print(c.level)
                        if (c.level > 0.5):
                            touched = True
                        elif (not touched and c.level <= 0.5):
                            touched = False
                    # Otherwise, listen for touch and send to SERVER
                    if touched:
                        scale = min(PWM_MAX, int(c.level*PWM_MAX))
                        pwm.duty_u16(scale)
                        pwm2.duty_u16(scale)
                        print('sent: ', scale)
                        s.send(b"" + str(scale))
                    

            s.close()          # Close socket
            time.sleep(0.03)

if __name__ == '__main__':
    main()
