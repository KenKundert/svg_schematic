#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Amp, Dot, Ground, Label, Pin, Resistor, Source, Wire
)
from inform import Error, error, os_error

try:
    with Schematic(
        filename = "inverting.svg",
        font_size=16,
        font_family='serif'
    ):

        vin = Pin(kind='in', name='in', w=1.5)
        vout = Pin(C=vin.C, xoff=350, kind='out', name='out', w=2)
        Wire([vin.C, vout.C])
        rin = Resistor(W=vin.C, xoff=25, name='Rin')
        vg = Dot(C=rin.E, xoff=25)
        rfb = Resistor(W=vg.C, xoff=25, name='Rfb')
        oj = Dot(C=rfb.E, xoff=25)
        amp = Amp(C=rfb.C, yoff=75, orient='-', kind='oa')
        Wire([oj.C, amp.o], kind='|-')
        gnd = Ground(C=amp.pi, xoff=-25, orient='h|')
        Wire([gnd.C, amp.pi])
        Wire([vg.C, amp.ni], kind='|-')
        Label(C=vg.C, name='Vg', loc='sw')

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
