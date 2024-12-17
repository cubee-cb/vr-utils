## VR OSC Tools

A few tools I've made based on PythonOSC over my time playing VR, to help let others know about my status without having to tell them.


# ALVRConnectionOSC - OSC headset connection status updates for ALVR

A small program to send an OSC message with a BOOL value when a headset connects to or disconnects from ALVR, so things can match state. Useful for example if you have an unstable connection or need to leave intermittently.

By default it is set up to set a VRChat avatar parameter `hardware/headsetConnected` (Bool), which your avatar can be set up read to enter an "away" or "error" state to let other people know you can't hear or see them anymore.
As an example, my personal avatar plays a sound and flashes the outline red, then changes to a Resonite-style away material when I disconnect.

In addition, it (by default) sends a chatbox message `[Headset Disconnected]` and clears it when the connection is restored so you don't *need* specific avatar setup.

Setup:
- Make sure you have Python and PythonOSC installed. (`pip install python-osc`)
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json, that works too)
- Change both the `On Connect Script` and `On Disconnect Script` options to contain the *absolute* path to the script.bat file.
	- Windows users: this could be something like `C:\Users\user\...\alvr_streamer_windows\script\script.bat`
	- Linux users: make a .sh file that runs connection.py and use that instead. My current Linux VR setup doesn't use SteamVR or ALVR so I can't test unfortunately.

You can edit the script to change basic functionality, there are some variables near the top of [connection.py](connection.py) with descriptive comments so they should be easy to find.

Known Issues:
- At the moment on Windows it pops up a Command window whenever it runs. I do not know how to prevent this.


# HMD Battery Test - Test integration of battery level indicators

A set of tests to check avatar setup for battery-displaying functionality on VRChat avatars, for example, using my [Battery Prefab]([https://cubee.gumroad.com/l/battery-indicator](https://cubee.booth.pm/items/6093346)).

Contains tests:
- Set battery to Full (1)
- Set battery to Empty (may set a weird value. unsure exactly why, but it doesn't like sending -1)
- Charge test (0 to 1, set charging)
- Discharge test (1 to 0)
- Clear battery - set to a negative value so the avatar can know there is no battery
- Overlay integration: connected with battery full (sets open overlays to 2)
- Overlay integration: connected only - no battery sent (sets open overlays to 2)
- Disconnect OVR Toolkit integration (resets to expected default open overlays value to 255)

Some prefabs or avatars may support connected without battery status - this is what the `connected with no battery` test is for. [Battery Prefab](https://cubee.booth.pm/items/6093346) and [Badge](https://cubee.booth.pm/items/6100939) support this.
This is because the provider doesn't strictly need to send the battery parameter constantly, for example Wlx-Overlay-S only sends the battery every 10 seconds, while the open overlays are send every 0.1 seconds.
Indicators may display a "connecting" animation when they receive a different, frequently-updated parameter until they receive a battery level to at least show the connection is working.

My batteries use the following parameters internally:
- battery/level - The level shown on the batteries.
- battery/charging - Whether to show the charging indicator.
- battery/visible - If the battery indicator should be shown or not.
- battery/connected - If the provider is connected but may not be sending battery yet. This is not required to be set before showing the battery level.
They also have a layer that takes in parameters from external OSC-sending software and converts them to the internal format. This simplifies the logic.


# OSC Sender - That's all it is

A small script to send singular OSC values to specific addresses. That's it.
By default prepends "/avatar/parameters/" to all messages - this can be changed.



Scripts use Python OSC:
https://github.com/attwad/python-osc
