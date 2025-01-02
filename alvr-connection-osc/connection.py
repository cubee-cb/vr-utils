#!/usr/bin/env python3
"""
ALVRConnectionOSC

Small program to send an OSC message with a BOOL value when a headset connects or disconnects to ALVR, describing its current connection status.

Setup:
- Make sure python3 and python3-pip are installed.
- Install PythonOSC with `pip install python-osc`
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json)
- Change the "On Connect Script" and "On Disconnect Script" options to contain:
  - Windows: the absolute path to the script.bat file. (C:/Users/.../.../script.bat)
  - Linux: the absolute path to this file. Untested.

https://github.com/attwad/python-osc
"""

# import libraries and set constants
import os
#from tkinter import messagebox
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

PROJECT = "ALVRConnectionOSC"
CONNECTED = "connect"
DISCONNECTED = "disconnect"


# change the following to match your setup

# streaming software display name.
STREAMER = "ALVR"

# leave this unless the target game is running on a different device.
GAME_IP = "127.0.0.1"

# the port the game is using to take in OSC messages.
#GAME_PORT = 9086 # custom port for routing
GAME_PORT = 9000

# the address to write to, set to true when the headset is connected, false when disconnected.
# for vrchat avatars, set to a BOOL parameter like "/avatar/parameters/<parameter>"
# CONNECTION_PARAMETER = "/avatar/parameters/VRCOSC/OpenVR/HMD/Connected"
CONNECTION_PARAMETER = "/avatar/parameters/hardware/headsetConnected"

# if true, send a chatbox message when the headset loses or regains connection
USE_CHATBOX = True

def chat(message):
  if (USE_CHATBOX):
    client.send_message("/chatbox/input", [message, True, False])


# main code below

# set up udp client for sending data to vrchat
client = udp_client.SimpleUDPClient(GAME_IP, GAME_PORT)

# run on connection
if (os.getenv('ACTION') == CONNECTED):
  client.send_message(CONNECTION_PARAMETER, True)
  # send an empty string to make the chatbox disappear
  chat("")

# run on disconnection
elif os.getenv('ACTION') == DISCONNECTED:
  client.send_message(CONNECTION_PARAMETER, False)
  # send disconnection message
  chat("[Headset Disconnected]")

# no action specified
elif os.getenv('ACTION') == None:
  # send error message
  message = "No action specified. (got \"" + os.getenv('ACTION', "<None>") + "\")"
  print(message)
  chat(message)

# unknown action; future-proofing in case someone puts it in a future ALVR slot it's not supposed to be in, or ALVR starts sending new actions.
else:
  # send error message
  message = "Action \"" + os.getenv('ACTION', "<None>") + "\" is unsupported. You should check if there's a new script available to handle this action."
  print(message)
  chat("Unsupported action: \"" + os.getenv('ACTION', "<None>") + "\"")

