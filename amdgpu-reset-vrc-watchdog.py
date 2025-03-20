#!/usr/bin/env python3
"""
OSC sender

detects when amdgpu decides it's reset time,
then sets avatar parameter "dead" to true so
my avatar can do funny explode when my gpu dies

cause it's dumb and keeps resetting for some reason

https://github.com/attwad/python-osc
"""

from time import sleep
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
from systemd import journal
from datetime import datetime, timedelta, timezone

# change the following to match your setup

# the root address to prepend to sent addresses.
PARAMETER_ROOT = "/avatar/parameters/"


# set up udp client for sending data to vrchat
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

j = journal.Reader()

# this is called by cron every minute, so we only loop for one minute
for i in range(1, 59):
  # check journal to see if amdgpu is resetting
  reset = False
  resetType = "Error"
  resetMessage = "uhhh"
  messages = 0

  since = datetime.now().astimezone() - timedelta(seconds=1)
  until = datetime.now().astimezone()
  j.seek_realtime(since)

  for entry in j:
    if entry['__REALTIME_TIMESTAMP'] > until:
      continue

    message = entry['MESSAGE']
    #print(message)
    messages += 1

    if "reset" in message and "amdgpu" in message and ("timeout" in message or "page fault" in message):
      resetType = "GPU reset; will crash momentarily"
      resetMessage = message
      reset = True

    elif "0" in message and False:
      resetType = "test case"
      reset = True

  # tell vrc if a reset happened so avatar can die peacefully
  if reset:
    print("Reset detected!!! (" + resetType + ")")
    print("Got: " + resetMessage)
    # send value to address
    client.send_message(PARAMETER_ROOT + "dead", True)
    client.send_message("/chatbox/input", ["[" + resetType + "]", True, False])
    print("Parameters sent, exiting.")
    exit(0)
  else:
    print("Iteration " + str(i) + ": Checked " + str(messages) + " entries. Ok.")

  sleep(1)
