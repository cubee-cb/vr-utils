"""
ALVRConnectionOSC

Small program to send an OSC message with a BOOL value when a headset connects or disconnects to ALVR, describing its current connection status.

Setup:
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json if you're feeling special)
- Change the "On Connect Script" and "On Disconnect Script" options to contain the *absolute* path to the script.bat file.
  - Linux users: make a .sh file that runs connection.py and use that. I trust you know at least how to do that. I have no Linux VR setup at the moment so I can't test.

https://github.com/attwad/python-osc
"""

# import libraries and set constants
import os
#from tkinter import messagebox
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

PROJECT = "ALVR Connection OSC"
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


# main code below

# set up udp client for sending data to vrchat
client = udp_client.SimpleUDPClient(GAME_IP, GAME_PORT)

# run on connection
if (os.getenv('ACTION') == CONNECTED):
  client.send_message(CONNECTION_PARAMETER, True)
  if (USE_CHATBOX):
    # send an empty string so the chatbox disappears
    client.send_message("/chatbox/input", ["", True, False])

# run on disconnection
elif os.getenv('ACTION') == DISCONNECTED:
  client.send_message(CONNECTION_PARAMETER, False)
  if (USE_CHATBOX):
    client.send_message("/chatbox/input", ["[Headset Disconnected]", True, False])
  
# unknown action; future-proofing in case someone puts it in a future ALVR slot it's not supposed to be in.
#else:
#  messagebox.showwarning(PROJECT + " - Unknown Action", "Action \"" + os.getenv('ACTION', "<None>") + "\" is unsupported. You should check if there's a script update available to handle this action.")

