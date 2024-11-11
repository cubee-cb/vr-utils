## ALVRConnectionOSC - OSC headset connection status updates for ALVR

A small program to send an OSC message with a BOOL value when a headset connects to or disconnects from ALVR, so things can match state. Useful for example if you have an unstable connection or need to leave intermittently.

By default it is set up to set a VRChat avatar parameter "hardware/headsetConnected" (Bool), which your avatar can be set up read to enter an "away" or "error" state to let other people know you can't hear or see them anymore.
As an example, my personal avatar plays a sound and flashes the outline red, then changes to a Resonite-style away material when I disconnect.

In addition, it (by default) sends a chatbox message "\[Headset Disconnected\]" and clears it when the connection is restored so you don't *need* specific avatar setup.

Setup:
- Make sure you have Python and PythonOSC installed. (pip install python-osc)
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json, that works too)
- Change both the "On Connect Script" and "On Disconnect Script" options to contain the *absolute* path to the script.bat file.
	- Windows users: this could be something like "C:\\Users\\user\\...\\alvr_streamer_windows\\script\\script.bat"
	- Linux users: make a .sh file that runs connection.py and use that instead. I trust you know at least how to do that. My current Linux VR setup doesn't use SteamVR or ALVR so I can't test unfortunately.

You can edit the script to change basic functionality, there are some variables near the top of "connection.py" with descriptive comments so they should be easy to find.

Known Issues:
- At the moment on Windows it pops up a Command window whenever it runs. I do not know how to prevent this.


## HMD Battery Test

A set of tests to check avatar setup for battery-displaying functionality on VRChat avatars, for example: using my [Battery Prefab](https://cubee.gumroad.com/l/battery-indicator).

Contains tests:
- Set battery to Full
- Set battery to Empty (may not work, don't know which part of the chain is broken yet)
- Charge test (0 to 100)
- Discharge test (100 to 0)
- Clear battery - set to a negative value so the avatar can know there is no battery
- OVR Toolkit integration: connected with battery full
- OVR Toolkit integration: connected only - no battery sent
- Disconnect OVR Toolkit integration (sets integration parameters to 255)

Some prefabs or avatars may support connected without battery status - this is what the OVR connected with no battery test is for.
This is because OVR Toolkit may not always set the battery parameter, for example while at 100% or briefly after changing avatars.
They may display a "loading" indicator until they receive a battery level to at least show the connection is working.

My batteries use the following parameters:
- battery/hmd - the level shown on the batteries
- battery/visible - if the battery indicator should be shown or not
- battery/connected (optional) - if the provider is connected but may not be sending battery yet

battery/hmd may be set without battery/connected being set - this is fine. My prefabs/avatars that support it will just go directly to the battery level animation instead of showing the connection animation first.

## OSC Sender

A small script to send singular OSC values to specific addresses. That's it.
By default prepends "/avatar/parameters/" to all messages - this can be changed.



Scripts use Python OSC:
https://github.com/attwad/python-osc
