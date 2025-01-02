#!/usr/bin/env python3
"""
OSC sender

send arbitrary values to arbitrary avatar parameters

https://github.com/attwad/python-osc
"""

from tkinter import messagebox
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

# change the following to match your setup

# leave this unless the target game is running on a different device.
GAME_IP = "127.0.0.1"

# the port the game is using to take in OSC messages.
GAME_PORT = 9000

# the root address to prepend to sent addresses.
PARAMETER_ROOT = "/avatar/parameters/"

# if true, send a chatbox message when the headset loses or regains connection
USE_CHATBOX = True

# send OSC message, print to output, and send message to VRChat chatbox if enabled
def send(addr, param):
  myAddr = PARAMETER_ROOT + str(addr)
  client.send_message(myAddr, param)


  message = "set \"" + myAddr + "\" to \"" + str(param) + "\" " + str(type(param))
  print(message)
  if (USE_CHATBOX):
    client.send_message("/chatbox/input", [message, True, False])

# set up udp client for sending data to vrchat
client = udp_client.SimpleUDPClient(GAME_IP, GAME_PORT)

print("format: <address> <value>")
print("attempts to convert value into an int, float, or bool in that order")
print("target addresses - " + GAME_IP + ":" + str(GAME_PORT) + " - OSC " + PARAMETER_ROOT)

while True:
  percent = 100
  inp = str(input("send > ")).split(" ")

  if (len(inp) < 2):
    print("two values required, separated by a single space.")
    continue

  addr = inp[0]
  value = inp[1]

  # poor coding - this could be done way better
  # try convert to int
  try:
    value = int(value)

  except:
    # try convert to float
    try:
      value = float(value)

    except:
      # try convert to bool
      if (value in ["true", "True"]):
        value = True

      if (value in ["false", "False"]):
        value = False

  # send value to address
  send(addr, value)
