"""
ALVRHiccupOSC

Small program to send an OSC message with a BOOL value when a headset connects or disconnects to ALVR, describing its current connection status.

Setup:
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json if you're feeling special)
- Change the "On Connect Script" and "On Disconnect Script" options to contain the *absolute* path to the script.bat file.
  - Linux users: make a .sh file that runs connection.py and use that. I trust you know at least how to do that. I have no Linux VR setup at the moment so I can't test.

https://github.com/attwad/python-osc
"""

import os
import time
from tkinter import messagebox
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

PROJECT = "battery test"
CONNECTED = "connect"
DISCONNECTED = "disconnect"


# change the following to match your setup

# streaming software display name.
STREAMER = "ALVR"

# leave this unless the target game is running on a different device.
GAME_IP = "127.0.0.1"

# the port the game is using to take in OSC messages.
GAME_PORT = 9000

# the address to write to, set to true when the headset is connected, false when disconnected.
# for vrchat avatars, set to a BOOL parameter like "/avatar/parameters/<parameter>"
# CONNECTION_PARAMETER = "/avatar/parameters/VRCOSC/OpenVR/HMD/Battery"
CONNECTION_PARAMETER = "/avatar/parameters/battery/level"

# if true, send a chatbox message when the headset loses or regains connection
USE_CHATBOX = True


def chat(message):
  print(message)
  client.send_message("/chatbox/input", [message, True, False])

# main

# set up udp client for sending data to vrchat
client = udp_client.SimpleUDPClient(GAME_IP, GAME_PORT)

while True:
  percent = 100
  print("1 to set full, 2 for empty, 3 for charge test, 4 for drain test, 5 for disconnect battery.")
  inp = int(input("> ") or "-1")

  if (inp == 1):
    chat("batt set to full")
    client.send_message(CONNECTION_PARAMETER, 1)

  elif (inp == 2):
    chat("batt set to empty")
    client.send_message(CONNECTION_PARAMETER, 0)

  elif (inp == 3):
    chat("charge test")
    time.sleep(1)
    percent = 0

    while (percent <= 100):
      valueSent = percent / 100
      client.send_message(CONNECTION_PARAMETER, valueSent)

      # don't spam the chatbox
      if (percent % 25 == 0):
        chat("batt " + str(percent) + "%" + "(" + str(valueSent) + ")")

      time.sleep(0.1)
      percent += 1

  elif (inp == 4):
    chat("drain test")
    time.sleep(1)

    while (percent >= 0):
      valueSent = percent / 100
      client.send_message(CONNECTION_PARAMETER, valueSent)

      # don't spam the chatbox
      if (percent % 25 == 0):
        chat("batt " + str(percent) + "%" + "(" + str(valueSent) + ")")

      time.sleep(0.1)
      percent -= 1

  elif (inp == 5):
    chat("disconnect battery test")
    client.send_message(CONNECTION_PARAMETER, -0.9)

