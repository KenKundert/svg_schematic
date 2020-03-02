#!/usr/bin/env python3

from svg_schematic import Schematic, Capacitor, Diode, Ground, Pin, Wire, Dot, with_x
from inform import Error, error, os_error

try:
    with Schematic(
        filename = "charge-pump.svg", line_width=2, background='none'):

        vin = Pin(kind='in', name=r'$V_{\rm in}$', w=2)
        p1 = Pin(C=vin.C, yoff=150, kind='in', name=r'$\phi_1$', w=2)
        p2 = Pin(C=p1.C, yoff=50, kind='in', name=r'$\phi_2$', w=2)
        d1 = Diode(a=vin.C, xoff=25, orient='h')
        c1 = Capacitor(p=d1.c, off=(25, 25), orient='v')
        d2 = Diode(a=d1.c, xoff=50, orient='h')
        c2 = Capacitor(p=d2.c, off=(25, 25), orient='v')
        d3 = Diode(a=d2.c, xoff=50, orient='h')
        c3 = Capacitor(p=d3.c, off=(25, 25), orient='v')
        d4 = Diode(a=d3.c, xoff=50, orient='h')
        c4 = Capacitor(p=d4.c, off=(25, 25), orient='v')
        d5 = Diode(a=d4.c, xoff=50, orient='h')
        c5 = Capacitor(p=d5.c, off=(25, 25), orient='v')
        vout = Pin(C=d5.c, xoff=75, kind='out', name=r'$V_{\rm out}$', w=2)
        Ground(t=c5.n)

        Wire([vin.t, d1.a])
        Wire([d1.c, d2.a])
        Wire([d2.c, d3.a])
        Wire([d3.c, d4.a])
        Wire([d4.c, d5.a])
        Wire([d5.c, vout.t])
        Wire([with_x(vin.t, c1.C), c1.p])
        Wire([with_x(vin.t, c2.C), c2.p])
        Wire([with_x(vin.t, c3.C), c3.p])
        Wire([with_x(vin.t, c4.C), c4.p])
        Wire([with_x(vin.t, c5.C), c5.p])
        Wire([p1.t, c1.n], kind='-|')
        Wire([p2.t, c2.n], kind='-|')
        co = Dot(C=with_x(p1.C, c2.C), color='white')     # wire cross over
        Wire([p1.t, c3.n], kind='-|')
        Wire([p2.t, c4.n], kind='-|')

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
