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

  if "keygen" in sys.argv:
    print("Generating ADB key.")
    keygen(key_path)
    print("Done!")
    sys.exit(1)

  ADB_USB = sys.argv[1].lower() != "wireless"
  if len(sys.argv) > 2:
    if "." in sys.argv[2]:
      DEVICE_IP = sys.argv[2]
  if len(sys.argv) > 3:
    try:
      OSC_PORT = int(sys.argv[3])
    except:
      OSC_PORT = OSC_PORT

  if "verbose" in sys.argv:
    VERBOSE = True

# Load the public and private keys
with open(key_path) as f:
  priv = f.read()
with open(key_path + '.pub') as f:
  pub = f.read()
signer = PythonRSASigner(pub, priv)
print("Loaded ADB key.")

print("==", PROJECT, "==")
print("Talking to", DEVICE_IP, "over OSC:" + str(OSC_PORT), ADB_USB and "and USB ADB" or ("and ADB:" + str(ADB_PORT)))

# connect to device over adb
device = False
try:
  device = ADB_USB and AdbDeviceUsb() or AdbDeviceTcp(DEVICE_IP, ADB_PORT, default_transport_timeout_s=9.)
except:
  print("Device not found.")
  sys.exit(1)

try:
  device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
except ConnectionRefusedError:
  print("Connection refused! Is wireless debugging enabled?")
  sys.exit(1)
except:
  print("Failed to connect to ADB device.")
  print(ADB_USB and "Is USB Debugging enabled? Is there another ADB server running? Try \"adb kill-server\" to close it. (may kill WiVRn if running)" or "Some unknown error.")
  sys.exit(1)

# set up udp client for sending osc data to vrchat
try:
  client = udp_client.SimpleUDPClient(DEVICE_IP, OSC_PORT)
except:
  print("Couldn't start OSC client. Is pythonosc installed? Did you pass a valid IP and Port?")
  sys.exit(1)

loops = 0
failed_loops = 0
while True:
  #proc = subprocess.check_output(["adb", "shell", "dumpsys", "battery", "|", "grep", "level"])
  #proc = proc.strip().split(b":")[1].strip()
  #percent = int(proc)
  #print(percent)

  #proc = subprocess.check_output(["adb", "shell", "dumpsys", "battery", "|", "grep", "powered"])
  #charging = proc.find(b"true") >= 0
  #print(charging)


  # let the avatar know an "overlay" is connected
  # this parameter should default to 255 on the avatar,
  #   so it can detect when the overlays set it to 0, 1, 2, etc...
  if loops % TIMER_CONNECTION == 0:
    client.send_message(PARAMETER_OVERLAYS, 0)


  # poll the device for new information and forward it to vrchat
  if loops % TIMER_POLL_BATTERY == 0:

    # get raw data from the adb device
    try:
      battery_data_raw = device.shell("dumpsys battery")

      # process battery data into a dictionary
      battery_data = {}
      for line in battery_data_raw.split("\n"):
        split_data = line.strip().split(": ")
        if len(split_data) == 2:
          key, value = split_data[0].lower(), split_data[1]
          battery_data[key] = value
          if VERBOSE:
            print(key, "-", value)

      # now we can use the values easily!
      percent = int(battery_data.get("level")) or 255
      charging = bool(battery_data.get("ac powered")) or bool(battery_data.get("usb powered")) or bool(battery_data.get("wireless powered"))

      print(f"Got battery level: {percent}% (Charging: {charging})")

      #chat("batt set to full")
      client.send_message(PARAMETER_BATTERY, percent / 100.0)
      client.send_message(PARAMETER_CHARGE, charging)

      failed_loops = 0

    except:
      print("Couldn't get data from device!")
      failed_loops += 1
      if failed_loops >= 3:
        print("Stopping.")
        sys.exit(1)

  # loop once per second
  time.sleep(1)
  loops += 1
