# oled-sys(tem stats)
0.96 OLED Display System Stats

For use with 0.96 oled display on a Raspberry Pi.
To show the Raspberry Pi's system stats on an oled display.

Files:

ft_sys.py - this is a modified example script to show the stat I wanted displayed.
(temp, cpu usage with bar graph, memory usage with bar graph, system load, and the bottom line alternates between local ip address and system uptime.

installpkgs.sh - uses apt to update your systems packages then installs the required python3 luma.oled and psutil packages for the oled python scripts to run

