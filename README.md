# oled
0.96 OLED Display scripts

For use with 0.96 oled display on a Raspberry Pi.
The main use is to show the Raspberry Pi's system stats on an oled display.

Files:

ft_sys.py - this is a modified example script to show the stat I wanted displayed.
(temp, cpu usage with bar graph, memory usage with bar graph, system load, and the bottom line alternates between local ip address and system uptime.

ft_matrix.py - this displays a matrix code like screensaver.

installpkgs.sh - uses apt to update your systems packages then installs the required python3 luma.oled and psutil packages for the oled python scripts to run

oled-boot.sh - I run this scrip at system start up to enable the oled display.  It runs a matrix like screen saver for the first 45 seconds then displays the system stats indefinatly
