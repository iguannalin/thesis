# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# def button_callback(channel):
#     print("Button was pushed!")
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
# message = input("Press enter to quit\n\n") # Run until someone presses enter
# GPIO.cleanup() # Clean up


import time  
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep

GPIO.setmode(GPIO.BCM) 

touchSwitch = 27  
# outputPin = 27  

# # led = LED(27)

GPIO.setup(touchSwitch, GPIO.IN)
# GPIO.setup(outputPin, GPIO.OUT)  
# GPIO.output(outputPin, False)  

# # while True:
# #     led.on()
# #     sleep(1)
# #     led.off()
# #     sleep(1)

while True:  
    switchTouched = GPIO.input(touchSwitch)  

    if switchTouched:  
      print("touch detected")
      time.sleep(0.3) # sleep again here so not to toggle the lamp to quickly  
    else:  
      print("not touched")

    time.sleep(0.15) # 0.10 seems to give the best results but 0.15 uses less CPU  