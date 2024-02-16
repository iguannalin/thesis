# raspberry.local

import asyncio
import requests
from flask import Flask, request

app = Flask(__name__)

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
  requests.get("http://172.20.10.7:5000/listen/?id=1")
  return "<p>Hello, World!</p>"

asyncio.run(listen())
# shout()