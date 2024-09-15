## ALVRConnectionOSC - OSC headset connection status updates for ALVR

A small program to send an OSC message with a BOOL value when a headset connects or disconnects to ALVR, describing its current connection status.

By default it is set up to set a VRChat avatar parameter "hardware/headsetConnected" (Bool), which your avatar can be set up read to enter an "away" or "error" state to let other people know you can't hear or see them anymore.
As an example, my personal avatar plays a sound and flashes the outline red, then changes to a Resonite-style away material when I disconnect.

In addition, it sends a chatbox message "\[Headset Disconnected\]" and clears it when the connection is restored so you don't *need* specific avatar setup.

Setup:
- Make sure you have Python and PythonOSC installed.
- Place the script files somewhere ALVR can get to. (inside the ALVR executable's folder is fine)
- Open ALVR's config screen. (or session.json if you're feeling special)
- Change both the "On Connect Script" and "On Disconnect Script" options to contain the *absolute* path to the script.bat file.
	- Windows users: this would be something like "C:\\Users\\<user>\\Programs\\alvr_streamer_windows\\script\\script.bat"
	- Linux users: make a .sh file that runs connection.py and use that instead. I trust you know at least how to do that. I don't have a VR setup on Linux at the moment so I can't test unfortunately.

You can edit the script to change basic functionality, there are some variables near the top of "connection.py" with descriptive comments so they should be easy to find.

Known Issues:
- At the moment on Windows it pops up a Command window whenever it runs. I don't know how to stop this.

## HMD Battery Test

A small set of tests to check avatar setup for battery-displaying functionality on avatars, like my [Battery Prefab](https://cubee.gumroad.com/l/battery-indicator).



Scripts use Python OSC:
https://github.com/attwad/python-osc
