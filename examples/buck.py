#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Amp, Box, Capacitor, Converter, Dot, Ground, Inductor, Label, MOS,
    Pin, Resistor, Switch, Wire, shift, shift_x, shift_y, with_x, with_y, midpoint
)
from inform import Error, error, os_error

try:
    with Schematic(
        filename = "buck.svg", line_width=2, background='none'):

        pvdd = Pin(kind='in', name='pvdd', w=3)
        avdd = Pin(C=pvdd.C, yoff=50, kind='in', name='avdd', w=3)
        Wire([avdd.C, shift_x(avdd.C, 50)])

        lvl = Pin(C=avdd.C, yoff=90, kind='in', name='lvl', w=3)
        reference = Converter(i=lvl.C, xoff=75, name='ref')
        lvl2ref = Wire([lvl.C, reference.i])
        Label(C=lvl2ref.m, kind='slash', name='6', loc='se')

        amp = Amp(pi=reference.o, xoff=50, kind='oa', name='amp')
        Wire([reference.o, amp.pi])
        C1 = Capacitor(p=amp.C, off=(-12.5, 75), orient='h')
        R1 = Resistor(p=C1.p, xoff=12.5, orient='h')
        C2 = Capacitor(C=midpoint(R1.C, C1.C), yoff=50, orient='h')
        Wire([C1.n, with_y(C1.n, amp.o)], kind='-|')
        Wire([R1.n, amp.ni], kind='|-')
        Wire([C2.p, R1.n], kind='-|')
        Wire([C2.n, C1.n], kind='-|')

        cmp = Amp(pi=amp.o, xoff=125, kind='comp', name='cmp')
        Wire([amp.o, cmp.pi])

        gd = Box(i=cmp.o, xoff=50, name='gate', value='drivers')
        Wire([cmp.o, gd.i])

        pfet = MOS(g=gd.N, yoff=-50, kind='p', orient='h')
        Wire([pfet.g, gd.N])
        Wire([pfet.s, pvdd.C])

        nfet = MOS(g=gd.o, xoff=25, kind='n', orient='v')
        Wire([nfet.g, gd.o])
        Wire([nfet.d, pfet.d], kind='|-')
        Ground(C=nfet.s)

        ind = Inductor(n=with_x(pfet.d, nfet.E), orient='h')
        Wire([pfet.d, ind.n])
        cap = Capacitor(p=ind.p, orient='v')
        Ground(C=cap.n)
        out = Pin(C=ind.p, xoff=100, kind='out', name='out', w=3)
        out_wire = Wire([ind.p, out.C])

        fb = shift_y(R1.n, 100)

        Rt = Resistor(n=with_x(fb, out_wire.m), orient='v')
        Rb = Resistor(p=with_x(fb, out_wire.m), orient='v')
        Wire([Rt.p, with_y(Rt.p, out.C)])
        Ground(C=Rb.n)

        RG = Box(o=C1.n, yoff=175)
        rg2cmp = Wire([RG.o, cmp.ni], kind='-|-')
        Dot(C=with_y(rg2cmp.m, fb), color='white')
        Wire([shift_x(RG.C, -30), shift(RG.C, -25, 25), shift(RG.C, 25, -25), shift_x(RG.C, 30)])
        Label(C=RG.S, loc='s', name='ramp_gen')
        Wire([R1.n, fb, Rt.n], kind='|-')

        en = Pin(C=lvl.C, yoff=250, kind='in', name='en', w=3)
        Wire([en.C, shift_x(en.C, 50)])
        avss = Pin(C=en.C, yoff=50, kind='in', name='avss', w=3)
        Wire([avss.C, shift_x(avss.C, 50)])

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
