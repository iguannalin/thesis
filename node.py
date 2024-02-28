# raspberry.local

import requests
from flask import Flask, request

import board
import digitalio

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

app = Flask(__name__)

send = False

@app.route("/listen/")
def listen():
  print("listening ...")
  if request and request.args:
    id = request.args.get('id')
    if id:
      print(id)
  return "<p>Hello, World!</p>"

def buttonPress(pressed):
  led.value = pressed
  if pressed:
    shout()

@app.route("/shout/")
def shout():
  requests.get("http://192.168.1.2:5000/listen/?id=2")
  return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # listen()
    # while True:
    #   buttonPress(not button.value)
    # shout()
