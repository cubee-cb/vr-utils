## VR Utils

A few tools I've made over my time playing VRChat.


## [ALVRConnectionOSC](alvr-connection-osc)
### OSC headset connection status updates for ALVR

A small program to send an OSC message with a BOOL value when a headset connects to or disconnects from ALVR, so things can match state. Useful for example if you have an unstable connection or need to leave intermittently.

By default it is set up to set a VRChat avatar parameter `hardware/headsetConnected` (Bool), which your avatar can be set up read to enter an "away" or "error" state to let other people know you can't hear or see them anymore.
As an example, my personal avatar plays a sound and flashes the outline red, then changes to a Resonite-style away material when I disconnect.

In addition, it (by default) sends a chatbox message `[Headset Disconnected]` and clears it when the connection is restored so you don't *need* specific avatar setup. (though it can be funny for others if your avatar does something in the meantime)

Setup:
- Make sure you have Python3 and PythonOSC installed. (`pip install python-osc`)
- Place the script files somewhere ALVR can get to.
- Open ALVR's config screen. (or session.json, that works too)
- Change the "On Connect Script" and "On Disconnect Script" options to contain:
  - Windows: the absolute path to the script.bat file. (e.g. `C:\Users\user\...\alvr_streamer_windows\script\script.bat`)
  - Linux: the absolute path to this file. Untested. (e.g. `/home/user/alvr/scripts/connection.py`)

You can edit the script to change basic functionality, there are some variables near the top of [connection.py](alvr-connection-osc/connection.py) with descriptive comments so they should be easy to find.

Known Issues:
- At the moment on Windows it pops up a Command window whenever it runs. I do not know how to prevent this.
- May not work on Linux, can't test it since my setup doesn't even use SteamVR, let alone ALVR.


## [ADB-OSC Battery Relay](adb-osc-battery.py)
### Battery level relay for standalone VRChat

This is a small script that uses ADB commands to obtain the headset's battery and charging status, to send over OSC much like WlxOverlay-S and similar overlays for PC. In fact, it simulates the exact headset parameters sent by WlxOverlay-S!

It should work with any Android-based version of VRChat, including Quest, Pico, and Mobile. Note that this still requires another device to run the script itself on. (unless you can run it in the background, maybe possible with termux or something)

Currently, it is only tested over USB, but set `ADB_USB = True` in the script to `False` and you should be able to configure it to run wirelessly too.

Usage: `adb-osc-battery.py <mode> <device_ip> <osc_port>`
- `adb-osc-battery.py` - Defaults to USB ADB, IP and Ports specified in the script.
- `adb-osc-battery.py usb 192.168.0.255` - USB ADB and send OSC to the address, default port.
- `adb-osc-battery.py wireless 192.168.0.255 9008` - Wireless ADB and send OSC to the address, port 9008.
- `adb-osc-battery.py wireless 192.168.0.255 verbose` - Wireless ADB and send OSC to the address, default port and show all data.

Step-by-step:
- Enable Developer Mode on your device and turn on USB Debugging and/or Wireless Debugging.
- Make sure you have Python3, `python-osc` and `adb-shell` installed. (`pip install python-osc`, `pip install adb-shell[usb]`)
- Edit the script to change `DEVICE_IP` to the IP address or hostname of your headset. This is always used for OSC, and when using ADB wirelessly.
- Run the script to generate key files for adb. These are stored alongside the script.
- If `ADB_USB` is `True`, it will try connecting over USB. Make sure the headset is the only Android device plugged in, and stop any other ADB servers. (`adb kill-server`)
  - Otherwise, if `ADB_USB` is `False`, it will try connecting wirelessly to `DEVICE_IP`. Make sure `Wireless Debugging` is enabled in Developer Settings if possible. (The setting doesn't seem to exist on my Pico 4)
- If all goes well, it should start printing battery level and charging state every 10 seconds.
  - Append `verbose` when running the script if you want to see all the data grabbed from the device.
- Opening the OSC debug panel in VRChat should show you the parameters updating as they get printed to the console.

Uses:
- [`python-osc`](https://github.com/attwad/python-osc)
- [`adb-shell`](https://github.com/JeffLIrion/adb_shell)


## [HMD Battery Test](hmd-battery-test.py)
### Test integration of battery level indicators

A set of tests to check avatar setup for battery-displaying functionality on VRChat avatars, for example, using my [Battery Prefab](https://cubee.booth.pm/items/6093346).

Contains tests:
- Set battery to Full (1)
- Set battery to Empty (may not work. unsure exactly why, but it doesn't like sending -1)
- Charge test (0 to 1, set charging)
- Discharge test (1 to 0)
- Clear battery - set to a negative value so the avatar can know there is no battery
- Overlay integration: connected with battery full (sets open overlays to 2)
- Overlay integration: connected only - no battery sent (sets open overlays to 2)
- Disconnect WlxOverlay-S integration (resets the expected default open overlays value to 255)

Some prefabs or avatars may support connected without battery status - this is what the `connected with no battery` test is for. [Battery Prefab](https://cubee.booth.pm/items/6093346) and [Badge](https://cubee.booth.pm/items/6100939) support this.

This is because the provider doesn't strictly need to send the battery parameter constantly, for example WlxOverlay-S only sends the battery every 10 seconds, while the open overlays are sent every 0.1 seconds.

Indicators may display a "connecting" animation when they receive a different, frequently-updated parameter until they receive a battery level to at least show the connection is working.

My batteries use the following parameters internally:
- `battery/level` - The level shown on the batteries.
- `battery/charging` - Whether to show the charging indicator.
- `battery/visible` - If the battery indicator should be shown or not.
- `battery/connected` - If the provider is connected but may not be sending battery yet. This is not required to be set before showing the battery level.
They also have a layer that takes in parameters from external OSC-sending software and converts them to the internal format. This simplifies the logic.


## [Snitch](snitch.py)
### [VRChat-AFK-Status](https://gitea.moe/lamp/VRChat-AFK-Status) for Kwin/Wayland

Pretty much just checks what the active window is, then shows or hides the chatbox with the active window's title based on if it's VRChat or not.

Since it uses `kdotool`, it only works on Kwin/Plasma. Could likely replace it inplace with `xdotool` if you're using an X-based environment.

ALSO, since it can send the window title to chatbox (there is a variable to turn this on), consider avoiding any windows that may show sensitive info in the title bar! (filenames, browser tabs, working directories, etc...)
People can also see when you have unsaved changes in your text files lol, since the `*` is part of the title.

Depends on `kdotool` being available in `PATH`. Simply runs `kdotool getactivewindow getwindowname` via `subprocess` and forwards it to the vrchat chatbox and an avatar parameter `focused`.


## [ProTV3 Playlist From Files](protv-playlist-from-files.py)

Walks a directory, reading in filenames and extracting YouTube IDs from them.
Expected format: `video title [youtube id]` (this is the format output by yt-dlp, extensions are ignored)
These are formatted into the ProTV3 playlist format, with the video title sanitised and a link generated from the ID, and written to a file named `protv_playlist.txt`.

If you don't want to store/download the actual video files, making dummy files works too, just name them `video title [youtube id]` as above.


## [OSC Sender](osc-sender.py)

A small script to send singular OSC values to specific addresses. That's it.
By default prepends "/avatar/parameters/" to all messages - this can be changed.

---

References:
- [PythonOSC](https://github.com/attwad/python-osc)
- [ADB Shell](https://github.com/JeffLIrion/adb_shell)

Shameless Self-Promotion:
- [Battery Prefab](https://cubee.booth.pm/items/6093346) (Full battery support; waiting for battery, battery level, charging, + trackers mode)
- [Badge Avatar](https://cubee.booth.pm/items/6100939) (Partial battery support; waiting for battery, battery level)
