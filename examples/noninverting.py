#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Amp, Dot, Ground, Label, Pin, Resistor, Source, Wire
)
from inform import Error, error, os_error

try:
    with Schematic(filename = "noninverting.svg", line_width=2):

        vin = Source(kind='sine')
        Label(C=vin.p, name='Vin', loc='n')
        Ground(C=vin.n)
        amp = Amp(pi=vin.p, xoff=100, kind='oa')
        Label(C=amp.ni, xoff=-25, name='Ve', loc='n')
        Wire([vin.p, amp.pi])
        out = Pin(C=amp.o, xoff=50, name='out', w=2)
        Wire([amp.o, out.C])
        oj = Dot(C=amp.o, xoff=25)
        r1 = Resistor(p=amp.ni, off=(-25, 50), name='R1', orient='v')
        Wire([r1.N, amp.ni], kind='|-')
        r2 = Resistor(C=amp.C, yoff=75, name='R2')
        Wire([r1.p, r2.W], kind='|-')
        Wire([oj.C, r2.E], kind='|-')
        fj = Dot(C=r2.W, xoff=-25)
        Ground(C=r1.n)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
