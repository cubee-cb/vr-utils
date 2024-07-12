## ALVRConnectionOSC - OSC headset connection status updates for ALVR

Small program to send an OSC message with a BOOL value when a headset connects or disconnects to ALVR, describing its current connection status.

By default it is set up to set a VRChat avatar parameter "hardware/headsetConnected" (Bool), which your avatar can be set up read to enter an "away" or "error" state to let other people know you can't hear them anymore.
In addition, it sends a chatbox message "\[Headset Disconnected\]" and clears it when the connection is restored so you don't *need* specific avatar setup.
My personal avatar plays a sound, briefly flashes thee outline red and changes to a Resonite-style away material when I disconnect.

Setup:
- Make sure you have Python in your PATH as well as PythonOSC installed.
	- Open a command line and run "python --version" to check. If there's no red text, you should be good to go.
- Place the script files somewhere ALVR can get to. (inside the ALVR executable's folder is fine)
- Open ALVR's config screen. (or session.json if you're feeling special)
- Change both the "On Connect Script" and "On Disconnect Script" options to contain the *absolute* path to the script.bat file.
	- In my case on Windows this would be "C:\Users\<user>\Programs\alvr_streamer_windows\script\script.bat"
	- Linux users: make a .sh file that runs connection.py and use that instead. I trust you know at least how to do that. I have no Linux VR setup at the moment so I can't test, though that is in the works.

You can edit the script to change basic functionality, there are some variables near the top with descriptive comments so they should be easy to find.

Uses Python OSC:
https://github.com/attwad/python-osc

Known Issues:
- At the moment it pops up a Command window whenever it runs. I'll investigate workarounds.
