#!/usr/bin/env python
"""
by cubee

pass "keygen" ("script.py keygen") to re-generate the keys if needed.
pass "verbose" ("script.py verbose") to print out all battery info returned from adb.

using:
pythonosc: https://pypi.org/project/python-osc/
adb_shell: https://github.com/JeffLIrion/adb_shell
"""


import time
from pythonosc import udp_client
#import subprocess

PROJECT = "ADB-OSC Battery Relay"

# change the following to match your setup

# set this to the address of the device running vrchat.
DEVICE_IP = "127.0.0.1"

# ports used to talk to the osc receiver and the android device itself
OSC_PORT = 9000 # default: 9000
ADB_PORT = 5555 # default: 5555

ADB_USB = True

# the address to write to, set to true when the headset is connected, false when disconnected.
# for vrchat avatars, set to a BOOL parameter like "/avatar/parameters/<parameter>"
PARAMETER_OVERLAYS = "/avatar/parameters/openOverlayCount" # WlxOverlay / int
PARAMETER_BATTERY = "/avatar/parameters/headsetBattery" # WlxOverlay / float
PARAMETER_CHARGE = "/avatar/parameters/headsetCharging" # WlxOverlay / bool

# timers for sending things, seconds
TIMER_POLL_BATTERY = 10 # interval to poll the device's battery level
TIMER_CONNECTION = 1 # interval to tell the game we are connected

# main

import sys
from os import path
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen

# are we running in executable mode?
frozen = getattr(sys, 'frozen', False)
exec_root = frozen and path.dirname(sys.executable) or path.dirname(path.realpath(__file__))

# keygen
key_path = path.join(exec_root, "adb_key")
if not path.exists(key_path):
  print("ADB key doesn't exist, generating.")
  keygen(key_path)

VERBOSE = False
if len(sys.argv) > 1:
  cmd = sys.argv[1]
  if cmd == "keygen":
    print("Generating ADB key.")
    keygen(key_path)
    print("Done!")
    sys.exit(1)
  elif cmd == "verbose":
    VERBOSE = True

# Load the public and private keys
with open(key_path) as f:
  priv = f.read()
with open(key_path + '.pub') as f:
  pub = f.read()
signer = PythonRSASigner(pub, priv)
print("Loaded ADB key.")

print("==", PROJECT, "==")
print("Talking to", ADB_USB and "USB Device" or DEVICE_IP, "over OSC:" + str(OSC_PORT), ADB_USB and "" or ("and ADB:" + str(ADB_PORT)))

# connect to device over adb
device = ADB_USB and AdbDeviceUsb() or AdbDeviceTcp(DEVICE_IP, ADB_PORT, default_transport_timeout_s=9.)
try:
  device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
except ConnectionRefusedError:
  print("Connection refused! Is wireless debugging enabled?")
  sys.exit(1)
except:
  print("Failed to connect to ADB device.")
  print(ADB_USB and "Is there another ADB server running? Try \"adb kill-server\" to close it. (may kill WiVRn if running)" or "Some unknown error.")
  sys.exit(1)

# set up udp client for sending osc data to vrchat
try:
  client = udp_client.SimpleUDPClient(DEVICE_IP, OSC_PORT)
except:
  print("Couldn't start OSC client. Is pythonosc installed?")
  sys.exit(1)

loops = 0
while True:
  #proc = subprocess.check_output(["adb", "shell", "dumpsys", "battery", "|", "grep", "level"])
  #proc = proc.strip().split(b":")[1].strip()
  #percent = int(proc)
  #print(percent)

  #proc = subprocess.check_output(["adb", "shell", "dumpsys", "battery", "|", "grep", "powered"])
  #charging = proc.find(b"true") >= 0
  #print(charging)


  # let the avatar's battery know an "overlay" is connected
  # we can do this since android HMDs don't do custom overlays,
  #   nor do their integrated dashboards use osc
  if loops % TIMER_CONNECTION == 0:
    client.send_message(PARAMETER_OVERLAYS, 1)


  # poll the device for new information and forward it to vrchat
  if loops % TIMER_POLL_BATTERY == 0:

    # get raw data from the adb device
    battery_data_adb = device.shell("dumpsys battery").split("\n")

    # process battery data into a dictionary
    battery_data = {}
    for line in battery_data_adb:
      split_data = line.strip().split(": ")
      if len(split_data) == 2:
        key, value = split_data
        battery_data[key] = value
        if VERBOSE:
          print(key, "-", value)

    # now we can use the values easily!
    percent = int(battery_data.get("level")) or 255
    charging = bool(battery_data.get("AC powered")) or bool(battery_data.get("USB powered")) or bool(battery_data.get("Wireless powered"))

    print(f"Got battery level: {percent}% (Charging: {charging})")

    #chat("batt set to full")
    client.send_message(PARAMETER_BATTERY, percent / 100.0)
    client.send_message(PARAMETER_CHARGE, charging)

  # loop once per second
  time.sleep(1)
  loops += 1
