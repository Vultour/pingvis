#PingVis
**PingVis** is a simple python script for visualizing ping.

It has quite a fair number of use cases, however it's especially useful for diagnosing issues in areas with heavy Wi-Fi saturation that causes intermittent ping spikes.

![Screenshot](http://i.imgur.com/BBdNLil.png "PingVis Screenshot")

You can exit **PingVis** at any time by pressing the X button in the top right corner, `ESC`, `Q` or `CTRL + C` in terminal.

###Requirements
* Python 2.7
* PyGame
* Linux *(PingVis uses /bin/ping, however you can rewrite the getPing() function to wrap around anything you'd like)*


###Settings
**PingVis** is fully configurable by using the following command line switches:

`--help` - Prints the available command line switches and exits

`--address <IP>` - Specifies the IP address that is going to be pinged. *This can even be a hostname or anything else that `/bin/ping` accepts*

`--interval <float>` - Minimal number of seconds that will pass between each ping. This will ideally be a fraction of a second for real-time ping status. Default is 0.1. *Please note that each call to `getPing()` will block for the duration of it's execution, therefore it is highly likely that the resulting refresh interval will be higher if the ping takes too long. It is however guaranteed that the program will wait at least this long between pings.*

`--max-ping <float>` - Maximum ping that will be displayed. Values higher than this setting will be off the screen.

`--history <int>` - Number of historical values to store/display.

`--fullscreen` - Launches the program in fullscreen mode

`--window-height <int>` - Height of the PingVis window

`--window-width <int>` - Width of the PingVis window

`--ping-threshold <float>` - Any ping higher than this value will emit an **INTERNET DYING** message in console.


###Even more settings
You can tailor everything to your needs by modifying the code, however one thing that is especially notable is `LAG_THRESHOLD`. This is a list of "visual guides" - horizontal lines across the screen that help you more easily identify ping values. Default ones provided are *Counter-Strike lag (60ms)* and *Streaming lag (250ms)*.
