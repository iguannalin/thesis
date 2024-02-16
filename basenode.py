# raspberry.local

import asyncio
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
async def listen():
  print("listening ...")
  if request and request.args:
    id = request.args.get('id')
    if id:
      print(id)
  return "<p>Hello, World!</p>"

@app.route("/shout/")
def shout():
  # if not button.value:
    # requests.get("http://172.20.10.7:5000/listen/?id=1")
  return "<p>Hello, World!</p>"

asyncio.run(listen())
while True:
  if not button.value:
    send = True
  if send:
    requests.get("http://172.20.10.7:5000/listen/?id=1")
    send = False