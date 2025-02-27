#!/usr/bin/env python
"""
Snitch
by cubee

gets the active window and sends osc when it changes, plus periodically to keep the chatbox active.

using:
pythonosc: https://pypi.org/project/python-osc/
"""

INCOGNITO = True


import time
from pythonosc import udp_client
import subprocess

PROJECT = "Snitch"

# change the following to match your setup

# set this to the address of the device running vrchat.
DEVICE_IP = "127.0.0.1"

# ports used to talk to the osc receiver and the android device itself
OSC_PORT = 9000 # default: 9000

# the address to write to, to tell if vrchat is currently focused
PARAMETER_FOCUS = "/avatar/parameters/focus"

# timers for sending things, seconds
TIMER_POLL_FOCUS = 0.1 # interval to poll the active window
TIMER_SEND_OSC = 10 # interval to send the window state over osc

# main

import sys
from os import path

# are we running in executable mode?
frozen = getattr(sys, 'frozen', False)
exec_root = frozen and path.dirname(sys.executable) or path.dirname(path.realpath(__file__))

print("==", PROJECT, "==")
print("Talking to", DEVICE_IP, "over OSC:" + str(OSC_PORT))

# set up udp client for sending osc data to vrchat
try:
  client = udp_client.SimpleUDPClient(DEVICE_IP, OSC_PORT)
except:
  print("Couldn't start OSC client. Is pythonosc installed? Did you pass a valid IP and Port?")
  sys.exit(1)

def send_osc():
  print(f"Got window: {window_name} (is vrchat? {is_vrc})")
  text = not is_vrc and f"Unfocused: using {window_name}." or ""

  client.send_message(PARAMETER_FOCUS, is_vrc)
  client.send_message("/chatbox/input", [text, True, False]) # text, submit, sound

loop_interval = 1
loops = 0
failed_loops = 0
window_name = "VRChat"
window_name_last = window_name
is_vrc = True
while True:

  # poll for active window and forward it to vrchat
  if loops % (TIMER_POLL_FOCUS / loop_interval) == 0:

    # get raw data from the adb device
    try:
      proc = subprocess.check_output(["kdotool", "getactivewindow", "getwindowname"], text=True)
      window_name = proc.strip()
      is_vrc = window_name == "VRChat"

      if INCOGNITO and not is_vrc:
        window_name = "another application"

      # send an immediate update if the focused window changes
      if window_name_last != window_name:
        send_osc()
        window_name_last = window_name

      failed_loops = 0

    except:
      print("Loop failed!")
      failed_loops += 1
      if failed_loops >= 3:
        print("Stopping.")
        sys.exit(1)

  # periodically update the chatbox
  if not is_vrc and loops % (TIMER_SEND_OSC / loop_interval) == 0:
    send_osc()

  time.sleep(loop_interval)
  loops += 1
