#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Matrix.

Adapted from:
https://github.com/pimoroni/unicorn-hat-hd/blob/master/examples/matrix-hd.py
"""

from random import randint, gauss
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
#*
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
        print(display_settings(device, args))
        return device

    except error.Error as e:
        parser.error(e)
        return None

#*

def matrix(device):
    wrd_rgb = [
        (154, 173, 154),
        (0, 255, 0),
        (0, 235, 0),
        (0, 220, 0),
        (0, 185, 0),
        (0, 165, 0),
        (0, 128, 0),
        (0, 0, 0),
        (154, 173, 154),
        (0, 145, 0),
        (0, 125, 0),
        (0, 100, 0),
        (0, 80, 0),
        (0, 60, 0),
        (0, 40, 0),
        (0, 0, 0)
    ]

    clock = 0
    blue_pilled_population = []
    max_population = device.width * 8
    regulator = framerate_regulator(fps=10)

    def increase_population():
        blue_pilled_population.append([randint(0, device.width), 0, gauss(1.2, 0.6)])

    while True:
        clock += 1
        with regulator:
            with canvas(device, dither=True) as draw:
                for person in blue_pilled_population:
                    x, y, speed = person
                    for rgb in wrd_rgb:
                        if 0 <= y < device.height:
                            draw.point((x, y), fill=rgb)
                        y -= 1
                    person[1] += speed

        if clock % 5 == 0 or clock % 3 == 0:
            increase_population()

        while len(blue_pilled_population) > max_population:
            blue_pilled_population.pop(0)


if __name__ == "__main__":
    try:
        matrix(get_device())
    except KeyboardInterrupt:
        pass
