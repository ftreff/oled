#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display detailed system information in graph format.
It provides a display of CPU temp, cpu usage, memory usage, with IP address and system up time alternating on the last line.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""
import os
import time
from pathlib import Path
from datetime import datetime
#from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import subprocess as sp
import socket
from collections import OrderedDict

#---from demo_opts---

import sys
import logging

from luma.core import cmdline, error


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s - %(message)s'
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)


def display_settings(device, args):
    """
    Display a short summary of the settings.

    :rtype: str
    """
    iface = ''
    display_types = cmdline.get_display_types()
    if args.display not in display_types['emulator']:
        iface = f'Interface: {args.interface}\n'

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = 'unknown'

    import luma.core
    version = f'luma.{lib_name} {lib_version} (luma.core {luma.core.__version__})'

    return f'Version: {version}\nDisplay: {args.display}\n{iface}Dimensions: {device.width} x {device.height}\n{"-" * 60}'


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    # create device
    try:
        device = cmdline.create_device(args)
        #print(display_settings(device, args))
        print("Running OLED-SYS (ft_sys.py)")
        return device

    except error.Error as e:
        parser.error(e)
        return None

#---end from demo_opts.py---

def get_cpu_load():
    cpuLoad = os.getloadavg()
    return cpuLoad

def get_temp():
    temp = float(sp.getoutput("vcgencmd measure_temp").split("=")[1].split("'")[0])
    return temp


def get_cpu():
    return psutil.cpu_percent()


def get_mem():
    return psutil.virtual_memory().percent


def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage.used / usage.total * 100


def get_uptime():
    uptime = ("%s" % (datetime.now() - datetime.fromtimestamp(psutil.boot_time()))).split(".")[0]
    return "Up:%s" % (uptime)


def find_single_ipv4_address(addrs):
    for addr in addrs:
        if addr.family == socket.AddressFamily.AF_INET:  # IPv4
            return addr.address


def get_ipv4_address(interface_name=None):
    if_addrs = psutil.net_if_addrs()

    if isinstance(interface_name, str) and interface_name in if_addrs:
        addrs = if_addrs.get(interface_name)
        address = find_single_ipv4_address(addrs)
        return address if isinstance(address, str) else ""
    else:
        if_stats = psutil.net_if_stats()
        # remove loopback
        if_stats_filtered = {key: if_stats[key] for key, stat in if_stats.items() if "loopback" not in stat.flags}
        # sort interfaces by
        # 1. Up/Down
        # 2. Duplex mode (full: 2, half: 1, unknown: 0)
        if_names_sorted = [stat[0] for stat in sorted(if_stats_filtered.items(), key=lambda x: (x[1].isup, x[1].duplex), reverse=True)]
        if_addrs_sorted = OrderedDict((key, if_addrs[key]) for key in if_names_sorted if key in if_addrs)

        for _, addrs in if_addrs_sorted.items():
            address = find_single_ipv4_address(addrs)
            if isinstance(address, str):
                return address

        return ""


def get_ip(network_interface_name):
    return "IP:%s" % (get_ipv4_address(network_interface_name))


def format_percent(percent):
    return "%5.1f" % (percent)


def draw_text(draw, margin_x, line_num, text):
    draw.text((margin_x, margin_y_line[line_num]), text, font=font_default, fill="white")


def draw_bar(draw, line_num, percent):
    top_left_y = margin_y_line[line_num] + bar_margin_top
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width, top_left_y + bar_height), outline="white")
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width * percent / 100, top_left_y + bar_height), fill="white")


def draw_bar_full(draw, line_num):
    top_left_y = margin_y_line[line_num] + bar_margin_top
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width_full, top_left_y + bar_height), fill="white")
    draw.text((65, top_left_y - 2), "100 %", font=font_full, fill="black")


def stats(device):
    with canvas(device) as draw:
        temp = get_temp()
        draw_text(draw, 0, 0, "Temp")
        #draw_text(draw, margin_x_figure, 0, "%s'C" % (format_percent(temp)))
        draw_text(draw, margin_x_figure, 0, "%s'C" % temp)

        cpu = get_cpu()
        draw_text(draw, 0, 1, "CPU")
        if cpu < 100:
            draw_text(draw, margin_x_figure, 1, "%s %%" % (format_percent(cpu)))
            draw_bar(draw, 1, cpu)
        else:
            draw_bar_full(draw, 1)

        mem = get_mem()
        draw_text(draw, 0, 2, "Mem")
        if mem < 100:
            draw_text(draw, margin_x_figure, 2, "%s %%" % (format_percent(mem)))
            draw_bar(draw, 2, mem)
        else:
            draw_bar_full(draw, 2)

        load = get_cpu_load()
        draw_text(draw, 0, 3, "Load")
        #draw_text(draw, margin_x_figure, 3, "%s" % (format_percent(load[0])))
        draw_text(draw, margin_x_figure, 3, "%s" % load[0])

        #draw_text(draw, 0, 3, "Load:")
        #if load < 400:
        #draw_text(draw, margin_x_figure, 3, "%s %%" % (format_percent(load)))
            #draw_bar(draw, 3, disk)
        #else:
            #draw_bar_full(draw, 3)

        if datetime.now().second % (toggle_interval_seconds * 2) < toggle_interval_seconds:
            draw_text(draw, 0, 4, get_uptime())
        else:
            draw_text(draw, 0, 4, get_ip(network_interface_name))


font_size = 12
font_size_full = 10
margin_y_line = [0, 13, 25, 38, 51]
margin_x_figure = 78
margin_x_bar = 31
bar_width = 52
bar_width_full = 95
bar_height = 8
bar_margin_top = 3
toggle_interval_seconds = 4


# None : find suitable IPv4 address among all network interfaces
# or specify the desired interface name as string.
network_interface_name = None


device = get_device()
font_default = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")), font_size)
font_full = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")), font_size_full)


while True:
    stats(device)
    time.sleep(0.5)
