#!/usr/bin/env python3

import solid as sl
from keebgen import DactylManuform

# TODO: finish end user interface

"""
This file is an example to show how the library can be used, 
at least in a simple case.
"""

def main():
    keeb = DactylManuform(rows=4, cols=6)
    sl.scad_render_to_file(keeb.solid(), "example_keyboard.scad")


if __name__ == '__main__':
    main()