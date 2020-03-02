#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Capacitor, MOS, Inductor, Label, Source, Wire,
    midpoint, shift, shift_y,
)
from inform import Error, error, os_error

try:
    with Schematic(filename = "oscillator.svg", background='none', line_width=2):

        # resonator
        vdd = Label(loc='n', nudge=10, name=r'$V_{\rm dd}$')
        Wire([vdd.C, shift_y(vdd.C, 25)])
        ll = Inductor(p=shift(vdd.C, -125, 25), orient='v', name=r'$\frac{1}{2} L$')
        lr = Inductor(p=shift(vdd.C, 125, 25), orient='v|', name=r'$\frac{1}{2} L$')
        c = Capacitor(C=midpoint(ll.n, lr.n), orient='h', name='$C$')
        Wire([ll.p, lr.p])
        Wire([ll.n, c.p])
        Wire([lr.n, c.n])

        # gain stage
        ml = MOS(d=ll.n, yoff=50, orient='|')
        mr = MOS(d=lr.n, yoff=50, orient='')
        Wire([ll.n, ml.d])
        Wire([lr.n, mr.d])
        Wire([ml.g, shift_y(ml.g, -25), shift(ml.g, 50, -75), shift_y(mr.d, -25)])
        Wire([mr.g, shift_y(mr.g, -25), shift(mr.g, -50, -75), shift_y(ml.d, -25)])
        Wire([ml.s, mr.s])
        Source(p=midpoint(ml.s, mr.s), kind='idc', value=r'$I_{\rm ss}$')

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
