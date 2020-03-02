#!/usr/bin/env python3

from svg_schematic import Schematic, Amp, Box, Label, Pin, Source, Wire, shift_x
from inform import Error, error, os_error

try:
    with Schematic(
        filename = "feedback.svg",
        font_size=16,
        font_family='serif'
    ):

        summer = Source(kind='sum')
        amp = Amp(W=summer.E, xoff=25, name='$a$', kind='se')
        fb = Box(C=amp.C, yoff=100, name='$f$', h=1, orient='|')
        Label(C=summer.W, name='$+$', loc='nw')
        Label(C=summer.S, name='$-$', loc='sw')
        i = Pin(C=summer.W, xoff=-50, name='in', kind='in')
        o = Pin(C=amp.E, xoff=50, name='out', kind='out')

        Wire([i.C, summer.W])
        Wire([summer.E, amp.i])
        Wire([amp.E, o.C])
        Wire([shift_x(amp.E, 25), fb.i], kind='|-')
        Wire([summer.S, fb.W], kind='|-')

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
